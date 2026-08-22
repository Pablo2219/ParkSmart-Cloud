from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.Session import get_db
from app.models.Espacio import Espacio
from app.models.Reserva import Reserva
from app.models.Sector import Sector
from app.models.Usuario import Usuario
from app.schemas.proveedor.ProviderSectorCreate import ProviderSectorCreate
from app.schemas.proveedor.ProviderSpaceCreate import ProviderSpaceCreate
from app.security.Dependencies import exigir_roles

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


def _proveedor_id(usuario: Usuario) -> int:
    if not usuario.idProveedor:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="La cuenta no tiene un proveedor asociado.")
    return usuario.idProveedor


@router.get("/mi-catalogo")
def mi_catalogo(usuario: Usuario = Depends(exigir_roles("PROVEEDOR")), db: Session = Depends(get_db)):
    proveedor_id = _proveedor_id(usuario)
    sectores = db.scalars(select(Sector).where(Sector.idProveedor == proveedor_id)).all()
    espacios = db.scalars(
        select(Espacio).join(Sector, Espacio.idSector == Sector.idSector).where(Sector.idProveedor == proveedor_id)
    ).all()
    return {
        "sectores": [
            {
                "idSector": s.idSector,
                "nombreSector": s.nombreSector,
                "descripcion": s.descripcion,
                "ubicacion": s.ubicacion,
                "latitud": s.latitud,
                "longitud": s.longitud,
                "estado": s.estado,
            } for s in sectores
        ],
        "espacios": [
            {
                "idEspacio": e.idEspacio,
                "idSector": e.idSector,
                "codigoEspacio": e.codigoEspacio,
                "tipoEspacio": e.tipoEspacio,
                "estado": e.estado,
                "descripcion": e.descripcion,
                "latitud": e.latitud,
                "longitud": e.longitud,
            } for e in espacios
        ],
    }


@router.post("/sectores", status_code=status.HTTP_201_CREATED)
def crear_sector(datos: ProviderSectorCreate, usuario: Usuario = Depends(exigir_roles("PROVEEDOR")), db: Session = Depends(get_db)):
    proveedor_id = _proveedor_id(usuario)
    sector = Sector(
        idProveedor=proveedor_id,
        nombreSector=datos.nombreSector.strip(),
        descripcion=datos.descripcion,
        ubicacion=datos.ubicacion,
        latitud=datos.latitud,
        longitud=datos.longitud,
        estado="ACTIVO",
    )
    db.add(sector)
    try:
        db.commit()
        db.refresh(sector)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=409, detail="No se pudo crear el sector. Verifica que el nombre no esté en uso.")
    return sector


@router.post("/espacios", status_code=status.HTTP_201_CREATED)
def crear_espacio(datos: ProviderSpaceCreate, usuario: Usuario = Depends(exigir_roles("PROVEEDOR")), db: Session = Depends(get_db)):
    proveedor_id = _proveedor_id(usuario)
    sector = db.scalar(select(Sector).where(Sector.idSector == datos.idSector, Sector.idProveedor == proveedor_id))
    if sector is None:
        raise HTTPException(status_code=404, detail="El sector no pertenece al proveedor.")

    espacio = Espacio(
        idSector=datos.idSector,
        codigoEspacio=datos.codigoEspacio.strip().upper(),
        tipoEspacio=datos.tipoEspacio,
        descripcion=datos.descripcion,
        latitud=datos.latitud,
        longitud=datos.longitud,
        estado="DISPONIBLE",
    )
    db.add(espacio)
    try:
        db.commit()
        db.refresh(espacio)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=409, detail="No se pudo crear el espacio. El código puede estar en uso.")
    return espacio


@router.get("/reservas")
def reservas_del_proveedor(usuario: Usuario = Depends(exigir_roles("PROVEEDOR")), db: Session = Depends(get_db)):
    proveedor_id = _proveedor_id(usuario)
    filas = db.execute(
        select(Reserva, Espacio, Sector)
        .join(Espacio, Reserva.idEspacio == Espacio.idEspacio)
        .join(Sector, Espacio.idSector == Sector.idSector)
        .where(Sector.idProveedor == proveedor_id)
        .order_by(Reserva.fechaInicioReserva.desc())
    ).all()

    return [
        {
            "idReserva": reserva.idReserva,
            "codigoReserva": reserva.codigoReserva,
            "estado": reserva.estado,
            "fechaInicioReserva": reserva.fechaInicioReserva,
            "fechaFinReserva": reserva.fechaFinReserva,
            "idCliente": reserva.idCliente,
            "idEspacio": espacio.idEspacio,
            "codigoEspacio": espacio.codigoEspacio,
            "nombreSector": sector.nombreSector,
        }
        for reserva, espacio, sector in filas
    ]
