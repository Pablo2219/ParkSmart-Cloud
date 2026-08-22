from typing import List
from app.schemas.ocupacion.FinalizarOcupacionRequest import FinalizarOcupacionRequest
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.Session import get_db
from app.schemas.ocupacion.OcupacionCreate import OcupacionCreate
from app.schemas.ocupacion.OcupacionUpdate import OcupacionUpdate
from app.schemas.ocupacion.OcupacionResponse import OcupacionResponse
from app.services.OcupacionService import OcupacionService


router = APIRouter(
    prefix="/ocupaciones",
    tags=["Ocupaciones"]
)


@router.get("/", response_model=List[OcupacionResponse])
def listar_ocupaciones(db: Session = Depends(get_db)):
    service = OcupacionService(db)
    return service.listar_ocupaciones()


@router.get("/activas", response_model=List[OcupacionResponse])
def listar_ocupaciones_activas(db: Session = Depends(get_db)):
    service = OcupacionService(db)
    return service.listar_ocupaciones_activas()


@router.get("/reserva/{idReserva}", response_model=List[OcupacionResponse])
def listar_ocupaciones_por_reserva(
    idReserva: int,
    db: Session = Depends(get_db)
):
    service = OcupacionService(db)

    try:
        return service.listar_ocupaciones_por_reserva(idReserva)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.get("/{idOcupacion}", response_model=OcupacionResponse)
def obtener_ocupacion(
    idOcupacion: int,
    db: Session = Depends(get_db)
):
    service = OcupacionService(db)

    try:
        return service.obtener_ocupacion(idOcupacion)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.post(
    "/",
    response_model=OcupacionResponse,
    status_code=status.HTTP_201_CREATED
)
def iniciar_ocupacion(
    datos: OcupacionCreate,
    db: Session = Depends(get_db)
):
    service = OcupacionService(db)

    try:
        return service.iniciar_ocupacion(datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idOcupacion}", response_model=OcupacionResponse)
def actualizar_ocupacion(
    idOcupacion: int,
    datos: OcupacionUpdate,
    db: Session = Depends(get_db)
):
    service = OcupacionService(db)

    try:
        return service.actualizar_ocupacion(idOcupacion, datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idOcupacion}/finalizar", response_model=OcupacionResponse)
def finalizar_ocupacion(
    idOcupacion: int,
    datos: FinalizarOcupacionRequest,
    db: Session = Depends(get_db)
):
    service = OcupacionService(db)

    try:
        return service.finalizar_ocupacion(
            idOcupacion,
            datos
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idOcupacion}/cancelar", response_model=OcupacionResponse)
def cancelar_ocupacion(
    idOcupacion: int,
    db: Session = Depends(get_db)
):
    service = OcupacionService(db)

    try:
        return service.cancelar_ocupacion(idOcupacion)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )