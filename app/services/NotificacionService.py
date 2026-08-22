from sqlalchemy.orm import Session

from app.repositories.ClienteRepository import ClienteRepository
from app.repositories.DeudaRepository import DeudaRepository
from app.repositories.NotificacionRepository import NotificacionRepository
from app.repositories.PagoRepository import PagoRepository
from app.repositories.ReservaRepository import ReservaRepository
from app.schemas.notificacion.NotificacionCreate import NotificacionCreate
from app.schemas.notificacion.NotificacionUpdate import NotificacionUpdate


class NotificacionService:

    def __init__(self, db: Session):
        self.notificacion_repository = NotificacionRepository(db)
        self.cliente_repository = ClienteRepository(db)
        self.reserva_repository = ReservaRepository(db)
        self.pago_repository = PagoRepository(db)
        self.deuda_repository = DeudaRepository(db)

    def listar_notificaciones(self):
        return self.notificacion_repository.listar()

    def listar_notificaciones_pendientes(self):
        return self.notificacion_repository.listar_pendientes()

    def listar_notificaciones_por_cliente(self, idCliente: int):
        cliente = self.cliente_repository.obtener_por_id(idCliente)

        if cliente is None:
            raise ValueError("El cliente no existe.")

        return self.notificacion_repository.listar_por_cliente(idCliente)

    def obtener_notificacion(self, idNotificacion: int):
        notificacion = self.notificacion_repository.obtener_por_id(
            idNotificacion
        )

        if notificacion is None:
            raise ValueError("La notificacion no existe.")

        return notificacion

    def crear_notificacion(self, datos: NotificacionCreate):
        cliente = self.cliente_repository.obtener_por_id(datos.idCliente)

        if cliente is None:
            raise ValueError("El cliente no existe.")

        if datos.idReserva is not None:
            reserva = self.reserva_repository.obtener_por_id(datos.idReserva)

            if reserva is None:
                raise ValueError("La reserva asociada no existe.")

        if datos.idPago is not None:
            pago = self.pago_repository.obtener_por_id(datos.idPago)

            if pago is None:
                raise ValueError("El pago asociado no existe.")

        if datos.idDeuda is not None:
            deuda = self.deuda_repository.obtener_por_id(datos.idDeuda)

            if deuda is None:
                raise ValueError("La deuda asociada no existe.")

        return self.notificacion_repository.crear(datos)

    def actualizar_notificacion(
        self,
        idNotificacion: int,
        datos: NotificacionUpdate
    ):
        notificacion = self.notificacion_repository.obtener_por_id(
            idNotificacion
        )

        if notificacion is None:
            raise ValueError("La notificacion no existe.")

        if notificacion.estado in ["ENVIADA", "LEIDA", "ANULADA"]:
            raise ValueError(
                "No se puede modificar una notificacion enviada, leida o anulada."
            )

        return self.notificacion_repository.actualizar(notificacion, datos)

    def enviar_notificacion(self, idNotificacion: int):
        notificacion = self.notificacion_repository.obtener_por_id(
            idNotificacion
        )

        if notificacion is None:
            raise ValueError("La notificacion no existe.")

        if notificacion.estado != "PENDIENTE":
            raise ValueError("Solo se pueden enviar notificaciones pendientes.")

        return self.notificacion_repository.marcar_enviada(notificacion)

    def leer_notificacion(self, idNotificacion: int):
        notificacion = self.notificacion_repository.obtener_por_id(
            idNotificacion
        )

        if notificacion is None:
            raise ValueError("La notificacion no existe.")

        if notificacion.estado not in ["ENVIADA", "PENDIENTE"]:
            raise ValueError(
                "Solo se pueden marcar como leidas notificaciones pendientes o enviadas."
            )

        return self.notificacion_repository.marcar_leida(notificacion)

    def fallar_notificacion(self, idNotificacion: int):
        notificacion = self.notificacion_repository.obtener_por_id(
            idNotificacion
        )

        if notificacion is None:
            raise ValueError("La notificacion no existe.")

        if notificacion.estado not in ["PENDIENTE", "ENVIADA"]:
            raise ValueError(
                "Solo se pueden marcar como fallidas notificaciones pendientes o enviadas."
            )

        return self.notificacion_repository.marcar_fallida(notificacion)

    def anular_notificacion(self, idNotificacion: int):
        notificacion = self.notificacion_repository.obtener_por_id(
            idNotificacion
        )

        if notificacion is None:
            raise ValueError("La notificacion no existe.")

        if notificacion.estado == "LEIDA":
            raise ValueError("No se puede anular una notificacion leida.")

        return self.notificacion_repository.anular(notificacion)