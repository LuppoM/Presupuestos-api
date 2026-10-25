import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional

# Modelo de Materias Primas
from mpmodelo import (
    obtener_todas_materias_primas,
    obtener_materia_prima_por_id,
    insertar_materia_prima,
    actualizar_materia_prima,
    eliminar_materia_prima
)

# Modelo de Presupuestos
from presupuestosmodelo import (
    obtener_todos_presupuestos,
    obtener_presupuesto_por_id,
    obtener_detalles_presupuesto,
    guardar_presupuesto_completo,
    actualizar_presupuesto_completo,
    eliminar_presupuesto_completo
)

# Generador de PDF
from pdf import generar_pdf_presupuesto

app = FastAPI(title="API Tornería", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.path.exists("archivos"):
    app.mount("/archivos", StaticFiles(directory="archivos"), name="archivos")


# =========================================================
# SCHEMAS (PYDANTIC)
# =========================================================

class MateriaPrimaSchema(BaseModel):
    nombre: str
    unidad_medida: str
    precio_unitario: float

class DetallePresupuestoSchema(BaseModel):
    id_material: int
    cantidad: float
    precio_venta: float

class PresupuestoSchema(BaseModel):
    fecha: str
    cliente: str
    descripcion: str
    mano_obra: float
    total_materiales: float
    total_general: float
    detalles: List[DetallePresupuestoSchema]


# =========================================================
# RUTAS HTML (VISTAS)
# =========================================================

@app.get("/", response_class=FileResponse)
@app.get("/principal", response_class=FileResponse)
def servir_principal():
    return FileResponse(os.path.join(os.path.dirname(__file__), "Principal.html"))

@app.get("/materias_primas", response_class=FileResponse)
def servir_materias_primas():
    return FileResponse(os.path.join(os.path.dirname(__file__), "mp.html"))

@app.get("/presupuestos", response_class=FileResponse)
def servir_presupuestos():
    return FileResponse(os.path.join(os.path.dirname(__file__), "presupuestos.html"))


# =========================================================
# ENDPOINTS API - MATERIAS PRIMAS
# =========================================================

@app.get("/api/materias_primas")
def api_listar_materias_primas():
    try:
        data = obtener_todas_materias_primas()
        return {"materias_primas": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/materias_primas/{id_material}")
def api_obtener_materia_prima(id_material: int):
    data = obtener_materia_prima_por_id(id_material)
    if not data:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    return data

@app.post("/api/materias_primas")
def api_crear_materia_prima(material: MateriaPrimaSchema):
    try:
        nuevo_id = insertar_materia_prima(material.dict())
        return {"mensaje": "Guardado correctamente", "id_material": nuevo_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/materias_primas/{id_material}")
def api_actualizar_materia_prima(id_material: int, material: MateriaPrimaSchema):
    try:
        actualizar_materia_prima(id_material, material.dict())
        return {"mensaje": "Actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/materias_primas/{id_material}")
def api_eliminar_materia_prima(id_material: int):
    try:
        eliminar_materia_prima(id_material)
        return {"mensaje": "Eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================================================
# ENDPOINTS API - PRESUPUESTOS
# =========================================================

@app.get("/api/presupuestos")
def api_listar_presupuestos():
    try:
        data = obtener_todos_presupuestos()
        return {"presupuestos": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/presupuestos/{id_presupuesto}")
def api_obtener_presupuesto(id_presupuesto: int):
    cabecera = obtener_presupuesto_por_id(id_presupuesto)
    if not cabecera:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    detalles = obtener_detalles_presupuesto(id_presupuesto)
    return {"cabecera": cabecera, "detalles": detalles}

@app.post("/api/presupuestos")
def api_crear_presupuesto(p: PresupuestoSchema):
    try:
        datos = p.dict()
        detalles = datos.pop("detalles")
        nuevo_id = guardar_presupuesto_completo(datos, detalles)
        return {"mensaje": "Presupuesto guardado correctamente", "id_presupuesto": nuevo_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/presupuestos/{id_presupuesto}")
def api_actualizar_presupuesto(id_presupuesto: int, p: PresupuestoSchema):
    try:
        datos = p.dict()
        detalles = datos.pop("detalles")
        actualizar_presupuesto_completo(id_presupuesto, datos, detalles)
        return {"mensaje": "Presupuesto actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/presupuestos/{id_presupuesto}")
def api_eliminar_presupuesto(id_presupuesto: int):
    try:
        eliminar_presupuesto_completo(id_presupuesto)
        return {"mensaje": "Presupuesto eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/presupuestos/{id_presupuesto}/pdf")
def api_descargar_pdf_presupuesto(id_presupuesto: int):
    cabecera = obtener_presupuesto_por_id(id_presupuesto)
    if not cabecera:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    
    detalles = obtener_detalles_presupuesto(id_presupuesto)
    
    try:
        ruta_pdf = generar_pdf_presupuesto(cabecera, detalles)
        return FileResponse(
            ruta_pdf, 
            media_type="application/pdf", 
            filename=f"Presupuesto_{id_presupuesto}.pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el PDF: {str(e)}")