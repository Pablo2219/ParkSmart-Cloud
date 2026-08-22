from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class NotificacionResponse(BaseModel):
    idNotificacion: int
    idCliente: int
    idReserva: Optional[int]
    idPago: Optional[int]
    idDeuda: Optional[int]
    tipoNotificacion: str
    canal: str
    titulo: str
    mensaje: str
    estado: str
    fechaEnvio: Optional[datetime]
    fechaLectura: Optional[datetime]
    fechaCreacion: datetime
    fechaActualizacion: datetime

    model_config = ConfigDict(from_attributes=True)