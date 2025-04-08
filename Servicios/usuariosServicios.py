# Servicios/usuarioServicios.py
import mysql.connector
from fastapi import FastAPI, HTTPException, Depends


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "sistema_ejemplo2"
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def get_todos_los_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener todos los usuarios
    cursor.execute("SELECT id, name, email, role FROM usuarios")  # Asegúrate de que tu tabla 'usuarios' tenga estas columnas
    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    if not usuarios:
        raise HTTPException(status_code=404, detail="No hay usuarios disponibles")

    return usuarios



def crear_usuario(nombre: str, email: str, password: str, role: str = "user"):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (name, email, password, role) VALUES (%s, %s, %s, %s)",
            (nombre, email, password, role)
        )
        conn.commit()
        return {"mensaje": "Usuario creado correctamente"}
    except mysql.connector.IntegrityError as err:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Ya existe un usuario con ese email: {err}")
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {err}")
    finally:
        cursor.close()
        conn.close()


def editar_usuario(id: int, nombre: str, email: str, password: str, role: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            UPDATE usuarios
            SET name = %s, email = %s, password = %s, role = %s
            WHERE id = %s
            """,
            (nombre, email, password, role, id)
        )
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return {"mensaje": "Usuario actualizado correctamente"}
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {err}")
    finally:
        cursor.close()
        conn.close()


def eliminar_usuario(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return {"mensaje": f"Usuario con ID {id} eliminado correctamente"}
    except mysql.connector.Error as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {err}")
    finally:
        cursor.close()
        conn.close()
