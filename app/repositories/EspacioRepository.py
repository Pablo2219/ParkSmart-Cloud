from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.Espacio import Espacio
from app.models.Proveedor import Proveedor
from app.models.Sector import Sector
from app.schemas.espacio.EspacioCreate import EspacioCreate
from app.schemas.espacio.EspacioUpdate import EspacioUpdate


class EspacioRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar_sectores(self):
        consulta = (
            select(Sector)
            .join(Proveedor, Sector.idProveedor == Proveedor.idProveedor)
            .where(Sector.estado == "ACTIVO", Proveedor.estado == "ACTIVO")
            .options(joinedload(Sector.proveedor))
            .order_by(Sector.nombreSector)
        )
        return self.db.scalars(consulta).unique().all()

    def obtener_sector_por_id(self, idSector: int):
        consulta = select(Sector).where(Sector.idSector == idSector)
        return self.db.scalar(consulta)

    def listar(self):
        consulta = (
            select(Espacio)
            .join(Sector, Espacio.idSector == Sector.idSector)
            .join(Proveedor, Sector.idProveedor == Proveedor.idProveedor)
            .where(Espacio.estado != "INACTIVO", Sector.estado == "ACTIVO", Proveedor.estado == "ACTIVO")
            .options(joinedload(Espacio.sector).joinedload(Sector.proveedor))
            .order_by(Espacio.codigoEspacio)
        )
        return self.db.scalars(consulta).unique().all()

    def listar_disponibles(self):
        consulta = (
            select(Espacio)
            .join(Sector, Espacio.idSector == Sector.idSector)
            .join(Proveedor, Sector.idProveedor == Proveedor.idProveedor)
            .where(Espacio.estado == "DISPONIBLE", Sector.estado == "ACTIVO", Proveedor.estado == "ACTIVO")
            .options(joinedload(Espacio.sector).joinedload(Sector.proveedor))
            .order_by(Espacio.codigoEspacio)
        )
        return self.db.scalars(consulta).unique().all()

    def obtener_por_id(self, idEspacio: int):
        consulta = select(Espacio).where(Espacio.idEspacio == idEspacio)
        return self.db.scalar(consulta)

    def obtener_por_codigo(self, codigoEspacio: str):
        consulta = select(Espacio).where(Espacio.codigoEspacio == codigoEspacio)
        return self.db.scalar(consulta)

    def crear(self, datos: EspacioCreate):
        espacio = Espacio(**datos.model_dump())
        self.db.add(espacio)
        self.db.commit()
        self.db.refresh(espacio)
        return espacio

    def actualizar(self, espacio: Espacio, datos: EspacioUpdate):
        datos_actualizados = datos.model_dump(exclude_unset=True)
        for campo, valor in datos_actualizados.items():
            setattr(espacio, campo, valor)
        self.db.commit()
        self.db.refresh(espacio)
        return espacio

    def eliminar_logico(self, espacio: Espacio):
        espacio.estado = "INACTIVO"
        self.db.commit()
        self.db.refresh(espacio)
        return espacio
