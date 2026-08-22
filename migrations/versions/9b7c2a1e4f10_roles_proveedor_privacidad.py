"""Agrega proveedores, geolocalizacion y consentimiento de privacidad.

Revision ID: 9b7c2a1e4f10
Revises: 6f68b132cbc8
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "9b7c2a1e4f10"
down_revision: Union[str, Sequence[str], None] = "6f68b132cbc8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ADMIN_HASH = "$argon2id$v=19$m=65536,t=3,p=4$h72JsZmHx9KDqnEgnGOW/Q$hQyD/+R06mCF2TSars4TGlNhJ5hW/bwtkTDhsZaAfkM"


def upgrade() -> None:
    op.create_table(
        "proveedor",
        sa.Column("idProveedor", sa.BigInteger().with_variant(sa.BIGINT(unsigned=True), "mysql"), primary_key=True, autoincrement=True),
        sa.Column("identificacion", sa.String(20), nullable=False),
        sa.Column("nombreComercial", sa.String(120), nullable=False),
        sa.Column("telefono", sa.String(20), nullable=False),
        sa.Column("correoElectronico", sa.String(120), nullable=False),
        sa.Column("direccion", sa.String(250), nullable=True),
        sa.Column("latitud", sa.Numeric(10, 7), nullable=True),
        sa.Column("longitud", sa.Numeric(10, 7), nullable=True),
        sa.Column("estado", sa.Enum("ACTIVO", "INACTIVO", "SUSPENDIDO"), nullable=False, server_default="ACTIVO"),
        sa.Column("fechaCreacion", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("fechaActualizacion", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("identificacion", name="UK_Proveedor_Identificacion"),
        sa.UniqueConstraint("correoElectronico", name="UK_Proveedor_CorreoElectronico"),
        sa.CheckConstraint("latitud IS NULL OR (latitud BETWEEN -90 AND 90)", name="CK_Proveedor_Latitud"),
        sa.CheckConstraint("longitud IS NULL OR (longitud BETWEEN -180 AND 180)", name="CK_Proveedor_Longitud"),
        mysql_engine="InnoDB",
    )

    op.add_column("usuario", sa.Column("idProveedor", sa.BigInteger().with_variant(sa.BIGINT(unsigned=True), "mysql"), nullable=True))
    op.add_column("usuario", sa.Column("aceptaPrivacidad", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("usuario", sa.Column("fechaConsentimiento", sa.DateTime(), nullable=True))
    op.add_column("usuario", sa.Column("versionPoliticaPrivacidad", sa.String(20), nullable=True))
    op.create_index("IX_Usuario_IdProveedor", "usuario", ["idProveedor"])
    op.create_foreign_key("FK_Usuario_Proveedor", "usuario", "proveedor", ["idProveedor"], ["idProveedor"], ondelete="SET NULL", onupdate="CASCADE")

    op.add_column("sector", sa.Column("idProveedor", sa.BigInteger().with_variant(sa.BIGINT(unsigned=True), "mysql"), nullable=True))
    op.add_column("sector", sa.Column("latitud", sa.Numeric(10, 7), nullable=True))
    op.add_column("sector", sa.Column("longitud", sa.Numeric(10, 7), nullable=True))
    op.create_index("IX_Sector_IdProveedor", "sector", ["idProveedor"])
    op.create_foreign_key("FK_Sector_Proveedor", "sector", "proveedor", ["idProveedor"], ["idProveedor"], ondelete="SET NULL", onupdate="CASCADE")

    op.add_column("espacio", sa.Column("latitud", sa.Numeric(10, 7), nullable=True))
    op.add_column("espacio", sa.Column("longitud", sa.Numeric(10, 7), nullable=True))

    op.execute("INSERT INTO rol (nombreRol, descripcion, estado) SELECT 'CLIENTE', 'Usuario que reserva espacios de parqueo', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM rol WHERE nombreRol = 'CLIENTE')")
    op.execute("INSERT INTO rol (nombreRol, descripcion, estado) SELECT 'ADMINISTRADOR', 'Administrador del sistema ParkSmart', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM rol WHERE nombreRol = 'ADMINISTRADOR')")
    op.execute("INSERT INTO rol (nombreRol, descripcion, estado) SELECT 'PROVEEDOR', 'Usuario encargado de ofrecer y administrar servicios de parqueo', 'ACTIVO' WHERE NOT EXISTS (SELECT 1 FROM rol WHERE nombreRol = 'PROVEEDOR')")

    op.get_bind().execute(
        sa.text(
            "INSERT INTO usuario (idRol, nombreUsuario, correoElectronico, contrasenaHash, estado, aceptaPrivacidad) "
            "SELECT idRol, 'admin', 'admin@parksmart.com', :hash, 'ACTIVO', 1 FROM rol "
            "WHERE nombreRol='ADMINISTRADOR' AND NOT EXISTS (SELECT 1 FROM usuario WHERE nombreUsuario='admin')"
        ),
        {"hash": ADMIN_HASH},
    )


def downgrade() -> None:
    op.drop_column("espacio", "longitud")
    op.drop_column("espacio", "latitud")
    op.drop_constraint("FK_Sector_Proveedor", "sector", type_="foreignkey")
    op.drop_index("IX_Sector_IdProveedor", table_name="sector")
    op.drop_column("sector", "longitud")
    op.drop_column("sector", "latitud")
    op.drop_column("sector", "idProveedor")
    op.drop_constraint("FK_Usuario_Proveedor", "usuario", type_="foreignkey")
    op.drop_index("IX_Usuario_IdProveedor", table_name="usuario")
    op.drop_column("usuario", "versionPoliticaPrivacidad")
    op.drop_column("usuario", "fechaConsentimiento")
    op.drop_column("usuario", "aceptaPrivacidad")
    op.drop_column("usuario", "idProveedor")
    op.drop_table("proveedor")
