from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from app.database.Base import Base


class Notificacion(Base):
    __tablename__ = "notificacion"

    __table_args__ = (
        Index(
            "FK_Notificacion_Reserva",
            "idReserva",
        ),
        Index(
            "FK_Notificacion_Pago",
            "idPago",
        ),
        Index(
            "IX_Notificacion_Estado",
            "estado",
        ),
        Index(
            "IX_Notificacion_Tipo",
            "tipoNotificacion",
        ),
        Index(
            "IX_Notificacion_Canal",
            "canal",
        ),
        Index(
            "IX_Notificacion_FechaEnvio",
            "fechaEnvio",
        ),
        Index(
            "IX_Notificacion_IdCliente",
            "idCliente",
        ),
    )

    idNotificacion: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    idCliente: Mapped[int] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "cliente.idCliente",
            name="FK_Notificacion_Cliente",
            ondelete="RESTRICT",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    idReserva: Mapped[Optional[int]] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "reserva.idReserva",
            name="FK_Notificacion_Reserva",
            ondelete="SET NULL",
            onupdate="CASCADE",
        ),
        nullable=True,
    )

    idPago: Mapped[Optional[int]] = mapped_column(
        BIGINT(unsigned=True),
        ForeignKey(
            "pago.idPago",
            name="FK_Notificacion_Pago",
            ondelete="SET NULL",
            onupdate="CASCADE",
        ),
        nullable=True,
    )

    idDeuda: Mapped[Optional[int]] = mapped_column(
        BIGINT(unsigned=True),
        nullable=True,
    )

    tipoNotificacion: Mapped[str] = mapped_column(
        SqlEnum(
            "RESERVA",
            "PAGO",
            "DEUDA",
            "SISTEMA",
        ),
        nullable=False,
    )

    canal: Mapped[str] = mapped_column(
        SqlEnum(
            "EMAIL",
            "SMS",
            "WHATSAPP",
            "PUSH",
        ),
        nullable=False,
        server_default=text("'EMAIL'"),
    )

    titulo: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    mensaje: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    destinatario: Mapped[Optional[str]] = mapped_column(
        String(150),
        nullable=True,
    )

    estado: Mapped[str] = mapped_column(
        SqlEnum(
            "PENDIENTE",
            "ENVIADA",
            "LEIDA",
            "ERROR",
        ),
        nullable=False,
        server_default=text("'PENDIENTE'"),
    )

    fechaEnvio: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    fechaLectura: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
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