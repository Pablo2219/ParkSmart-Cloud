from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Vehiculo(Base):
    __tablename__ = "vehiculo"

    __table_args__ = (
        Index(
            "UK_Vehiculo_Placa",
            "placa",
            unique=True,
        ),
        Index(
            "IX_Vehiculo_IdCliente",
            "idCliente",
        ),
        Index(
            "IX_Vehiculo_TipoVehiculo",
            "tipoVehiculo",
        ),
        Index(
            "IX_Vehiculo_Estado",
            "estado",
        ),
    )

    idVehiculo: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    idCliente: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "cliente.idCliente",
            name="FK_Vehiculo_Cliente",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    placa: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    marca: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    modelo: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    color: Mapped[Optional[str]] = mapped_column(
        String(30),
        nullable=True,
    )

    tipoVehiculo: Mapped[str] = mapped_column(
        SqlEnum(
            "AUTOMOVIL",
            "MOTOCICLETA",
            "CAMIONETA",
            "OTRO",
        ),
        nullable=False,
        server_default=text("'AUTOMOVIL'"),
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "ACTIVO",
            "INACTIVO",
        ),
        nullable=False,
        server_default=text("'ACTIVO'"),
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