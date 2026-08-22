from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from app.config.Settings import settings
from app.database.Base import Base
from app.database.ConnectionConfig import construir_configuracion_conexion

from app.models.Bitacora import Bitacora
from app.models.Cliente import Cliente
from app.models.Deuda import Deuda
from app.models.Espacio import Espacio
from app.models.Notificacion import Notificacion
from app.models.Ocupacion import Ocupacion
from app.models.Pago import Pago
from app.models.Qr import Qr
from app.models.Reserva import Reserva
from app.models.Rol import Rol
from app.models.Sector import Sector
from app.models.Usuario import Usuario
from app.models.Vehiculo import Vehiculo


_MODELOS_REGISTRADOS = (
    Bitacora,
    Cliente,
    Deuda,
    Espacio,
    Notificacion,
    Ocupacion,
    Pago,
    Qr,
    Reserva,
    Rol,
    Sector,
    Usuario,
    Vehiculo,
)

config = context.config
raw_database_url = settings.MIGRATION_DATABASE_URL or settings.DATABASE_URL
database_url, connect_args = construir_configuracion_conexion(raw_database_url)

config.set_main_option("sqlalchemy.url", database_url.replace("%", "%%"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
        connect_args=connect_args,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
