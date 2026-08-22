from sqlalchemy import create_engine

from app.config.Settings import settings
from app.database.ConnectionConfig import construir_configuracion_conexion


database_url, connect_args = construir_configuracion_conexion(
    settings.DATABASE_URL
)

engine = create_engine(
    database_url,
    pool_pre_ping=True,
    pool_recycle=1800,
    connect_args=connect_args,
)
