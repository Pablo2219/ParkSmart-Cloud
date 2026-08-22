from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.Session import get_db
from app.models.Espacio import Espacio
from app.models.Ocupacion import Ocupacion
from app.models.Pago import Pago
from app.models.Proveedor import Proveedor
from app.models.Reserva import Reserva
from app.models.Sector import Sector
from app.models.Usuario import Usuario
from app.schemas.proveedor.ProviderParkingCreate import ProviderParkingCreate, ProviderProfileUpdate
from app.schemas.proveedor.ProviderSectorCreate import ProviderSectorCreate
from app.schemas.proveedor.ProviderSpaceCreate import ProviderSpaceCreate
from app.security.Dependencies import exigir_roles

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


def _proveedor_id(usuario: Usuario) -> int:
    if not usuario.idProveedor:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="La cuenta no tiene un proveedor asociado.")
    return usuario.idProveedor


def _catalogo(db: Session, proveedor_id: int):
    sectores = db.scalars(select(Sector).where(Sector.idProveedor == proveedor_id, Sector.estado == "ACTIVO").order_by(Sector.nombreSector)).all()
    espacios = db.scalars(
        select(Espacio)
        .join(Sector, Espacio.idSector == Sector.idSector)
        .where(Sector.idProveedor == proveedor_id, Sector.estado == "ACTIVO", Espacio.estado != "INACTIVO")
        .order_by(Espacio.codigoEspacio)
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


@router.get("/perfil")
def perfil_proveedor(usuario: Usuario = Depends(exigir_roles("PROVEEDOR")), db: Session = Depends(get_db)):
    proveedor = db.get(Proveedor, _proveedor_id(usuario))
    if proveedor is None:
        raise HTTPException(status_code=404, detail="No se encontró el perfil del proveedor.")
    return {
        "idProveedor": proveedor.idProveedor,
        "identificacion": proveedor.identificacion,
        "nombreComercial": proveedor.nombreComercial,
        "telefono": proveedor.telefono,
        "correoElectronico": proveedor.correoElectronico,
        "direccion": proveedor.direccion,
        "latitud": proveedor.latitud,
        "longitud": proveedor.longitud,
        "estado": proveedor.estado,
    }


@router.put("/perfil")
def actualizar_perfil_proveedor(datos: ProviderProfileUpdate, usuario: Usuario = Depends(exigir_roles("PROVEEDOR")), db: Session = Depends(get_db)):
    proveedor = db.get(Proveedor, _proveedor_id(usuario))
    if proveedor is None:
        raise HTTPException(status_code=404, detail="No se encontró el perfil del proveedor.")
    proveedor.nombreComercial = datos.nombreComercial.strip()
    proveedor.telefono = datos.telefono.strip()
    proveedor.correoElectronico = datos.correoElectronico.strip().lower()
    proveedor.direccion = datos.direccion.strip() if datos.direccion else None
    proveedor.latitud = datos.latitud
    proveedor.longitud = datos.longitud
    try:
        db.commit()
        db.refresh(proveedor)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=409, detail="No se pudo actualizar el perfil. Verificá que el correo no esté registrado por otro proveedor.")
    return {"mensaje": "Perfil actualizado correctamente.", "proveedor": proveedor}


@router.get("/mi-catalogo")
def mi_catalogo(usuario: Usuario = Depends(exigir_roles("PROVEEDOR")), db: Session = Depends(get_db)):
    return _catalogo(db, _proveedor_id(usuario))


@router.post("/parqueos", status_code=status.HTTP_201_CREATED)
def crear_parqueo_con_espacios(datos: ProviderParkingCreate, usuario: Usuario = Depends(exigir_roles("PROVEEDOR")), db: Session = Depends(get_db)):
    proveedor_id = _proveedor_id(usuario)
    nombre_sector = datos.nombreSector.strip()
    if db.scalar(select(Sector.idSector).where(Sector.idProveedor == proveedor_id, Sector.nombreSector == nombre_sector)) is not None:
        raise HTTPException(status_code=409, detail="Ya existe un sector con ese nombre en tu oferta.")

    codigos = [espacio.codigoEspacio.strip().upper() for espacio in datos.espacios]
    if len(codigos) != len(set(codigos)):
        raise HTTPException(status_code=409, detail="No podés repetir códigos de espacios dentro del mismo parqueo.")
    if codigos and db.scalar(select(Espacio.idEspacio).where(Espacio.codigoEspacio.in_(codigos))) is not None:
        raise HTTPException(status_code=409, detail="Uno de los códigos de espacio ya existe en ParkSmart.")

    sector = Sector(
        idProveedor=proveedor_id,
        nombreSector=nombre_sector,
        descripcion=datos.descripcion,
        ubicacion=datos.ubicacion,
        latitud=datos.latitud,
        longitud=datos.longitud,
        estado="ACTIVO",
    )
    db.add(sector)
    db.flush()

    espacios = []
    for item in datos.espacios:
        espacio = Espacio(
            idSector=sector.idSector,
            codigoEspacio=item.codigoEspacio.strip().upper(),
            tipoEspacio=item.tipoEspacio,
            descripcion=item.descripcion,
            latitud=item.latitud,
            longitud=item.longitud,
            estado="DISPONIBLE",
        )
        db.add(espacio)
        espacios.append(espacio)

    try:
        db.commit()
        db.refresh(sector)
        for espacio in espacios:
            db.refresh(espacio)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=409, detail="No se pudo registrar el parqueo completo. No se guardaron cambios parciales.")

    return {"mensaje": "Parqueo registrado correctamente.", "sector": sector, "espacios": espacios, "catalogo": _catalogo(db, proveedor_id)}


@router.post("/sectores", status_code=status.HTTP_201_CREATED)
def crear_sector(datos: ProviderSectorCreate, usuario: Usuario = Depends(exigir_roles("PROVEEDOR")), db: Session = Depends(get_db)):
    proveedor_id = _proveedor_id(usuario)
    if db.scalar(select(Sector.idSector).where(Sector.idProveedor == proveedor_id, Sector.nombreSector == datos.nombreSector.strip())) is not None:
        raise HTTPException(status_code=409, detail="Ya existe un sector con ese nombre en tu oferta.")
    sector = Sector(idProveedor=proveedor_id, nombreSector=datos.nombreSector.strip(), descripcion=datos.descripcion, ubicacion=datos.ubicacion, latitud=datos.latitud, longitud=datos.longitud, estado="ACTIVO")
    db.add(sector)
    try:
        db.commit()
        db.refresh(sector)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=409, detail="No se pudo crear el sector.")
    return sector


@router.post("/espacios", status_code=status.HTTP_201_CREATED)
def crear_espacio(datos: ProviderSpaceCreate, usuario: Usuario = Depends(exigir_roles("PROVEEDOR")), db: Session = Depends(get_db)):
    proveedor_id = _proveedor_id(usuario)
    sector = db.scalar(select(Sector).where(Sector.idSector == datos.idSector, Sector.idProveedor == proveedor_id, Sector.estado == "ACTIVO"))
    if sector is None:
        raise HTTPException(status_code=404, detail="El sector no pertenece al proveedor.")
    if db.scalar(select(Espacio.idEspacio).where(Espacio.codigoEspacio == datos.codigoEspacio.strip().upper())) is not None:
        raise HTTPException(status_code=409, detail="El código del espacio ya existe.")
    espacio = Espacio(idSector=datos.idSector, codigoEspacio=datos.codigoEspacio.strip().upper(), tipoEspacio=datos.tipoEspacio, descripcion=datos.descripcion, latitud=datos.latitud, longitud=datos.longitud, estado="DISPONIBLE")
    db.add(espacio)
    try:
        db.commit()
        db.refresh(espacio)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=409, detail="No se pudo crear el espacio.")
    return espacio


@router.get("/reservas")
def reservas_del_proveedor(usuario: Usuario = Depends(exigir_roles("PROVEEDOR")), db: Session = Depends(get_db)):
    proveedor_id = _proveedor_id(usuario)
    filas = db.execute(select(Reserva, Espacio, Sector).join(Espacio, Reserva.idEspacio == Espacio.idEspacio).join(Sector, Espacio.idSector == Sector.idSector).where(Sector.idProveedor == proveedor_id).order_by(Reserva.fechaInicioReserva.desc())).all()
    return [
        {
            "idReserva": reserva.idReserva,
            "codigoReserva": reserva.codigoReserva,
            "estado": reserva.estado,
            "fechaInicioReserva": reserva.fechaInicioReserva,
            "fechaFinReserva": reserva.fechaFinReserva,
            "idCliente": reserva.idCliente,
            "idVehiculo": reserva.idVehiculo,
            "idEspacio": espacio.idEspacio,
            "codigoEspacio": espacio.codigoEspacio,
            "nombreSector": sector.nombreSector,
        }
        for reserva, espacio, sector in filas
    ]


@router.get("/billetera")
def billetera_proveedor(usuario: Usuario = Depends(exigir_roles("PROVEEDOR")), db: Session = Depends(get_db)):
    proveedor_id = _proveedor_id(usuario)
    pagos_query = (
        select(Pago)
        .join(Ocupacion, Pago.idOcupacion == Ocupacion.idOcupacion)
        .join(Reserva, Ocupacion.idReserva == Reserva.idReserva)
        .join(Espacio, Reserva.idEspacio == Espacio.idEspacio)
        .join(Sector, Espacio.idSector == Sector.idSector)
        .where(Sector.idProveedor == proveedor_id, Pago.estado == "PAGADO")
    )
    pagos_pagados = db.scalars(pagos_query.order_by(Pago.fechaPago.desc())).all()
    total_pagado = sum((Decimal(str(p.montoTotal or 0)) for p in pagos_pagados), Decimal("0.00"))
    return {
        "totalPagado": total_pagado,
        "cantidadPagos": len(pagos_pagados),
        "movimientos": [
            {"idPago": p.idPago, "codigoPago": p.codigoPago, "montoTotal": p.montoTotal, "estado": p.estado, "metodoPago": p.metodoPago, "fechaPago": p.fechaPago}
            for p in pagos_pagados[:50]
        ],
    }


@router.get("/resumen")
def resumen_proveedor(usuario: Usuario = Depends(exigir_roles("PROVEEDOR")), db: Session = Depends(get_db)):
    proveedor_id = _proveedor_id(usuario)
    sectores = db.scalar(select(func.count()).select_from(Sector).where(Sector.idProveedor == proveedor_id, Sector.estado == "ACTIVO")) or 0
    espacios = db.scalar(select(func.count()).select_from(Espacio).join(Sector, Espacio.idSector == Sector.idSector).where(Sector.idProveedor == proveedor_id, Espacio.estado != "INACTIVO")) or 0
    disponibles = db.scalar(select(func.count()).select_from(Espacio).join(Sector, Espacio.idSector == Sector.idSector).where(Sector.idProveedor == proveedor_id, Espacio.estado == "DISPONIBLE")) or 0
    reservas = db.scalar(select(func.count()).select_from(Reserva).join(Espacio, Reserva.idEspacio == Espacio.idEspacio).join(Sector, Espacio.idSector == Sector.idSector).where(Sector.idProveedor == proveedor_id)) or 0
    return {"sectores": sectores, "espacios": espacios, "disponibles": disponibles, "reservas": reservas}
