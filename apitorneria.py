from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from conexion import conectar_db

app = FastAPI(
    title="API Tornería",
    description="Endpoints para la interfaz principal del sistema de tornería",
    version="1.0.0"
)

# Permitir solicitudes desde el frontend HTML
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Endpoint de estado de la API / Base de Datos
@app.get("/api/estado")
def obtener_estado_conexion():
    try:
        with conectar_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                return {
                    "status": "ok",
                    "mensaje": "Conexión a Supabase exitosa",
                    "version_pg": version[0]
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {str(e)}")

# 2. Endpoint para obtener resumen/estado de Presupuestos (badge del menú)
@app.get("/api/presupuestos/resumen")
def resumen_presupuestos():
    try:
        with conectar_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM presupuestos;")
                total = cursor.fetchone()[0]
                
                return {
                    "total_presupuestos": total,
                    "estado": "OK"
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener presupuestos: {str(e)}")

# 3. Endpoint para listar Materias Primas
@app.get("/api/materias_primas")
def listar_materias_primas():
    try:
        with conectar_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id_material, nombre, unidad_medida, precio_unitario FROM materias_primas ORDER BY nombre ASC;"
                )
                filas = cursor.fetchall()
                materiales = [
                    {
                        "id_material": f[0],
                        "nombre": f[1],
                        "unidad_medida": f[2],
                        "precio_unitario": float(f[3]) if f[3] is not None else 0.0
                    }
                    for f in filas
                ]
                return {"materias_primas": materiales}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar materias primas: {str(e)}")

# 4. Endpoint para listar Presupuestos
@app.get("/api/presupuestos")
def listar_presupuestos():
    try:
        with conectar_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id_presupuesto, fecha, cliente, descripcion, mano_obra, total_materiales, total_general "
                    "FROM presupuestos ORDER BY id_presupuesto DESC;"
                )
                filas = cursor.fetchall()
                presupuestos = [
                    {
                        "id_presupuesto": f[0],
                        "fecha": f[1],
                        "cliente": f[2],
                        "descripcion": f[3],
                        "mano_obra": float(f[4]) if f[4] is not None else 0.0,
                        "total_materiales": float(f[5]) if f[5] is not None else 0.0,
                        "total_general": float(f[6]) if f[6] is not None else 0.0
                    }
                    for f in filas
                ]
                return {"presupuestos": presupuestos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar presupuestos: {str(e)}")