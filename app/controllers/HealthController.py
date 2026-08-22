from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.Session import get_db

router = APIRouter(prefix="/health", tags=["Salud y Monitoreo"])

@router.get("")
def health_check():
    # Liveness probe: Confirma que el proceso de FastAPI no se ha congelado
    return {"status": "ok", "message": "API ParkSmart en ejecución"}

@router.get("/ready")
def readiness_check(db: Session = Depends(get_db)):
    # Readiness probe: Confirma que podemos hablar con MySQL
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready", "message": "Conexión a base de datos exitosa"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Base de datos no disponible"
        )