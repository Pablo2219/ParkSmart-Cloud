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
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Ocupacion(Base):
    __tablename__ = "ocupacion"

    __table_args__ = (
        Index(
            "UK_Ocupacion_IdReserva",
            "idReserva",
            unique=True,
        ),
        Index(
            "UK_Ocupacion_IdQr",
            "idQr",
            unique=True,
        ),
        Index(
            "IX_Ocupacion_Estado",
            "estado",
        ),
        Index(
            "IX_Ocupacion_FechaEntrada",
            "fechaEntrada",
        ),
        Index(
            "IX_Ocupacion_FechaSalida",
            "fechaSalida",
        ),
        CheckConstraint(
            "fechaSalida IS NULL OR fechaSalida > fechaEntrada",
            name="CK_Ocupacion_Fechas",
        ),
    )

    idOcupacion: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    idReserva: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "reserva.idReserva",
            name="FK_Ocupacion_Reserva",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    idEspacio: Mapped[Optional[int]] = mapped_column(
        BIGINT(unsigned=True),
        nullable=True,
    )

    idQr: Mapped[Optional[int]] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "qr.idQr",
            name="FK_Ocupacion_Qr",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=True,
    )

    fechaEntrada: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    fechaSalida: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    tiempoTotalMinutos: Mapped[Optional[int]] = mapped_column(
        INTEGER(unsigned=True),
        nullable=True,
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "EN_CURSO",
            "FINALIZADA",
            "CANCELADA",
        ),
        nullable=False,
        server_default=text("'EN_CURSO'"),
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