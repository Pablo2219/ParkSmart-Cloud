from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.Session import get_db
from app.schemas.deuda.DeudaCreate import DeudaCreate
from app.schemas.deuda.DeudaUpdate import DeudaUpdate
from app.schemas.deuda.DeudaResponse import DeudaResponse
from app.services.DeudaService import DeudaService


router = APIRouter(
    prefix="/deudas",
    tags=["Deudas"]
)


@router.get("/", response_model=List[DeudaResponse])
def listar_deudas(db: Session = Depends(get_db)):
    service = DeudaService(db)
    return service.listar_deudas()


@router.get("/pendientes", response_model=List[DeudaResponse])
def listar_deudas_pendientes(db: Session = Depends(get_db)):
    service = DeudaService(db)
    return service.listar_deudas_pendientes()


@router.get("/vencidas", response_model=List[DeudaResponse])
def listar_deudas_vencidas(db: Session = Depends(get_db)):
    service = DeudaService(db)
    return service.listar_deudas_vencidas()


@router.get("/pago/{idPago}", response_model=List[DeudaResponse])
def listar_deudas_por_pago(
    idPago: int,
    db: Session = Depends(get_db)
):
    service = DeudaService(db)

    try:
        return service.listar_deudas_por_pago(idPago)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.get("/{idDeuda}", response_model=DeudaResponse)
def obtener_deuda(
    idDeuda: int,
    db: Session = Depends(get_db)
):
    service = DeudaService(db)

    try:
        return service.obtener_deuda(idDeuda)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.post(
    "/",
    response_model=DeudaResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_deuda(
    datos: DeudaCreate,
    db: Session = Depends(get_db)
):
    service = DeudaService(db)

    try:
        return service.crear_deuda(datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idDeuda}", response_model=DeudaResponse)
def actualizar_deuda(
    idDeuda: int,
    datos: DeudaUpdate,
    db: Session = Depends(get_db)
):
    service = DeudaService(db)

    try:
        return service.actualizar_deuda(idDeuda, datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idDeuda}/pagar", response_model=DeudaResponse)
def pagar_deuda(
    idDeuda: int,
    db: Session = Depends(get_db)
):
    service = DeudaService(db)

    try:
        return service.pagar_deuda(idDeuda)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idDeuda}/vencer", response_model=DeudaResponse)
def vencer_deuda(
    idDeuda: int,
    db: Session = Depends(get_db)
):
    service = DeudaService(db)

    try:
        return service.vencer_deuda(idDeuda)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idDeuda}/anular", response_model=DeudaResponse)
def anular_deuda(
    idDeuda: int,
    db: Session = Depends(get_db)
):
    service = DeudaService(db)

    try:
        return service.anular_deuda(idDeuda)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )