import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from app.database.Session import get_db
from app.main import app


client = TestClient(app)


class BaseDisponible:
    def execute(self, _consulta):
        return 1


class BaseNoDisponible:
    def execute(self, _consulta):
        raise SQLAlchemyError("Base de datos no disponible")


def usar_base_disponible():
    yield BaseDisponible()


def usar_base_no_disponible():
    yield BaseNoDisponible()


@pytest.fixture(autouse=True)
def limpiar_dependencias():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


def test_ruta_raiz_muestra_informacion_de_la_api():
    respuesta = client.get("/")

    assert respuesta.status_code == 200
    assert respuesta.json() == {
        "service": "ParkSmart API",
        "version": "1.0.0",
        "status": "ok",
        "docs": "/docs",
    }


def test_liveness_responde_sin_consultar_base_de_datos():
    respuesta = client.get("/health")

    assert respuesta.status_code == 200
    assert respuesta.json() == {
        "status": "ok",
        "message": "API ParkSmart en ejecución",
    }


def test_readiness_responde_200_con_base_disponible():
    app.dependency_overrides[get_db] = usar_base_disponible

    respuesta = client.get("/health/ready")

    assert respuesta.status_code == 200
    assert respuesta.json() == {
        "status": "ready",
        "message": "Conexión a base de datos exitosa",
    }


def test_readiness_responde_503_con_base_no_disponible():
    app.dependency_overrides[get_db] = usar_base_no_disponible

    respuesta = client.get("/health/ready")

    assert respuesta.status_code == 503
    assert respuesta.json() == {
        "detail": "Base de datos no disponible",
    }