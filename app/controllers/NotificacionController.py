from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.Session import get_db
from app.schemas.notificacion.NotificacionCreate import NotificacionCreate
from app.schemas.notificacion.NotificacionUpdate import NotificacionUpdate
from app.schemas.notificacion.NotificacionResponse import NotificacionResponse
from app.services.NotificacionService import NotificacionService


router = APIRouter(
    prefix="/notificaciones",
    tags=["Notificaciones"]
)


@router.get("/", response_model=List[NotificacionResponse])
def listar_notificaciones(db: Session = Depends(get_db)):
    service = NotificacionService(db)
    return service.listar_notificaciones()


@router.get("/pendientes", response_model=List[NotificacionResponse])
def listar_notificaciones_pendientes(db: Session = Depends(get_db)):
    service = NotificacionService(db)
    return service.listar_notificaciones_pendientes()


@router.get("/cliente/{idCliente}", response_model=List[NotificacionResponse])
def listar_notificaciones_por_cliente(
    idCliente: int,
    db: Session = Depends(get_db)
):
    service = NotificacionService(db)

    try:
        return service.listar_notificaciones_por_cliente(idCliente)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.get("/{idNotificacion}", response_model=NotificacionResponse)
def obtener_notificacion(
    idNotificacion: int,
    db: Session = Depends(get_db)
):
    service = NotificacionService(db)

    try:
        return service.obtener_notificacion(idNotificacion)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.post(
    "/",
    response_model=NotificacionResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_notificacion(
    datos: NotificacionCreate,
    db: Session = Depends(get_db)
):
    service = NotificacionService(db)

    try:
        return service.crear_notificacion(datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idNotificacion}", response_model=NotificacionResponse)
def actualizar_notificacion(
    idNotificacion: int,
    datos: NotificacionUpdate,
    db: Session = Depends(get_db)
):
    service = NotificacionService(db)

    try:
        return service.actualizar_notificacion(idNotificacion, datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idNotificacion}/enviar", response_model=NotificacionResponse)
def enviar_notificacion(
    idNotificacion: int,
    db: Session = Depends(get_db)
):
    service = NotificacionService(db)

    try:
        return service.enviar_notificacion(idNotificacion)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idNotificacion}/leer", response_model=NotificacionResponse)
def leer_notificacion(
    idNotificacion: int,
    db: Session = Depends(get_db)
):
    service = NotificacionService(db)

    try:
        return service.leer_notificacion(idNotificacion)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idNotificacion}/fallar", response_model=NotificacionResponse)
def fallar_notificacion(
    idNotificacion: int,
    db: Session = Depends(get_db)
):
    service = NotificacionService(db)

    try:
        return service.fallar_notificacion(idNotificacion)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.put("/{idNotificacion}/anular", response_model=NotificacionResponse)
def anular_notificacion(
    idNotificacion: int,
    db: Session = Depends(get_db)
):
    service = NotificacionService(db)

    try:
        return service.anular_notificacion(idNotificacion)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )