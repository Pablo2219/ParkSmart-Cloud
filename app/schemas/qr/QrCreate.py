from pydantic import BaseModel, Field


class QrCreate(BaseModel):
    idReserva: int = Field(..., gt=0)