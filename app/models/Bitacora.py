from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Bitacora(Base):
    __tablename__ = "bitacora"

    __table_args__ = (
        Index(
            "IX_Bitacora_Modulo",
            "modulo",
        ),
        Index(
            "IX_Bitacora_Accion",
            "accion",
        ),
        Index(
            "IX_Bitacora_Resultado",
            "resultado",
        ),
        Index(
            "IX_Bitacora_FechaRegistro",
            "fechaRegistro",
        ),
        Index(
            "IX_Bitacora_IdUsuario",
            "idUsuario",
        ),
    )

    idBitacora: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    idUsuario: Mapped[Optional[int]] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "usuario.idUsuario",
            name="FK_Bitacora_Usuario",
            ondelete="SET NULL",
            onupdate="CASCADE",
        ),
        nullable=True,
    )

    modulo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    accion: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    descripcion: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )

    resultado: Mapped[str] = mapped_column(
        SqlEnum(
            "EXITOSO",
            "FALLIDO",
            "ADVERTENCIA",
        ),
        nullable=False,
        server_default=text("'EXITOSO'"),
    )

    direccionIp: Mapped[Optional[str]] = mapped_column(
        String(45),
        nullable=True,
    )

    userAgent: Mapped[Optional[str]] = mapped_column(
        String(250),
        nullable=True,
    )

    fechaRegistro: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )