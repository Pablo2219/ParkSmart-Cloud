from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.Session import get_db
from app.schemas.vehiculo.VehiculoCreate import VehiculoCreate
from app.schemas.vehiculo.VehiculoUpdate import VehiculoUpdate
from app.schemas.vehiculo.VehiculoResponse import VehiculoResponse
from app.services.VehiculoService import VehiculoService


router = APIRouter(
    prefix="/vehiculos",
    tags=["Vehiculos"]
)


@router.get("/", response_model=List[VehiculoResponse])
def listar_vehiculos(db: Session = Depends(get_db)):
    service = VehiculoService(db)
    return service.listar_vehiculos()


@router.get("/cliente/{idCliente}", response_model=List[VehiculoResponse])
def listar_vehiculos_por_cliente(
    idCliente: int,
    db: Session = Depends(get_db)
):
    service = VehiculoService(db)

    try:
        return service.listar_vehiculos_por_cliente(idCliente)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.get("/{idVehiculo}", response_model=VehiculoResponse)
def obtener_vehiculo(
    idVehiculo: int,
    db: Session = Depends(get_db)
):
    service = VehiculoService(db)

    try:
        return service.obtener_vehiculo(idVehiculo)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.post(
    "/",
    response_model=VehiculoResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_vehiculo(
    datos: VehiculoCreate,
    db: Session = Depends(get_db)
):
    service = VehiculoService(db)

    try:
        return service.crear_vehiculo(datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idVehiculo}", response_model=VehiculoResponse)
def actualizar_vehiculo(
    idVehiculo: int,
    datos: VehiculoUpdate,
    db: Session = Depends(get_db)
):
    service = VehiculoService(db)

    try:
        return service.actualizar_vehiculo(idVehiculo, datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.delete("/{idVehiculo}", response_model=VehiculoResponse)
def eliminar_vehiculo(
    idVehiculo: int,
    db: Session = Depends(get_db)
):
    service = VehiculoService(db)

    try:
        return service.eliminar_vehiculo(idVehiculo)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )