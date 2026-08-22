from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Index, Numeric, String, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.Base import Base


class Espacio(Base):
    __tablename__ = "espacio"

    __table_args__ = (
        Index("UK_Espacio_CodigoEspacio", "codigoEspacio", unique=True),
        Index("IX_Espacio_IdSector", "idSector"),
        Index("IX_Espacio_TipoEspacio", "tipoEspacio"),
        Index("IX_Espacio_Estado", "estado"),
    )

    idEspacio: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    idSector: Mapped[int] = mapped_column(BIGINT(unsigned=True), ForeignKey("sector.idSector", name="FK_Espacio_Sector", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    codigoEspacio: Mapped[str] = mapped_column(String(20), nullable=False)
    tipoEspacio: Mapped[str] = mapped_column(SqlEnum("REGULAR", "MOTOCICLETA", "DISCAPACIDAD", "ELECTRICO", "VIP"), nullable=False, server_default=text("'REGULAR'"))
    estado: Mapped[str] = mapped_column(SqlEnum("DISPONIBLE", "OCUPADO", "RESERVADO", "MANTENIMIENTO", "INACTIVO"), nullable=False, server_default=text("'DISPONIBLE'"))
    descripcion: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    latitud: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7), nullable=True)
    longitud: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 7), nullable=True)
    fechaCreacion: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    fechaActualizacion: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    sector = relationship("Sector", lazy="joined")
