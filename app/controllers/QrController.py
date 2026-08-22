from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.Session import get_db
from app.schemas.qr.QrCreate import QrCreate
from app.schemas.qr.QrResponse import QrResponse
from app.services.QrService import QrService


router = APIRouter(
    prefix="/qrs",
    tags=["QR"]
)


@router.get("/", response_model=List[QrResponse])
def listar_qrs(db: Session = Depends(get_db)):
    service = QrService(db)
    return service.listar_qrs()


@router.get("/reserva/{idReserva}", response_model=List[QrResponse])
def listar_qrs_por_reserva(
    idReserva: int,
    db: Session = Depends(get_db)
):
    service = QrService(db)

    try:
        return service.listar_qrs_por_reserva(idReserva)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.get("/codigo/{codigoQr}", response_model=QrResponse)
def obtener_qr_por_codigo(
    codigoQr: str,
    db: Session = Depends(get_db)
):
    service = QrService(db)

    try:
        return service.obtener_qr_por_codigo(codigoQr)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.post(
    "/",
    response_model=QrResponse,
    status_code=status.HTTP_201_CREATED
)
def generar_qr(
    datos: QrCreate,
    db: Session = Depends(get_db)
):
    service = QrService(db)

    try:
        return service.generar_qr(datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/codigo/{codigoQr}/usar", response_model=QrResponse)
def usar_qr(
    codigoQr: str,
    db: Session = Depends(get_db)
):
    service = QrService(db)

    try:
        return service.usar_qr(codigoQr)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idQr}/activar", response_model=QrResponse)
def activar_qr(
    idQr: int,
    db: Session = Depends(get_db)
):
    service = QrService(db)

    try:
        return service.activar_qr(idQr)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idQr}/anular", response_model=QrResponse)
def anular_qr(
    idQr: int,
    db: Session = Depends(get_db)
):
    service = QrService(db)

    try:
        return service.anular_qr(idQr)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.get("/{idQr}", response_model=QrResponse)
def obtener_qr(
    idQr: int,
    db: Session = Depends(get_db)
):
    service = QrService(db)

    try:
        return service.obtener_qr(idQr)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )