from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.Session import get_db
from app.models.Usuario import Usuario
from app.schemas.reserva.ReservaCreate import ReservaCreate
from app.schemas.reserva.ReservaUpdate import ReservaUpdate
from app.schemas.reserva.ReservaResponse import ReservaResponse
from app.security.Dependencies import exigir_roles
from app.services.ReservaService import ReservaService

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.get("/", response_model=List[ReservaResponse])
def listar_reservas(usuario: Usuario = Depends(exigir_roles("ADMINISTRADOR")), db: Session = Depends(get_db)):
    return ReservaService(db).listar_reservas()


@router.get("/activas", response_model=List[ReservaResponse])
def listar_reservas_activas(usuario: Usuario = Depends(exigir_roles("ADMINISTRADOR")), db: Session = Depends(get_db)):
    return ReservaService(db).listar_reservas_activas()


@router.get("/mis-reservas", response_model=List[ReservaResponse])
def mis_reservas(usuario: Usuario = Depends(exigir_roles("CLIENTE")), db: Session = Depends(get_db)):
    if not usuario.idCliente:
        raise HTTPException(status_code=403, detail="La cuenta no tiene un cliente asociado.")
    return ReservaService(db).listar_reservas_por_cliente(usuario.idCliente)


@router.get("/cliente/{idCliente}", response_model=List[ReservaResponse])
def listar_reservas_por_cliente(idCliente: int, usuario: Usuario = Depends(exigir_roles("CLIENTE", "ADMINISTRADOR")), db: Session = Depends(get_db)):
    if usuario.rol.nombreRol == "CLIENTE" and usuario.idCliente != idCliente:
        raise HTTPException(status_code=403, detail="No puedes consultar las reservas de otro cliente.")
    try:
        return ReservaService(db).listar_reservas_por_cliente(idCliente)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get("/{idReserva}", response_model=ReservaResponse)
def obtener_reserva(idReserva: int, usuario: Usuario = Depends(exigir_roles("CLIENTE", "ADMINISTRADOR")), db: Session = Depends(get_db)):
    try:
        reserva = ReservaService(db).obtener_reserva(idReserva)
        if usuario.rol.nombreRol == "CLIENTE" and reserva.idCliente != usuario.idCliente:
            raise HTTPException(status_code=403, detail="No puedes consultar una reserva de otro cliente.")
        return reserva
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.post("/", response_model=ReservaResponse, status_code=201)
def crear_reserva(datos: ReservaCreate, usuario: Usuario = Depends(exigir_roles("CLIENTE")), db: Session = Depends(get_db)):
    if not usuario.idCliente or datos.idCliente != usuario.idCliente:
        raise HTTPException(status_code=403, detail="Solo puedes crear reservas para tu propia cuenta.")
    try:
        return ReservaService(db).crear_reserva(datos)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.put("/{idReserva}", response_model=ReservaResponse)
def actualizar_reserva(idReserva: int, datos: ReservaUpdate, usuario: Usuario = Depends(exigir_roles("CLIENTE", "ADMINISTRADOR")), db: Session = Depends(get_db)):
    service = ReservaService(db)
    try:
        reserva = service.obtener_reserva(idReserva)
        if usuario.rol.nombreRol == "CLIENTE" and reserva.idCliente != usuario.idCliente:
            raise HTTPException(status_code=403, detail="No puedes modificar una reserva de otro cliente.")
        return service.actualizar_reserva(idReserva, datos)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.put("/{idReserva}/cancelar", response_model=ReservaResponse)
def cancelar_reserva(idReserva: int, usuario: Usuario = Depends(exigir_roles("CLIENTE", "ADMINISTRADOR")), db: Session = Depends(get_db)):
    service = ReservaService(db)
    try:
        reserva = service.obtener_reserva(idReserva)
        if usuario.rol.nombreRol == "CLIENTE" and reserva.idCliente != usuario.idCliente:
            raise HTTPException(status_code=403, detail="No puedes cancelar una reserva de otro cliente.")
        return service.cancelar_reserva(idReserva)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.delete("/{idReserva}", response_model=ReservaResponse)
def eliminar_reserva(idReserva: int, usuario: Usuario = Depends(exigir_roles("CLIENTE", "ADMINISTRADOR")), db: Session = Depends(get_db)):
    return cancelar_reserva(idReserva, usuario, db)
