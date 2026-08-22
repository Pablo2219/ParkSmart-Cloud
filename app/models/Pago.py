from datetime import datetime
from decimal import Decimal
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
from sqlalchemy.dialects.mysql import BIGINT, DECIMAL, INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Pago(Base):
    __tablename__ = "pago"

    __table_args__ = (
        Index(
            "UK_Pago_CodigoPago",
            "codigoPago",
            unique=True,
        ),
        Index(
            "UK_Pago_IdOcupacion",
            "idOcupacion",
            unique=True,
        ),
        Index(
            "IX_Pago_Estado",
            "estado",
        ),
        Index(
            "IX_Pago_MetodoPago",
            "metodoPago",
        ),
        Index(
            "IX_Pago_FechaLimitePago",
            "fechaLimitePago",
        ),
        Index(
            "IX_Pago_FechaPago",
            "fechaPago",
        ),
        CheckConstraint(
            "montoImpuesto >= 0",
            name="CK_Pago_MontoImpuesto",
        ),
        CheckConstraint(
            "montoSubtotal >= 0",
            name="CK_Pago_MontoSubtotal",
        ),
        CheckConstraint(
            "montoTotal >= 0",
            name="CK_Pago_MontoTotal",
        ),
        CheckConstraint(
            "tarifaPorHora >= 0",
            name="CK_Pago_TarifaPorHora",
        ),
        CheckConstraint(
            "tiempoCobradoMinutos > 0",
            name="CK_Pago_TiempoCobrado",
        ),
    )

    idPago: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    idOcupacion: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "ocupacion.idOcupacion",
            name="FK_Pago_Ocupacion",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    codigoPago: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    tiempoCobradoMinutos: Mapped[Optional[int]] = mapped_column(
        INTEGER(unsigned=True),
        nullable=True,
        server_default=text("1"),
    )

    tarifaPorHora: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(10, 2),
        nullable=True,
        server_default=text("'0.00'"),
    )

    montoSubtotal: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(10, 2),
        nullable=True,
        server_default=text("'0.00'"),
    )

    montoImpuesto: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2),
        nullable=False,
        server_default=text("'0.00'"),
    )

    montoTotal: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2),
        nullable=False,
    )

    metodoPago: Mapped[Optional[str]] = mapped_column(
        SqlEnum(
            "EFECTIVO",
            "TARJETA",
            "SINPE",
            "PASARELA",
        ),
        nullable=True,
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "PENDIENTE",
            "PAGADO",
            "RECHAZADO",
            "VENCIDO",
            "ANULADO",
        ),
        nullable=False,
        server_default=text("'PENDIENTE'"),
    )

    fechaGeneracion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    fechaLimitePago: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    fechaPago: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    referenciaTransaccion: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    numeroComprobante: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
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