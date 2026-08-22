from sqlalchemy.orm import Session

from app.repositories.ClienteRepository import ClienteRepository
from app.repositories.VehiculoRepository import VehiculoRepository
from app.schemas.vehiculo.VehiculoCreate import VehiculoCreate
from app.schemas.vehiculo.VehiculoUpdate import VehiculoUpdate


class VehiculoService:

    def __init__(self, db: Session):
        self.vehiculo_repository = VehiculoRepository(db)
        self.cliente_repository = ClienteRepository(db)

    def listar_vehiculos(self):
        return self.vehiculo_repository.listar()

    def obtener_vehiculo(self, idVehiculo: int):
        vehiculo = self.vehiculo_repository.obtener_por_id(idVehiculo)

        if vehiculo is None:
            raise ValueError("El vehiculo no existe.")

        return vehiculo

    def listar_vehiculos_por_cliente(self, idCliente: int):
        cliente = self.cliente_repository.obtener_por_id(idCliente)

        if cliente is None:
            raise ValueError("El cliente no existe.")

        return self.vehiculo_repository.obtener_por_cliente(idCliente)

    def crear_vehiculo(self, datos: VehiculoCreate):
        cliente = self.cliente_repository.obtener_por_id(datos.idCliente)

        if cliente is None:
            raise ValueError("El cliente no existe.")

        if cliente.estado != "ACTIVO":
            raise ValueError("El cliente no se encuentra activo.")

        vehiculo_placa = self.vehiculo_repository.obtener_por_placa(
            datos.placa
        )

        if vehiculo_placa is not None:
            raise ValueError("Ya existe un vehiculo con esa placa.")

        return self.vehiculo_repository.crear(datos)

    def actualizar_vehiculo(
        self,
        idVehiculo: int,
        datos: VehiculoUpdate
    ):
        vehiculo = self.vehiculo_repository.obtener_por_id(idVehiculo)

        if vehiculo is None:
            raise ValueError("El vehiculo no existe.")

        if datos.placa is not None:
            vehiculo_placa = self.vehiculo_repository.obtener_por_placa(
                datos.placa
            )

            if (
                vehiculo_placa is not None
                and vehiculo_placa.idVehiculo != idVehiculo
            ):
                raise ValueError("La placa ya esta registrada.")

        return self.vehiculo_repository.actualizar(vehiculo, datos)

    def eliminar_vehiculo(self, idVehiculo: int):
        vehiculo = self.vehiculo_repository.obtener_por_id(idVehiculo)

        if vehiculo is None:
            raise ValueError("El vehiculo no existe.")

        return self.vehiculo_repository.eliminar_logico(vehiculo)