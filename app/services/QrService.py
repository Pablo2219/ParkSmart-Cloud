from datetime import datetime, timedelta
import secrets

from sqlalchemy.orm import Session

from app.repositories.QrRepository import QrRepository
from app.repositories.ReservaRepository import ReservaRepository
from app.schemas.qr.QrCreate import QrCreate


class QrService:

    def __init__(self, db: Session):
        self.qr_repository = QrRepository(db)
        self.reserva_repository = ReservaRepository(db)

    def listar_qrs(self):
        return self.qr_repository.listar()

    def listar_qrs_por_reserva(self, idReserva: int):
        reserva = self.reserva_repository.obtener_por_id(idReserva)

        if reserva is None:
            raise ValueError("La reserva no existe.")

        return self.qr_repository.listar_por_reserva(idReserva)

    def obtener_qr(self, idQr: int):
        qr = self.qr_repository.obtener_por_id(idQr)

        if qr is None:
            raise ValueError("El QR no existe.")

        return qr

    def validar_qr_activo(self, idQr: int) -> bool:
        qr = self.qr_repository.obtener_por_id(idQr)

        if qr is None:
            raise ValueError("El QR no existe.")

        return self.qr_repository.validar_qr_activo(idQr)

    def obtener_qr_por_codigo(self, codigoQr: str):
        qr = self.qr_repository.obtener_por_codigo(codigoQr)

        if qr is None:
            raise ValueError("El QR no existe.")

        return qr

    def generar_qr(self, datos: QrCreate):
        reserva = self.reserva_repository.obtener_por_id(datos.idReserva)

        if reserva is None:
            raise ValueError("La reserva no existe.")

        if reserva.estado != "CONFIRMADA":
            raise ValueError(
                "Solo se puede generar QR para reservas confirmadas."
            )

        qr_existente = self.qr_repository.obtener_por_reserva_activa(
            datos.idReserva
        )

        if qr_existente is not None:
            return qr_existente

        codigo_qr = self.generar_codigo_qr(datos.idReserva)
        token_qr = secrets.token_urlsafe(32)

        fecha_activacion = reserva.fechaInicioReserva - timedelta(
            minutes=10
        )

        fecha_expiracion = reserva.fechaFinReserva

        return self.qr_repository.crear_activo(
            idReserva=datos.idReserva,
            codigoQr=codigo_qr,
            tokenQr=token_qr,
            fechaActivacion=fecha_activacion,
            fechaExpiracion=fecha_expiracion
        )

    def validar_qr(self, codigoQr: str):
        qr = self.qr_repository.obtener_por_codigo(codigoQr)

        if qr is None:
            raise ValueError("El QR no existe.")

        if qr.estado == "USADO":
            raise ValueError("El QR ya fue utilizado.")

        if qr.estado == "CANCELADO":
            raise ValueError("El QR se encuentra cancelado.")

        if qr.estado == "VENCIDO":
            raise ValueError("El QR se encuentra vencido.")

        if qr.estado != "ACTIVO":
            raise ValueError("El QR no se encuentra activo.")

        fecha_actual = datetime.now()

        if fecha_actual < qr.fechaActivacion:
            raise ValueError("El QR todavia no es valido.")

        if fecha_actual > qr.fechaExpiracion:
            self.qr_repository.marcar_vencido(qr)
            raise ValueError("El QR se encuentra vencido.")

        return qr

    def usar_qr(self, codigoQr: str):
        qr = self.validar_qr(codigoQr)

        return self.qr_repository.marcar_usado(qr)

    def anular_qr(self, idQr: int):
        qr = self.qr_repository.obtener_por_id(idQr)

        if qr is None:
            raise ValueError("El QR no existe.")

        if qr.estado in ["USADO", "VENCIDO", "CANCELADO"]:
            raise ValueError(
                "No se puede cancelar un QR usado, vencido o ya cancelado."
            )

        return self.qr_repository.anular(qr)

    def generar_codigo_qr(self, idReserva: int):
        fecha = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"QR-{idReserva}-{fecha}"