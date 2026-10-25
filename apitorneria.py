import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

# Importamos las funciones del modelo
from mpmodelo import (
    obtener_todas_materias_primas,
    obtener_materia_prima_por_id,
    insertar_materia_prima,
    actualizar_materia_prima,
    eliminar_materia_prima
)

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

class MateriaPrimaSchema(BaseModel):
    nombre: str
    unidad_medida: str
    precio_unitario: float

# Vistas HTML
@app.get("/", response_class=FileResponse)
@app.get("/principal", response_class=FileResponse)
def servir_principal():
    return FileResponse(os.path.join(os.path.dirname(__file__), "Principal.html"))

@app.get("/materias_primas", response_class=FileResponse)
def servir_materias_primas():
    return FileResponse(os.path.join(os.path.dirname(__file__), "mp.html"))

# Endpoints de API
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