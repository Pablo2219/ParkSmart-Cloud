from datetime import datetime

from sqlalchemy.orm import Session

from app.repositories.ClienteRepository import ClienteRepository
from app.repositories.VehiculoRepository import VehiculoRepository
from app.repositories.EspacioRepository import EspacioRepository
from app.repositories.ReservaRepository import ReservaRepository
from app.schemas.reserva.ReservaCreate import ReservaCreate
from app.schemas.reserva.ReservaUpdate import ReservaUpdate


class ReservaService:

    def __init__(self, db: Session):
        self.reserva_repository = ReservaRepository(db)
        self.cliente_repository = ClienteRepository(db)
        self.vehiculo_repository = VehiculoRepository(db)
        self.espacio_repository = EspacioRepository(db)

    def listar_reservas(self):
        return self.reserva_repository.listar()

    def listar_reservas_activas(self):
        return self.reserva_repository.listar_activas()

    def listar_reservas_por_cliente(self, idCliente: int):
        cliente = self.cliente_repository.obtener_por_id(idCliente)

        if cliente is None:
            raise ValueError("El cliente no existe.")

        return self.reserva_repository.listar_por_cliente(idCliente)

    def obtener_reserva(self, idReserva: int):
        reserva = self.reserva_repository.obtener_por_id(idReserva)

        if reserva is None:
            raise ValueError("La reserva no existe.")

        return reserva

    def crear_reserva(self, datos: ReservaCreate):
        cliente = self.cliente_repository.obtener_por_id(datos.idCliente)

        if cliente is None:
            raise ValueError("El cliente no existe.")

        if cliente.estado != "ACTIVO":
            raise ValueError("El cliente no se encuentra activo.")

        vehiculo = self.vehiculo_repository.obtener_por_id(datos.idVehiculo)

        if vehiculo is None:
            raise ValueError("El vehiculo no existe.")

        if vehiculo.estado != "ACTIVO":
            raise ValueError("El vehiculo no se encuentra activo.")

        if vehiculo.idCliente != datos.idCliente:
            raise ValueError("El vehiculo no pertenece al cliente indicado.")

        espacio = self.espacio_repository.obtener_por_id(datos.idEspacio)

        if espacio is None:
            raise ValueError("El espacio no existe.")

        if espacio.estado != "DISPONIBLE":
            raise ValueError("El espacio no se encuentra disponible.")

        existe_cruce = self.reserva_repository.existe_cruce_reserva(
            datos.idEspacio,
            datos.fechaInicioReserva,
            datos.fechaFinReserva
        )

        if existe_cruce:
            raise ValueError(
                "Ya existe una reserva activa para ese espacio en ese horario."
            )

        codigo_reserva = self.generar_codigo_reserva()

        return self.reserva_repository.crear(datos, codigo_reserva)

    def actualizar_reserva(self, idReserva: int, datos: ReservaUpdate):
        reserva = self.reserva_repository.obtener_por_id(idReserva)

        if reserva is None:
            raise ValueError("La reserva no existe.")

        if reserva.estado in ["CANCELADA", "UTILIZADA", "VENCIDA"]:
            raise ValueError(
                "No se puede modificar una reserva cancelada, utilizada o vencida."
            )

        fecha_inicio = datos.fechaInicioReserva or reserva.fechaInicioReserva
        fecha_fin = datos.fechaFinReserva or reserva.fechaFinReserva

        if fecha_fin <= fecha_inicio:
            raise ValueError(
                "La fecha final debe ser posterior a la fecha inicial."
            )

        existe_cruce = self.reserva_repository.existe_cruce_reserva(
            reserva.idEspacio,
            fecha_inicio,
            fecha_fin,
            idReservaExcluir=idReserva
        )

        if existe_cruce:
            raise ValueError(
                "Ya existe otra reserva activa para ese espacio en ese horario."
            )

        return self.reserva_repository.actualizar(reserva, datos)

    def cancelar_reserva(self, idReserva: int):
        reserva = self.reserva_repository.obtener_por_id(idReserva)

        if reserva is None:
            raise ValueError("La reserva no existe.")

        if reserva.estado not in ["PENDIENTE", "CONFIRMADA"]:
            raise ValueError("Solo se pueden cancelar reservas activas.")

        return self.reserva_repository.cancelar(reserva)

    def generar_codigo_reserva(self):
        fecha = datetime.now().strftime("%Y%m%d%H%M%S%f")
        return f"RES-{fecha}"