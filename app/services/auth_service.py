from dataclasses import dataclass
from secrets import token_urlsafe
from time import time
from uuid import uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.auth import (
    ACCESS_TTL,
    LOGIN_BLOCK_TTL,
    LOGIN_MAX_ATTEMPTS,
    REFRESH_TTL,
    RESET_INTERVAL,
    RESET_TTL,
    CredencialInvalida,
    EmailDuplicado,
    Rol,
    normalizar_email,
)
from app.infrastructure.auth_models import RefreshToken, Usuario
from app.infrastructure.security import (
    TokensJWT,
    hash_password,
    hash_refresh,
    necesita_rehash,
    verificar_password,
)
from app.repositories.auth_repository import AuthRepositorio


@dataclass(frozen=True)
class SesionEmitida:
    access_token: str
    refresh_token: str
    refresh_expira: int


def registrar_usuario(db: Session, email: str, password: str, rol: Rol = Rol.USUARIO) -> Usuario:
    usuario = Usuario(email=normalizar_email(email), password_hash=hash_password(password), rol=rol)
    db.add(usuario)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        if AuthRepositorio(db).usuario_por_email(usuario.email) is not None:
            raise EmailDuplicado from None
        raise
    return usuario


class AuthServicio:
    def __init__(self, db: Session, jwt: TokensJWT):
        self.db = db
        self.repo = AuthRepositorio(db)
        self.jwt = jwt

    def _emitir_sesion(
        self, usuario: Usuario, familia: str, expira: int, ahora: int
    ) -> SesionEmitida:
        refresh = token_urlsafe(32)
        self.db.add(
            RefreshToken(token_hash=hash_refresh(refresh), usuario_id=usuario.id, familia=familia, expira=expira)
        )
        access = self.jwt.emitir(usuario.id, "access", ahora + ACCESS_TTL, ver=usuario.version_acceso)
        return SesionEmitida(access, refresh, expira)

    def login(self, email: str, password: str) -> SesionEmitida:
        usuario = self.repo.usuario_por_email(normalizar_email(email), bloquear=True)
        ahora = int(time())
        if not usuario or not usuario.activo:
            verificar_password(password, None)
            raise CredencialInvalida
        if usuario.bloqueo_hasta > ahora:
            raise CredencialInvalida
        if not verificar_password(password, usuario.password_hash):
            usuario.intentos_fallidos += 1
            if usuario.intentos_fallidos >= LOGIN_MAX_ATTEMPTS:
                usuario.bloqueo_hasta = ahora + LOGIN_BLOCK_TTL
                usuario.intentos_fallidos = 0
            self.db.commit()
            raise CredencialInvalida

        usuario.intentos_fallidos = 0
        usuario.bloqueo_hasta = 0
        if necesita_rehash(usuario.password_hash):
            usuario.password_hash = hash_password(password)
        self.repo.borrar_refresh_vencidos(usuario.id, ahora)
        sesion = self._emitir_sesion(usuario, uuid4().hex, ahora + REFRESH_TTL, ahora)
        self.db.commit()
        return sesion

    def usuario_actual(self, token: str) -> Usuario:
        claims = self.jwt.validar(token, "access", "ver")
        usuario = self.repo.usuario_por_id(int(claims["sub"]))
        if not usuario or not usuario.activo or usuario.version_acceso != claims["ver"]:
            raise CredencialInvalida
        return usuario

    def _bloquear_sesion(self, token: str) -> tuple[Usuario, RefreshToken]:
        token_hash = hash_refresh(token)
        usuario_id = self.repo.usuario_id_por_refresh(token_hash)
        if usuario_id is None:
            raise CredencialInvalida

        # Login, rotación, logout y reset toman el mismo bloqueo antes de modificar sesiones.
        usuario = self.repo.usuario_por_id(usuario_id, bloquear=True)
        refresh = self.repo.refresh(token_hash)
        if not usuario or not usuario.activo or not refresh:
            raise CredencialInvalida
        return usuario, refresh

    def renovar(self, token: str) -> SesionEmitida:
        usuario, refresh = self._bloquear_sesion(token)
        ahora = int(time())
        if refresh.revocado or refresh.expira <= ahora:
            raise CredencialInvalida
        if refresh.rotado:
            self.repo.revocar_refresh(usuario.id, refresh.familia)
            self.db.commit()
            raise CredencialInvalida

        refresh.rotado = True
        sesion = self._emitir_sesion(usuario, refresh.familia, refresh.expira, ahora)
        self.db.commit()
        return sesion

    def logout(self, token: str) -> None:
        try:
            usuario, refresh = self._bloquear_sesion(token)
        except CredencialInvalida:
            return
        self.repo.revocar_refresh(usuario.id, refresh.familia)
        self.db.commit()

    def preparar_recuperacion(self, email: str) -> tuple[str, str] | None:
        usuario = self.repo.usuario_por_email(normalizar_email(email), bloquear=True)
        ahora = int(time())
        if not usuario or not usuario.activo or usuario.reset_disponible_desde > ahora:
            return None

        usuario.reset_jti = uuid4().hex
        usuario.reset_disponible_desde = ahora + RESET_INTERVAL
        destinatario = usuario.email
        token = self.jwt.emitir(usuario.id, "password_reset", ahora + RESET_TTL, jti=usuario.reset_jti)
        self.db.commit()
        return destinatario, token

    def restablecer(self, token: str, password: str) -> None:
        claims = self.jwt.validar(token, "password_reset", "jti")
        usuario = self.repo.usuario_por_id(int(claims["sub"]), bloquear=True)
        if (
            not usuario
            or not usuario.activo
            or not usuario.reset_jti
            or usuario.reset_jti != claims["jti"]
            or claims["exp"] <= int(time())
        ):
            raise CredencialInvalida

        usuario.password_hash = hash_password(password)
        usuario.reset_jti = None
        usuario.version_acceso += 1
        usuario.intentos_fallidos = 0
        usuario.bloqueo_hasta = 0
        self.repo.revocar_refresh(usuario.id)
        self.db.commit()
