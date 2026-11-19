"""Agrega cuentas y sesiones sin modificar los datos de negocio."""

import sqlalchemy as sa
from alembic import op

revision = "71fd6e842b19"
down_revision = "2a0a434ad066"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(254), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("rol", sa.String(16), nullable=False),
        sa.Column("activo", sa.Boolean, nullable=False),
        sa.Column("version_acceso", sa.Integer, nullable=False),
        sa.Column("intentos_fallidos", sa.Integer, nullable=False),
        sa.Column("bloqueo_hasta", sa.BigInteger, nullable=False),
        sa.Column("reset_disponible_desde", sa.BigInteger, nullable=False),
        sa.Column("reset_jti", sa.String(32), nullable=True),
        sa.UniqueConstraint("email", name="uq_usuarios_email"),
        sa.CheckConstraint("rol IN ('usuario', 'admin')", name="ck_usuarios_rol"),
    )
    op.create_table(
        "refresh_tokens",
        sa.Column("token_hash", sa.String(64), primary_key=True),
        sa.Column("usuario_id", sa.Integer, sa.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False),
        sa.Column("familia", sa.String(32), nullable=False),
        sa.Column("expira", sa.BigInteger, nullable=False),
        sa.Column("rotado", sa.Boolean, nullable=False),
        sa.Column("revocado", sa.Boolean, nullable=False),
    )
    op.create_index("ix_refresh_tokens_usuario_familia", "refresh_tokens", ["usuario_id", "familia"])
    op.create_index("ix_refresh_tokens_expira", "refresh_tokens", ["expira"])


def downgrade() -> None:
    op.drop_table("refresh_tokens")
    op.drop_table("usuarios")
