from sqlalchemy.orm import Session

from app.repositories.EspacioRepository import EspacioRepository
from app.schemas.espacio.EspacioCreate import EspacioCreate
from app.schemas.espacio.EspacioUpdate import EspacioUpdate


class EspacioService:

    def __init__(self, db: Session):
        self.repository = EspacioRepository(db)

    def listar_sectores(self):
        return self.repository.listar_sectores()

    def listar_espacios(self):
        return self.repository.listar()

    def listar_espacios_disponibles(self):
        return self.repository.listar_disponibles()

    def obtener_espacio(self, idEspacio: int):
        espacio = self.repository.obtener_por_id(idEspacio)

        if espacio is None:
            raise ValueError("El espacio no existe.")

        return espacio

    def crear_espacio(self, datos: EspacioCreate):
        sector = self.repository.obtener_sector_por_id(datos.idSector)

        if sector is None:
            raise ValueError("El sector no existe.")

        if sector.estado != "ACTIVO":
            raise ValueError("El sector no se encuentra activo.")

        espacio_codigo = self.repository.obtener_por_codigo(
            datos.codigoEspacio
        )

        if espacio_codigo is not None:
            raise ValueError("Ya existe un espacio con ese codigo.")

        return self.repository.crear(datos)

    def actualizar_espacio(self, idEspacio: int, datos: EspacioUpdate):
        espacio = self.repository.obtener_por_id(idEspacio)

        if espacio is None:
            raise ValueError("El espacio no existe.")

        if datos.idSector is not None:
            sector = self.repository.obtener_sector_por_id(datos.idSector)

            if sector is None:
                raise ValueError("El sector no existe.")

            if sector.estado != "ACTIVO":
                raise ValueError("El sector no se encuentra activo.")

        if datos.codigoEspacio is not None:
            espacio_codigo = self.repository.obtener_por_codigo(
                datos.codigoEspacio
            )

            if (
                espacio_codigo is not None
                and espacio_codigo.idEspacio != idEspacio
            ):
                raise ValueError("El codigo de espacio ya esta registrado.")

        return self.repository.actualizar(espacio, datos)

    def eliminar_espacio(self, idEspacio: int):
        espacio = self.repository.obtener_por_id(idEspacio)

        if espacio is None:
            raise ValueError("El espacio no existe.")

        return self.repository.eliminar_logico(espacio)