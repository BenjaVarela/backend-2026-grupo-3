from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config import jwt_secret
from app.database import get_db
from app.domain.auth import CredencialInvalida, Rol
from app.infrastructure.auth_models import Usuario
from app.infrastructure.security import TokensJWT
from app.services.auth_service import AuthServicio


bearer = HTTPBearer(auto_error=False)
DB = Annotated[Session, Depends(get_db)]

RESPUESTA_401 = {401: {"description": "Se requiere una credencial válida."}}
RESPUESTA_403 = {403: {"description": "La cuenta no tiene permiso para esta operación."}}
RESPUESTAS_ADMIN = RESPUESTA_401 | RESPUESTA_403


def error_bearer() -> HTTPException:
    return HTTPException(
        status_code=401,
        detail="Credencial de acceso inválida o ausente.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def tokens_jwt() -> TokensJWT:
    return TokensJWT(jwt_secret())


def auth_servicio(db: DB, jwt: Annotated[TokensJWT, Depends(tokens_jwt)]) -> AuthServicio:
    return AuthServicio(db, jwt)


ServicioAuth = Annotated[AuthServicio, Depends(auth_servicio)]


def usuario_actual(
    servicio: ServicioAuth,
    credencial: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> Usuario:
    if credencial is None or len(credencial.credentials) > 2048:
        raise error_bearer()
    try:
        return servicio.usuario_actual(credencial.credentials)
    except CredencialInvalida:
        raise error_bearer() from None


UsuarioActual = Annotated[Usuario, Depends(usuario_actual)]


def requiere_admin(usuario: UsuarioActual) -> None:
    if usuario.rol != Rol.ADMIN:
        raise HTTPException(status_code=403, detail="Se requiere el perfil administrador.")
