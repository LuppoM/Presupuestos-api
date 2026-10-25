import os
import psycopg2
from contextlib import contextmanager

# Carga la URI desde las variables de entorno de Render
SUPABASE_URI = os.getenv(
    "SUPABASE_URI",
    "postgresql://postgres.wieljyluvxlsolrjcnjk:lautarodrogadicto@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
)

@contextmanager
def conectar_db():
    conexion = None
    try:
        conexion = psycopg2.connect(SUPABASE_URI)
        yield conexion
    except Exception as e:
        if conexion:
            conexion.rollback()
        print(f"Error al conectar a Supabase: {e}")
        raise e
    finally:
        if conexion:
            conexion.close()