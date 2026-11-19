from sqlalchemy import BigInteger, Boolean, CheckConstraint, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.domain.auth import Rol


class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = (CheckConstraint("rol IN ('usuario', 'admin')", name="ck_usuarios_rol"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    rol: Mapped[str] = mapped_column(String(16), default=Rol.USUARIO)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    version_acceso: Mapped[int] = mapped_column(Integer, default=0)
    intentos_fallidos: Mapped[int] = mapped_column(Integer, default=0)
    bloqueo_hasta: Mapped[int] = mapped_column(BigInteger, default=0)
    reset_disponible_desde: Mapped[int] = mapped_column(BigInteger, default=0)
    reset_jti: Mapped[str | None] = mapped_column(String(32))


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    __table_args__ = (
        Index("ix_refresh_tokens_usuario_familia", "usuario_id", "familia"),
        Index("ix_refresh_tokens_expira", "expira"),
    )

    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"))
    familia: Mapped[str] = mapped_column(String(32))
    expira: Mapped[int] = mapped_column(BigInteger)
    rotado: Mapped[bool] = mapped_column(Boolean, default=False)
    revocado: Mapped[bool] = mapped_column(Boolean, default=False)
