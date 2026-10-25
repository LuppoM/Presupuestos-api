import psycopg2
from contextlib import contextmanager

# Opción A: Conexión Directa (Reemplaza [TU_CONTRASEÑA] con la clave de tu base de datos)
SUPABASE_URI = "postgresql://postgres:[lautarodrogadicto]@db.wieljyluvxlsolrjcnjk.supabase.co:5432/postgres"

# Opción B: Si prefieres usar el Session Pooler (puerto 6543)
# SUPABASE_URI = "postgresql://postgres.wieljyluvxlsolrjcnjk:[TU_CONTRASEÑA]@aws-0-[region].pooler.supabase.com:6543/postgres"

@contextmanager
def conectar_db():
    """Context manager para manejar la conexión a Supabase de forma segura."""
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

# Bloque para probar la conexión
if __name__ == "__main__":
    try:
        with conectar_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                print("¡Conexión exitosa a Supabase!")
                print("Versión de PostgreSQL:", version[0])
    except Exception as e:
        print("No se pudo establecer la conexión. Revisa tu contraseña.")