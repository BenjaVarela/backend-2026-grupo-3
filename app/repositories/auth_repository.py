from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from app.infrastructure.auth_models import RefreshToken, Usuario


class AuthRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def usuario_por_email(self, email: str, *, bloquear: bool = False) -> Usuario | None:
        consulta = select(Usuario).where(Usuario.email == email)
        return self.db.scalar(consulta.with_for_update() if bloquear else consulta)

    def usuario_por_id(self, usuario_id: int, *, bloquear: bool = False) -> Usuario | None:
        consulta = select(Usuario).where(Usuario.id == usuario_id)
        return self.db.scalar(consulta.with_for_update() if bloquear else consulta)

    def usuario_id_por_refresh(self, token_hash: str) -> int | None:
        return self.db.scalar(select(RefreshToken.usuario_id).where(RefreshToken.token_hash == token_hash))

    def refresh(self, token_hash: str) -> RefreshToken | None:
        return self.db.get(RefreshToken, token_hash)

    def revocar_refresh(self, usuario_id: int, familia: str | None = None) -> None:
        consulta = update(RefreshToken).where(RefreshToken.usuario_id == usuario_id)
        if familia is not None:
            consulta = consulta.where(RefreshToken.familia == familia)
        self.db.execute(consulta.values(revocado=True))

    def borrar_refresh_vencidos(self, usuario_id: int, ahora: int) -> None:
        self.db.execute(
            delete(RefreshToken).where(RefreshToken.usuario_id == usuario_id, RefreshToken.expira <= ahora)
        )
