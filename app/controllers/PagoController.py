from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.Session import get_db
from app.schemas.pago.PagoCreate import PagoCreate
from app.schemas.pago.PagoUpdate import PagoUpdate
from app.schemas.pago.PagoResponse import PagoResponse
from app.services.PagoService import PagoService


router = APIRouter(
    prefix="/pagos",
    tags=["Pagos"]
)


@router.get("/", response_model=List[PagoResponse])
def listar_pagos(db: Session = Depends(get_db)):
    service = PagoService(db)
    return service.listar_pagos()


@router.get("/pendientes", response_model=List[PagoResponse])
def listar_pagos_pendientes(db: Session = Depends(get_db)):
    service = PagoService(db)
    return service.listar_pagos_pendientes()


@router.get("/ocupacion/{idOcupacion}", response_model=List[PagoResponse])
def listar_pagos_por_ocupacion(
    idOcupacion: int,
    db: Session = Depends(get_db)
):
    service = PagoService(db)

    try:
        return service.listar_pagos_por_ocupacion(idOcupacion)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.get("/{idPago}", response_model=PagoResponse)
def obtener_pago(
    idPago: int,
    db: Session = Depends(get_db)
):
    service = PagoService(db)

    try:
        return service.obtener_pago(idPago)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.post(
    "/",
    response_model=PagoResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_pago(
    datos: PagoCreate,
    db: Session = Depends(get_db)
):
    service = PagoService(db)

    try:
        return service.crear_pago(datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idPago}", response_model=PagoResponse)
def actualizar_pago(
    idPago: int,
    datos: PagoUpdate,
    db: Session = Depends(get_db)
):
    service = PagoService(db)

    try:
        return service.actualizar_pago(idPago, datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idPago}/confirmar", response_model=PagoResponse)
def confirmar_pago(
    idPago: int,
    datos: PagoUpdate,
    db: Session = Depends(get_db)
):
    service = PagoService(db)

    try:
        return service.confirmar_pago(idPago, datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idPago}/anular", response_model=PagoResponse)
def anular_pago(
    idPago: int,
    db: Session = Depends(get_db)
):
    service = PagoService(db)

    try:
        return service.anular_pago(idPago)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )