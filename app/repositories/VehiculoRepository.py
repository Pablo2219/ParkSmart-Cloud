from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.Vehiculo import Vehiculo
from app.schemas.vehiculo.VehiculoCreate import VehiculoCreate
from app.schemas.vehiculo.VehiculoUpdate import VehiculoUpdate


class VehiculoRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        consulta = select(Vehiculo)
        return self.db.scalars(consulta).all()

    def obtener_por_id(self, idVehiculo: int):
        consulta = select(Vehiculo).where(
            Vehiculo.idVehiculo == idVehiculo
        )

        return self.db.scalar(consulta)

    def obtener_por_cliente(self, idCliente: int):
        consulta = select(Vehiculo).where(
            Vehiculo.idCliente == idCliente
        )

        return self.db.scalars(consulta).all()

    def obtener_por_placa(self, placa: str):
        consulta = select(Vehiculo).where(
            Vehiculo.placa == placa
        )

        return self.db.scalar(consulta)

    def crear(self, datos: VehiculoCreate):
        vehiculo = Vehiculo(**datos.model_dump())

        self.db.add(vehiculo)
        self.db.commit()
        self.db.refresh(vehiculo)

        return vehiculo

    def actualizar(self, vehiculo: Vehiculo, datos: VehiculoUpdate):
        datos_actualizados = datos.model_dump(exclude_unset=True)

        for campo, valor in datos_actualizados.items():
            setattr(vehiculo, campo, valor)

        self.db.commit()
        self.db.refresh(vehiculo)

        return vehiculo

    def eliminar_logico(self, vehiculo: Vehiculo):
        vehiculo.estado = "INACTIVO"

        self.db.commit()
        self.db.refresh(vehiculo)

        return vehiculo