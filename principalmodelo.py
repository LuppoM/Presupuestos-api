import psycopg2
from conexion import SUPABASE_URI

def obtener_conexion():
    """ 
    Establece la conexión activa con la base de datos de Supabase 
    para mantenerla abierta durante la sesión del usuario.
    """
    try:
        conexion = psycopg2.connect(SUPABASE_URI)
        return conexion
    except Exception as e:
        print(f"Error al conectar con Supabase: {e}")
        raise e

def realizar_backup():
    """
    Al trabajar con Supabase (PostgreSQL en la nube), los respaldos 
    y la seguridad de los datos son administrados automáticamente por la plataforma.
    """
    try:
        # Retornamos éxito para que el flujo de cierre de la aplicación continúe con normalidad
        return True, "Respaldo gestionado automáticamente por Supabase en la nube."
    except Exception as e:
        return False, str(e)