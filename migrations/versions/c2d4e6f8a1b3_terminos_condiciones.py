"""Agrega aceptación versionada de términos y condiciones.

Revision ID: c2d4e6f8a1b3
Revises: 9b7c2a1e4f10
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "c2d4e6f8a1b3"
down_revision: Union[str, Sequence[str], None] = "9b7c2a1e4f10"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("usuario", sa.Column("aceptaTerminos", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("usuario", sa.Column("fechaAceptacionTerminos", sa.DateTime(), nullable=True))
    op.add_column("usuario", sa.Column("versionTerminos", sa.String(20), nullable=True))

    # Existing administrator remains usable; its explicit legacy acceptance is retained.
    op.execute("UPDATE usuario SET aceptaTerminos = 1, fechaAceptacionTerminos = COALESCE(fechaConsentimiento, CURRENT_TIMESTAMP), versionTerminos = '1.0' WHERE nombreUsuario = 'admin'")


def downgrade() -> None:
    op.drop_column("usuario", "versionTerminos")
    op.drop_column("usuario", "fechaAceptacionTerminos")
    op.drop_column("usuario", "aceptaTerminos")
