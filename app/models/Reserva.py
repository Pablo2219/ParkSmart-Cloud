from datetime import datetime
from typing import Optional

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Index,
    String,
    text,
)
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Reserva(Base):
    __tablename__ = "reserva"

    __table_args__ = (
        Index(
            "UK_Reserva_CodigoReserva",
            "codigoReserva",
            unique=True,
        ),
        Index(
            "IX_Reserva_IdCliente",
            "idCliente",
        ),
        Index(
            "IX_Reserva_IdVehiculo",
            "idVehiculo",
        ),
        Index(
            "IX_Reserva_IdEspacio",
            "idEspacio",
        ),
        Index(
            "IX_Reserva_Estado",
            "estado",
        ),
        Index(
            "IX_Reserva_Fechas",
            "fechaInicioReserva",
            "fechaFinReserva",
        ),
        CheckConstraint(
            "fechaFinReserva > fechaInicioReserva",
            name="CK_Reserva_Fechas",
        ),
    )

    idReserva: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    idCliente: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "cliente.idCliente",
            name="FK_Reserva_Cliente",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    idVehiculo: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "vehiculo.idVehiculo",
            name="FK_Reserva_Vehiculo",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    idEspacio: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "espacio.idEspacio",
            name="FK_Reserva_Espacio",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    codigoReserva: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    fechaInicioReserva: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    fechaFinReserva: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "PENDIENTE",
            "CONFIRMADA",
            "CANCELADA",
            "VENCIDA",
            "UTILIZADA",
        ),
        nullable=False,
        server_default=text("'PENDIENTE'"),
    )

    observaciones: Mapped[Optional[str]] = mapped_column(
        String(250),
        nullable=True,
    )

    fechaCreacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    fechaActualizacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text(
            "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
        ),
    )