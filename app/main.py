from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.Settings import settings
import app.events.ClienteEvents
from app.controllers.ClienteController import router as cliente_router
from app.controllers.DeudaController import router as deuda_router
from app.controllers.EspacioController import router as espacio_router
from app.controllers.HealthController import router as health_router
from app.controllers.NotificacionController import router as notificacion_router
from app.controllers.OcupacionController import router as ocupacion_router
from app.controllers.PagoController import router as pago_router
from app.controllers.QrController import router as qr_router
from app.controllers.ReservaController import router as reserva_router
from app.controllers.VehiculoController import router as vehiculo_router
from app.controllers.AuthController import router as auth_router


app = FastAPI(
    title="ParkSmart API",
    version="1.0.0",
    description="API REST para el sistema ParkSmart",
    root_path=settings.ROOT_PATH,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(cliente_router)
app.include_router(vehiculo_router)
app.include_router(espacio_router)
app.include_router(reserva_router)
app.include_router(qr_router)
app.include_router(ocupacion_router)
app.include_router(pago_router)
app.include_router(deuda_router)
app.include_router(notificacion_router)
app.include_router(auth_router)


@app.get("/", tags=["General"])
def inicio():
    return {
        "service": "ParkSmart API",
        "version": "1.0.0",
        "status": "ok",
        "docs": "/docs",
    }