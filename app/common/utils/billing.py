import math
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional


DOS_DECIMALES = Decimal("0.01")


def _redondear_moneda(valor: Decimal) -> Decimal:
    return valor.quantize(DOS_DECIMALES, rounding=ROUND_HALF_UP)


def calcular_horas_cobro(minutos: Optional[int]) -> int:
    if minutos is None or minutos == 0:
        return 0

    return math.ceil(minutos / 60)


def calcular_impuesto(
    monto_subtotal: Decimal,
    porcentaje_impuesto: Decimal,
) -> Decimal:
    impuesto = monto_subtotal * (porcentaje_impuesto / Decimal("100"))
    return _redondear_moneda(impuesto)


def calcular_subtotal_pago(
    tiempo_minutos: int,
    tarifa_por_hora: Decimal,
) -> Decimal:
    horas = calcular_horas_cobro(tiempo_minutos)
    subtotal = Decimal(horas) * tarifa_por_hora

    return _redondear_moneda(subtotal)


def calcular_tiempo_ocupacion(
    fecha_entrada: datetime,
    fecha_salida: Optional[datetime] = None,
) -> int:
    salida = fecha_salida or datetime.now()

    diferencia = salida - fecha_entrada

    return int(diferencia.total_seconds() // 60)


def calcular_total_pago(
    monto_subtotal: Decimal,
    monto_impuesto: Decimal,
) -> Decimal:
    total = monto_subtotal + monto_impuesto

    return _redondear_moneda(total)