from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum as SqlEnum, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Sector(Base):
    __tablename__ = "sector"

    __table_args__ = (
        Index(
            "UK_Sector_NombreSector",
            "nombreSector",
            unique=True,
        ),
        Index(
            "IX_Sector_Estado",
            "estado",
        ),
    )

    idSector: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    nombreSector: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    descripcion: Mapped[Optional[str]] = mapped_column(
        String(250),
        nullable=True,
    )

    ubicacion: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "ACTIVO",
            "INACTIVO",
            "MANTENIMIENTO",
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