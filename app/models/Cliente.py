from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum as SqlEnum, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Cliente(Base):
    __tablename__ = "cliente"

    __table_args__ = (
        Index(
            "UK_Cliente_Identificacion",
            "identificacion",
            unique=True,
        ),
        Index(
            "UK_Cliente_CorreoElectronico",
            "correoElectronico",
            unique=True,
        ),
        Index(
            "IX_Cliente_PrimerApellido",
            "primerApellido",
        ),
        Index(
            "IX_Cliente_Telefono",
            "telefono",
        ),
    )

    idCliente: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    identificacion: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    nombre: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    primerApellido: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    segundoApellido: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    telefono: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    correoElectronico: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    direccion: Mapped[Optional[str]] = mapped_column(
        String(250),
        nullable=True,
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "ACTIVO",
            "INACTIVO",
            "SUSPENDIDO",
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

    provincia: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    canton: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    distrito: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    direccionExacta: Mapped[Optional[str]] = mapped_column(
        String(250),
        nullable=True,
    )