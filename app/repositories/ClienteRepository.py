from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.Cliente import Cliente
from app.schemas.cliente.ClienteCreate import ClienteCreate
from app.schemas.cliente.ClienteUpdate import ClienteUpdate


class ClienteRepository:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        consulta = select(Cliente)
        return self.db.scalars(consulta).all()

    def obtener_por_id(self, idCliente: int):
        consulta = select(Cliente).where(
            Cliente.idCliente == idCliente
        )

        return self.db.scalar(consulta)

    def obtener_por_identificacion(self, identificacion: str):
        consulta = select(Cliente).where(
            Cliente.identificacion == identificacion
        )

        return self.db.scalar(consulta)

    def obtener_por_correo(self, correoElectronico: str):
        consulta = select(Cliente).where(
            Cliente.correoElectronico == correoElectronico
        )

        return self.db.scalar(consulta)

    def crear(self, datos: ClienteCreate):
        cliente = Cliente(**datos.model_dump())

        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)

        return cliente

    def actualizar(self, cliente: Cliente, datos: ClienteUpdate):
        datos_actualizados = datos.model_dump(exclude_unset=True)

        for campo, valor in datos_actualizados.items():
            setattr(cliente, campo, valor)

        self.db.commit()
        self.db.refresh(cliente)

        return cliente

    def eliminar_logico(self, cliente: Cliente):
        cliente.estado = "INACTIVO"

        self.db.commit()
        self.db.refresh(cliente)

        return cliente