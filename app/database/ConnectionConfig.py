import os
import tempfile
from pathlib import Path

from sqlalchemy.engine import URL, make_url

from app.config.Settings import settings


_SSL_QUERY_KEYS = (
    "ssl-mode",
    "ssl_mode",
    "sslmode",
    "ssl-ca",
    "ssl_ca",
)


def normalizar_database_url(raw_url: str) -> str:
    """Normaliza URLs MySQL de proveedores cloud para usar PyMySQL."""
    url = make_url(raw_url)

    if url.drivername == "mysql":
        url = url.set(drivername="mysql+pymysql")

    url = url.difference_update_query(_SSL_QUERY_KEYS)
    return url.render_as_string(hide_password=False)


def _es_mysql_remoto(url: URL) -> bool:
    return (
        url.drivername.startswith("mysql")
        and url.host not in {"db", "localhost", "127.0.0.1", None}
    )


def _materializar_ca() -> str | None:
    contenido = settings.DATABASE_CA_CERT.strip()
    if not contenido:
        return None

    ruta = Path(tempfile.gettempdir()) / "parksmart-managed-db-ca.pem"
    ruta.write_text(contenido + "\n", encoding="utf-8")
    try:
        os.chmod(ruta, 0o600)
    except OSError:
        pass
    return str(ruta)


def construir_configuracion_conexion(raw_url: str) -> tuple[str, dict]:
    database_url = normalizar_database_url(raw_url)
    url = make_url(database_url)
    connect_args: dict = {}

    if _es_mysql_remoto(url):
        ca_path = _materializar_ca()
        if ca_path:
            connect_args["ssl"] = {
                "ca": ca_path,
                "check_hostname": True,
            }

    return database_url, connect_args
