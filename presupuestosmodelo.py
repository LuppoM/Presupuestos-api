from conexion import conectar_db

def obtener_todos_presupuestos():
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id_presupuesto, fecha, cliente, descripcion, total_general 
                FROM presupuestos 
                ORDER BY id_presupuesto DESC;
            """)
            filas = cursor.fetchall()
            return [
                {
                    "id": f[0],
                    "fecha": f[1] or "",
                    "cliente": f[2] or "",
                    "descripcion": f[3] or "",
                    "total_general": float(f[4]) if f[4] is not None else 0.0
                }
                for f in filas
            ]

def obtener_presupuesto_por_id(id_presupuesto):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id_presupuesto, fecha, cliente, descripcion, mano_obra, total_materiales, total_general
                FROM presupuestos 
                WHERE id_presupuesto = %s;
            """, (id_presupuesto,))
            f = cursor.fetchone()
            if not f:
                return None
            return {
                "id_presupuesto": f[0],
                "fecha": f[1] or "",
                "cliente": f[2] or "",
                "descripcion": f[3] or "",
                "mano_obra": float(f[4]) if f[4] is not None else 0.0,
                "total_materiales": float(f[5]) if f[5] is not None else 0.0,
                "total_general": float(f[6]) if f[6] is not None else 0.0
            }

def obtener_detalles_presupuesto(id_presupuesto):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT pd.id_material, mp.nombre, mp.unidad_medida, pd.cantidad, pd.precio_venta
                FROM presupuesto_detalles pd
                INNER JOIN materias_primas mp ON pd.id_material = mp.id_material
                WHERE pd.id_presupuesto = %s;
            """, (id_presupuesto,))
            filas = cursor.fetchall()
            return [
                {
                    "id_material": f[0],
                    "nombre": f[1] or "",
                    "unidad": f[2] or "",
                    "cantidad": float(f[3]),
                    "precio_venta": float(f[4]),
                    "subtotal": float(f[3]) * float(f[4])
                }
                for f in filas
            ]

def guardar_presupuesto_completo(cabecera, detalles):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO presupuestos (fecha, cliente, descripcion, mano_obra, total_materiales, total_general)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_presupuesto;
            """, (
                cabecera["fecha"],
                cabecera["cliente"],
                cabecera["descripcion"],
                cabecera["mano_obra"],
                cabecera["total_materiales"],
                cabecera["total_general"]
            ))
            id_nuevo = cursor.fetchone()[0]

            for d in detalles:
                cursor.execute("""
                    INSERT INTO presupuesto_detalles (id_presupuesto, id_material, cantidad, precio_venta)
                    VALUES (%s, %s, %s, %s);
                """, (id_nuevo, d["id_material"], d["cantidad"], d["precio_venta"]))

            conn.commit()
            return id_nuevo

def actualizar_presupuesto_completo(id_presupuesto, cabecera, detalles):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE presupuestos
                SET fecha = %s, cliente = %s, descripcion = %s, mano_obra = %s, total_materiales = %s, total_general = %s
                WHERE id_presupuesto = %s;
            """, (
                cabecera["fecha"],
                cabecera["cliente"],
                cabecera["descripcion"],
                cabecera["mano_obra"],
                cabecera["total_materiales"],
                cabecera["total_general"],
                id_presupuesto
            ))

            cursor.execute("DELETE FROM presupuesto_detalles WHERE id_presupuesto = %s;", (id_presupuesto,))

            for d in detalles:
                cursor.execute("""
                    INSERT INTO presupuesto_detalles (id_presupuesto, id_material, cantidad, precio_venta)
                    VALUES (%s, %s, %s, %s);
                """, (id_presupuesto, d["id_material"], d["cantidad"], d["precio_venta"]))

            conn.commit()
            return True

def eliminar_presupuesto_completo(id_presupuesto):
    with conectar_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM presupuesto_detalles WHERE id_presupuesto = %s;", (id_presupuesto,))
            cursor.execute("DELETE FROM presupuestos WHERE id_presupuesto = %s;", (id_presupuesto,))
            conn.commit()
            return True