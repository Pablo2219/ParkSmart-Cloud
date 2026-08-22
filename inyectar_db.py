import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# 1. Cargar variables del entorno
load_dotenv(override=True)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Error: No se encontró DATABASE_URL en el archivo .env")
    exit()

# Truco 1: Corregir el conector si viene como 'mysql://'
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

# Truco 2: Quitar el ssl-mode de la URL porque a pymysql no le gusta
if "?ssl-mode=REQUIRED" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("?ssl-mode=REQUIRED", "")

print("Conectando con el driver pymysql...")

# Pasamos el SSL limpio como diccionario para que DigitalOcean nos deje entrar
engine = create_engine(
    DATABASE_URL,
    connect_args={"ssl": {}} 
)

# 2. Ruta al archivo SQL
ruta_sql = os.path.join("database", "parksmart_db.sql")

try:
    with open(ruta_sql, 'r', encoding='utf-8') as archivo:
        codigo_sql = archivo.read()

    # Dividir las sentencias SQL
    instrucciones = [i.strip() for i in codigo_sql.split(';') if i.strip()]

    with engine.begin() as conexion:
        for instruccion in instrucciones:
            conexion.execute(text(instruccion))

    print("¡Éxito total! Tus tablas ya están en la nube de DigitalOcean.")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo SQL en '{ruta_sql}'. Revisa el nombre o la carpeta.")
except Exception as e:
    print(f"Error durante la ejecución: {e}")