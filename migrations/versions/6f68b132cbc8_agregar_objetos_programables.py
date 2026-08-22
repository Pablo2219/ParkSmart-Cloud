"""Agregar funciones, procedimientos, triggers y vistas.

Revision ID: 6f68b132cbc8
Revises: 38f1b9784628
Create Date: 2026-08-04
"""

from pathlib import Path
from typing import Sequence, Union

from alembic import op


# Identificadores utilizados por Alembic.
revision: str = "6f68b132cbc8"
down_revision: Union[str, Sequence[str], None] = "38f1b9784628"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


SQL_FILES = (
    "Functions.sql",
    "Procedures.sql",
    "Triggers.sql",
    "Views.sql",
)

VIEWS = (
    "vw_bitacoradetalle",
    "vw_clientesactivos",
    "vw_deudaspendientes",
    "vw_espaciosdisponibles",
    "vw_notificacionespendientes",
    "vw_ocupacionesactivas",
    "vw_pagospendientes",
    "vw_qractivos",
    "vw_reservasactivas",
    "vw_reservasdetalle",
)

TRIGGERS = (
    "TR_Cliente_AI_Bitacora",
    "TR_Notificacion_BU",
    "TR_Ocupacion_AI",
    "TR_Ocupacion_AU",
    "TR_Ocupacion_BU",
    "TR_Pago_AU_Bitacora",
    "TR_Pago_BU",
    "TR_Qr_BI",
    "TR_Reserva_AI",
    "TR_Reserva_AI_Bitacora",
    "TR_Reserva_AU",
)

PROCEDURES = (
    "SP_CancelarReserva",
    "SP_CrearReserva",
    "SP_FinalizarOcupacionGenerarPago",
    "SP_GenerarDeudaPago",
    "SP_GenerarQrReserva",
    "SP_IniciarOcupacion",
    "SP_RegistrarCliente",
    "SP_RegistrarPago",
    "SP_RegistrarVehiculo",
)

FUNCTIONS = (
    "FN_CalcularHorasCobro",
    "FN_CalcularImpuesto",
    "FN_CalcularSubtotalPago",
    "FN_CalcularTiempoOcupacion",
    "FN_CalcularTotalPago",
    "FN_ValidarQrActivo",
    "FN_VerificarPagoVencido",
)


def _sql_directory() -> Path:
    return Path(__file__).resolve().parents[2] / "database" / "scripts"


def _read_statements(file_name: str) -> list[str]:
    path = _sql_directory() / file_name
    content = path.read_text(encoding="utf-8-sig")
    statements: list[str] = []
    buffer: list[str] = []
    delimiter = ";"

    for raw_line in content.splitlines():
        stripped_line = raw_line.strip()

        if stripped_line.upper().startswith("DELIMITER "):
            delimiter = stripped_line.split(maxsplit=1)[1]
            continue

        buffer.append(raw_line)
        candidate = "\n".join(buffer).rstrip()

        if candidate.endswith(delimiter):
            statement = candidate[: -len(delimiter)].strip()
            if statement:
                statements.append(statement)
            buffer = []

    remaining = "\n".join(buffer).strip()
    if remaining:
        statements.append(remaining)

    return statements


def _execute_sql_file(file_name: str) -> None:
    connection = op.get_bind()

    for statement in _read_statements(file_name):
        connection.exec_driver_sql(
            statement,
            execution_options={"no_parameters": True},
        )


def _drop_objects(object_type: str, names: tuple[str, ...]) -> None:
    connection = op.get_bind()

    for name in names:
        connection.exec_driver_sql(
            f"DROP {object_type} IF EXISTS `{name}`"
        )


def upgrade() -> None:
    """Instala los objetos programables de ParkSmart."""
    for file_name in SQL_FILES:
        _execute_sql_file(file_name)


def downgrade() -> None:
    """Elimina los objetos programables en orden de dependencias."""
    _drop_objects("VIEW", VIEWS)
    _drop_objects("TRIGGER", TRIGGERS)
    _drop_objects("PROCEDURE", PROCEDURES)
    _drop_objects("FUNCTION", FUNCTIONS)