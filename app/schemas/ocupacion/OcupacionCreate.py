from typing import Optional

from pydantic import BaseModel, Field


class OcupacionCreate(BaseModel):
    idQr: int = Field(..., gt=0)
    observaciones: Optional[str] = Field(None, max_length=250)