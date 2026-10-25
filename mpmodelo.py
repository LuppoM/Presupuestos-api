from conexion import conectar_db

def obtener_todas_materias_primas():
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id_material, nombre, unidad_medida, precio_unitario FROM materias_primas ORDER BY id_material ASC;"
            )
            filas = cursor.fetchall()
            return [
                {
                    "id_material": f[0],
                    "nombre": f[1] or "",
                    "unidad_medida": f[2] or "",
                    "precio_unitario": float(f[3]) if f[3] is not None else 0.0
                }
                for f in filas
            ]

def obtener_materia_prima_por_id(id_material):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id_material, nombre, unidad_medida, precio_unitario FROM materias_primas WHERE id_material = %s;",
                (id_material,)
            )
            f = cursor.fetchone()
            if not f:
                return None
            return {
                "id_material": f[0],
                "nombre": f[1] or "",
                "unidad_medida": f[2] or "",
                "precio_unitario": float(f[3]) if f[3] is not None else 0.0
            }

def insertar_materia_prima(datos):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO materias_primas (nombre, unidad_medida, precio_unitario) VALUES (%s, %s, %s) RETURNING id_material;",
                (datos["nombre"], datos["unidad_medida"], datos["precio_unitario"])
            )
            nuevo_id = cursor.fetchone()[0]
            conn.commit()
            return nuevo_id

def actualizar_materia_prima(id_material, datos):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE materias_primas SET nombre = %s, unidad_medida = %s, precio_unitario = %s WHERE id_material = %s;",
                (datos["nombre"], datos["unidad_medida"], datos["precio_unitario"], id_material)
            )
            conn.commit()
            return True

def eliminar_materia_prima(id_material):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM materias_primas WHERE id_material = %s;", (id_material,))
            conn.commit()
            return True