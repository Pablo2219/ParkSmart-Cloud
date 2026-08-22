from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.Session import get_db
from app.schemas.espacio.EspacioCreate import EspacioCreate
from app.schemas.espacio.EspacioUpdate import EspacioUpdate
from app.schemas.espacio.EspacioResponse import EspacioResponse
from app.schemas.espacio.SectorResponse import SectorResponse
from app.services.EspacioService import EspacioService


router = APIRouter(
    prefix="/espacios",
    tags=["Espacios"]
)


@router.get("/sectores", response_model=List[SectorResponse])
def listar_sectores(db: Session = Depends(get_db)):
    service = EspacioService(db)
    return service.listar_sectores()


@router.get("/disponibles", response_model=List[EspacioResponse])
def listar_espacios_disponibles(db: Session = Depends(get_db)):
    service = EspacioService(db)
    return service.listar_espacios_disponibles()


@router.get("/", response_model=List[EspacioResponse])
def listar_espacios(db: Session = Depends(get_db)):
    service = EspacioService(db)
    return service.listar_espacios()


@router.get("/{idEspacio}", response_model=EspacioResponse)
def obtener_espacio(
    idEspacio: int,
    db: Session = Depends(get_db)
):
    service = EspacioService(db)

    try:
        return service.obtener_espacio(idEspacio)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.post(
    "/",
    response_model=EspacioResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_espacio(
    datos: EspacioCreate,
    db: Session = Depends(get_db)
):
    service = EspacioService(db)

    try:
        return service.crear_espacio(datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idEspacio}", response_model=EspacioResponse)
def actualizar_espacio(
    idEspacio: int,
    datos: EspacioUpdate,
    db: Session = Depends(get_db)
):
    service = EspacioService(db)

    try:
        return service.actualizar_espacio(idEspacio, datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.delete("/{idEspacio}", response_model=EspacioResponse)
def eliminar_espacio(
    idEspacio: int,
    db: Session = Depends(get_db)
):
    service = EspacioService(db)

    try:
        return service.eliminar_espacio(idEspacio)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )