from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum as SqlEnum, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Rol(Base):
    __tablename__ = "rol"

    __table_args__ = (
        Index(
            "UK_Rol_NombreRol",
            "nombreRol",
            unique=True,
        ),
        Index(
            "IX_Rol_Estado",
            "estado",
        ),
    )

    idRol: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    nombreRol: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    descripcion: Mapped[Optional[str]] = mapped_column(
        String(250),
        nullable=True,
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