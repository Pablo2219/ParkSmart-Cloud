from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import DateTime, Enum as SqlEnum, Index, Numeric, String, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Proveedor(Base):
    __tablename__ = "proveedor"

    __table_args__ = (
        Index("UK_Proveedor_Identificacion", "identificacion", unique=True),
        Index("UK_Proveedor_CorreoElectronico", "correoElectronico", unique=True),
        Index("IX_Proveedor_Estado", "estado"),
    )

    idProveedor: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    identificacion: Mapped[str] = mapped_column(String(20), nullable=False)
    nombreComercial: Mapped[str] = mapped_column(String(120), nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)
    correoElectronico: Mapped[str] = mapped_column(String(120), nullable=False)
    direccion: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    latitud: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7), nullable=True)
    longitud: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7), nullable=True)
    estado: Mapped[str] = mapped_column(SqlEnum("ACTIVO", "INACTIVO", "SUSPENDIDO"), nullable=False, server_default=text("'ACTIVO'"))
    fechaCreacion: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    fechaActualizacion: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
