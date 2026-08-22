from decimal import Decimal

from pydantic import BaseModel, Field


class FinalizarOcupacionRequest(BaseModel):
    tarifaPorHora: Decimal = Field(
        ...,
        gt=0,
        decimal_places=2
    )

    porcentajeImpuesto: Decimal = Field(
        ...,
        ge=0,
        le=100,
        decimal_places=2
    )