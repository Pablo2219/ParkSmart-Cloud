from sqlalchemy.orm import Session

from app.repositories.ClienteRepository import ClienteRepository
from app.schemas.cliente.ClienteCreate import ClienteCreate
from app.schemas.cliente.ClienteUpdate import ClienteUpdate


class ClienteService:

    def __init__(self, db: Session):
        self.repository = ClienteRepository(db)

    def listar_clientes(self):
        return self.repository.listar()

    def obtener_cliente(self, idCliente: int):
        cliente = self.repository.obtener_por_id(idCliente)

        if cliente is None:
            raise ValueError("El cliente no existe.")

        return cliente

    def crear_cliente(self, datos: ClienteCreate):
        cliente_identificacion = self.repository.obtener_por_identificacion(
            datos.identificacion
        )

        if cliente_identificacion is not None:
            raise ValueError("Ya existe un cliente con esa identificacion.")

        cliente_correo = self.repository.obtener_por_correo(
            datos.correoElectronico
        )

        if cliente_correo is not None:
            raise ValueError("Ya existe un cliente con ese correo electronico.")

        return self.repository.crear(datos)

    def actualizar_cliente(self, idCliente: int, datos: ClienteUpdate):
        cliente = self.repository.obtener_por_id(idCliente)

        if cliente is None:
            raise ValueError("El cliente no existe.")

        if datos.correoElectronico is not None:
            cliente_correo = self.repository.obtener_por_correo(
                datos.correoElectronico
            )

            if (
                cliente_correo is not None
                and cliente_correo.idCliente != idCliente
            ):
                raise ValueError("El correo electronico ya esta registrado.")

        return self.repository.actualizar(cliente, datos)

    def eliminar_cliente(self, idCliente: int):
        cliente = self.repository.obtener_por_id(idCliente)

        if cliente is None:
            raise ValueError("El cliente no existe.")

        return self.repository.eliminar_logico(cliente)