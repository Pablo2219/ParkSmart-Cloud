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


class Qr(Base):
    __tablename__ = "qr"

    __table_args__ = (
        Index(
            "UK_Qr_CodigoQr",
            "codigoQr",
            unique=True,
        ),
        Index(
            "UK_Qr_IdReserva",
            "idReserva",
            unique=True,
        ),
        Index(
            "IX_Qr_Estado",
            "estado",
        ),
        Index(
            "IX_Qr_Fechas",
            "fechaActivacion",
            "fechaExpiracion",
        ),
        CheckConstraint(
            "fechaExpiracion > fechaActivacion",
            name="CK_Qr_Fechas",
        ),
    )

    idQr: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    idReserva: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "reserva.idReserva",
            name="FK_Qr_Reserva",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    codigoQr: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    tokenQr: Mapped[Optional[str]] = mapped_column(
        String(250),
        nullable=True,
    )

    fechaGeneracion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    fechaValidezInicio: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    fechaValidezFin: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    fechaActivacion: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    fechaExpiracion: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    fechaUso: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "GENERADO",
            "ACTIVO",
            "USADO",
            "VENCIDO",
            "CANCELADO",
        ),
        nullable=False,
        server_default=text("'GENERADO'"),
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