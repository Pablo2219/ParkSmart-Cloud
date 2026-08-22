from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.Session import get_db
from app.schemas.reserva.ReservaCreate import ReservaCreate
from app.schemas.reserva.ReservaUpdate import ReservaUpdate
from app.schemas.reserva.ReservaResponse import ReservaResponse
from app.services.ReservaService import ReservaService


router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"]
)


@router.get("/", response_model=List[ReservaResponse])
def listar_reservas(db: Session = Depends(get_db)):
    service = ReservaService(db)
    return service.listar_reservas()


@router.get("/activas", response_model=List[ReservaResponse])
def listar_reservas_activas(db: Session = Depends(get_db)):
    service = ReservaService(db)
    return service.listar_reservas_activas()


@router.get("/cliente/{idCliente}", response_model=List[ReservaResponse])
def listar_reservas_por_cliente(
    idCliente: int,
    db: Session = Depends(get_db)
):
    service = ReservaService(db)

    try:
        return service.listar_reservas_por_cliente(idCliente)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.get("/{idReserva}", response_model=ReservaResponse)
def obtener_reserva(
    idReserva: int,
    db: Session = Depends(get_db)
):
    service = ReservaService(db)

    try:
        return service.obtener_reserva(idReserva)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.post(
    "/",
    response_model=ReservaResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_reserva(
    datos: ReservaCreate,
    db: Session = Depends(get_db)
):
    service = ReservaService(db)

    try:
        return service.crear_reserva(datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idReserva}", response_model=ReservaResponse)
def actualizar_reserva(
    idReserva: int,
    datos: ReservaUpdate,
    db: Session = Depends(get_db)
):
    service = ReservaService(db)

    try:
        return service.actualizar_reserva(idReserva, datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idReserva}/cancelar", response_model=ReservaResponse)
def cancelar_reserva(
    idReserva: int,
    db: Session = Depends(get_db)
):
    service = ReservaService(db)

    try:
        return service.cancelar_reserva(idReserva)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.delete("/{idReserva}", response_model=ReservaResponse)
def eliminar_reserva(
    idReserva: int,
    db: Session = Depends(get_db)
):
    service = ReservaService(db)

    try:
        return service.cancelar_reserva(idReserva)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )