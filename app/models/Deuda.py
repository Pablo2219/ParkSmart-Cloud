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
from sqlalchemy.dialects.mysql import BIGINT, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Deuda(Base):
    __tablename__ = "deuda"

    __table_args__ = (
        Index(
            "UK_Deuda_CodigoDeuda",
            "codigoDeuda",
            unique=True,
        ),
        Index(
            "UK_Deuda_IdPago",
            "idPago",
            unique=True,
        ),
        Index(
            "IX_Deuda_Estado",
            "estado",
        ),
        Index(
            "IX_Deuda_FechaLimite",
            "fechaLimite",
        ),
        CheckConstraint(
            "montoDeuda >= 0",
            name="CK_Deuda_Monto",
        ),
    )

    idDeuda: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    idPago: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "pago.idPago",
            name="FK_Deuda_Pago",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    codigoDeuda: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    montoDeuda: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2),
        nullable=False,
    )

    fechaGeneracion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    fechaLimite: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "PENDIENTE",
            "PAGADA",
            "VENCIDA",
            "ANULADA",
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