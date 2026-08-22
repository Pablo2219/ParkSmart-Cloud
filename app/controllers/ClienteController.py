from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.Session import get_db
from app.schemas.cliente.ClienteCreate import ClienteCreate
from app.schemas.cliente.ClienteUpdate import ClienteUpdate
from app.schemas.cliente.ClienteResponse import ClienteResponse
from app.services.ClienteService import ClienteService

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    service = ClienteService(db)
    return service.listar_clientes()

@router.get("/{idCliente}", response_model=ClienteResponse)
def obtener_cliente(
    idCliente: int,
    db: Session = Depends(get_db)
):
    service = ClienteService(db)
    try:
        return service.obtener_cliente(idCliente)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )

@router.post(
    "/",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_cliente(
    datos: ClienteCreate,
    db: Session = Depends(get_db)
):
    service = ClienteService(db)
    try:
        return service.crear_cliente(datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

@router.put("/{idCliente}", response_model=ClienteResponse)
def actualizar_cliente(
    idCliente: int,
    datos: ClienteUpdate,
    db: Session = Depends(get_db)
):
    service = ClienteService(db)
    try:
        return service.actualizar_cliente(idCliente, datos)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

@router.delete("/{idCliente}", response_model=ClienteResponse)
def eliminar_cliente(
    idCliente: int,
    db: Session = Depends(get_db)
):
    service = ClienteService(db)
    try:
        return service.eliminar_cliente(idCliente)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )