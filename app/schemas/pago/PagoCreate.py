from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class PagoCreate(BaseModel):
    idOcupacion: int = Field(..., gt=0)
    montoTotal: Decimal = Field(..., gt=0)
    observaciones: Optional[str] = Field(None, max_length=250)