from sqlalchemy import event

from app.models.Cliente import Cliente
from app.models.Bitacora import Bitacora


@event.listens_for(Cliente, "after_insert")
def registrar_cliente_en_bitacora(mapper, connection, target):
    connection.execute(
        Bitacora.__table__.insert().values(
            modulo="Cliente",
            accion="INSERT",
            descripcion=(
                f"Se registro el cliente con identificacion: "
                f"{target.identificacion}"
            ),
            resultado="EXITOSO",
        )
    )