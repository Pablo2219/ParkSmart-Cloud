from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.Base import Base


class Usuario(Base):
    __tablename__ = "usuario"

    __table_args__ = (
        Index(
            "UK_Usuario_NombreUsuario",
            "nombreUsuario",
            unique=True,
        ),
        Index(
            "UK_Usuario_CorreoElectronico",
            "correoElectronico",
            unique=True,
        ),
        Index(
            "IX_Usuario_Estado",
            "estado",
        ),
        Index(
            "IX_Usuario_UltimoAcceso",
            "ultimoAcceso",
        ),
        Index(
            "IX_Usuario_IdRol",
            "idRol",
        ),
        Index(
            "IX_Usuario_IdCliente",
            "idCliente",
        ),
    )

    idUsuario: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    idRol: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "rol.idRol",
            name="FK_Usuario_Rol",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    idCliente: Mapped[Optional[int]] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "cliente.idCliente",
            name="FK_Usuario_Cliente",
            ondelete="SET NULL",
            onupdate="CASCADE",
        ),
        nullable=True,
    )

    nombreUsuario: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    correoElectronico: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    contrasenaHash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "ACTIVO",
            "INACTIVO",
            "BLOQUEADO",
        ),
        nullable=False,
        server_default=text("'ACTIVO'"),
    )

    ultimoAcceso: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    fechaCreacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )


    rol = relationship("Rol", lazy="joined")

    fechaActualizacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text(
            "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
        ),
    )