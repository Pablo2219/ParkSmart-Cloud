from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.Espacio import Espacio
from app.models.Sector import Sector
from app.schemas.espacio.EspacioCreate import EspacioCreate
from app.schemas.espacio.EspacioUpdate import EspacioUpdate


class EspacioRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar_sectores(self):
        consulta = select(Sector)
        return self.db.scalars(consulta).all()

    def obtener_sector_por_id(self, idSector: int):
        consulta = select(Sector).where(
            Sector.idSector == idSector
        )

        return self.db.scalar(consulta)

    def listar(self):
        consulta = select(Espacio)
        return self.db.scalars(consulta).all()

    def listar_disponibles(self):
        consulta = select(Espacio).where(
            Espacio.estado == "DISPONIBLE"
        )

        return self.db.scalars(consulta).all()

    def obtener_por_id(self, idEspacio: int):
        consulta = select(Espacio).where(
            Espacio.idEspacio == idEspacio
        )

        return self.db.scalar(consulta)

    def obtener_por_codigo(self, codigoEspacio: str):
        consulta = select(Espacio).where(
            Espacio.codigoEspacio == codigoEspacio
        )

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