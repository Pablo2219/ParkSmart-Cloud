from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.Espacio import Espacio
from app.models.Ocupacion import Ocupacion
from app.models.Reserva import Reserva
from app.models.Sector import Sector
from app.repositories.OcupacionRepository import OcupacionRepository
from app.repositories.PagoRepository import PagoRepository
from app.schemas.pago.PagoCreate import PagoCreate
from app.schemas.pago.PagoUpdate import PagoUpdate
from app.services.FacturacionService import facturacion_service


class PagoService:

    def __init__(self, db: Session):
        self.db = db
        self.pago_repository = PagoRepository(db)
        self.ocupacion_repository = OcupacionRepository(db)

    def listar_pagos(self):
        return self.pago_repository.listar()

    def listar_pagos_pendientes(self):
        return self.pago_repository.listar_pendientes()

    def listar_pagos_por_ocupacion(self, idOcupacion: int):
        ocupacion = self.ocupacion_repository.obtener_por_id(idOcupacion)
        if ocupacion is None:
            raise ValueError("La ocupacion no existe.")
        return self.pago_repository.listar_por_ocupacion(idOcupacion)

    def obtener_pago(self, idPago: int):
        pago = self.pago_repository.obtener_por_id(idPago)
        if pago is None:
            raise ValueError("El pago no existe.")
        return pago

    def verificar_pago_vencido(self, idPago: int) -> bool:
        pago = self.pago_repository.obtener_por_id(idPago)
        if pago is None:
            raise ValueError("El pago no existe.")
        return self.pago_repository.verificar_pago_vencido(idPago)

    def crear_pago(self, datos: PagoCreate):
        ocupacion = self.ocupacion_repository.obtener_por_id(datos.idOcupacion)
        if ocupacion is None:
            raise ValueError("La ocupacion no existe.")
        if ocupacion.estado != "FINALIZADA":
            raise ValueError("Solo se puede generar pago para ocupaciones finalizadas.")
        if self.pago_repository.obtener_activo_por_ocupacion(datos.idOcupacion) is not None:
            raise ValueError("Ya existe un pago registrado para esta ocupacion.")
        return self.pago_repository.crear(datos, self.generar_codigo_pago())

    def actualizar_pago(self, idPago: int, datos: PagoUpdate):
        pago = self.pago_repository.obtener_por_id(idPago)
        if pago is None:
            raise ValueError("El pago no existe.")
        if pago.estado == "PAGADO":
            raise ValueError("No se puede modificar un pago ya confirmado.")
        return self.pago_repository.actualizar(pago, datos)

    def confirmar_pago(self, idPago: int, datos: PagoUpdate):
        pago = self.pago_repository.obtener_por_id(idPago)
        if pago is None:
            raise ValueError("El pago no existe.")
        if pago.estado != "PENDIENTE":
            raise ValueError("Solo se pueden confirmar pagos pendientes.")
        if self.pago_repository.verificar_pago_vencido(idPago):
            self.pago_repository.marcar_vencido(pago)
            raise ValueError("El pago ya supero el limite de 24 horas.")
        if datos.metodoPago is None:
            raise ValueError("Debe indicar el metodo de pago.")

        pago = self.pago_repository.confirmar(pago, datos)
        proveedor_id = self.db.scalar(
            select(Sector.idProveedor)
            .join(Espacio, Espacio.idSector == Sector.idSector)
            .join(Reserva, Reserva.idEspacio == Espacio.idEspacio)
            .join(Ocupacion, Ocupacion.idReserva == Reserva.idReserva)
            .where(Ocupacion.idOcupacion == pago.idOcupacion)
        )
        # No se revierte un pago confirmado si el API externo falla.
        # En local el adaptador trabaja en modo SIMULATION.
        facturacion_service.emitir_factura(pago, proveedor_id=proveedor_id)
        return pago

    def anular_pago(self, idPago: int):
        pago = self.pago_repository.obtener_por_id(idPago)
        if pago is None:
            raise ValueError("El pago no existe.")
        if pago.estado == "PAGADO":
            raise ValueError("No se puede anular un pago confirmado.")
        return self.pago_repository.anular(pago)

    def generar_codigo_pago(self):
        fecha = datetime.now().strftime("%Y%m%d%H%M%S%f")
        return f"PAG-{fecha}"
