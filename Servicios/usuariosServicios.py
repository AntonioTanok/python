# Servicios/usuarioServicios.py
import mysql.connector
from fastapi import FastAPI, HTTPException, Depends
import bcrypt
import secrets
import datetime



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
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') #Agregue esto
        cursor.execute(
            "INSERT INTO usuarios (name, email, password, role) VALUES (%s, %s, %s, %s)",
            (nombre, email, hashed_password, role)
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




################### Agregue esto #####################
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



################### Agregue esto #####################
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

################### Agregue esto #####################
def iniciar_sesion(email: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id, name, email, role, password FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if not bcrypt.checkpw(password.encode('utf-8'), usuario["password"].encode('utf-8')):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

        # Devolver solo los datos necesarios (sin la contraseña)
        return {
            "id": usuario["id"],
            "nombre": usuario["name"],
            "email": usuario["email"],
            "role": usuario["role"],
            "mensaje": "Inicio de sesión exitoso"
        }

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {err}")
    finally:
        cursor.close()
        conn.close()


################### Agregue esto ##################### 
##Codigo para revisar
def login_usuario(email: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Obtener el usuario por email
        cursor.execute("SELECT id, name, password FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        # Verificar existencia y contraseña
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        # Generar token y registrar sesión
        token = secrets.token_hex(32)
        fecha_inicio = datetime.datetime.now()
        status = 1

        cursor.execute(
            "INSERT INTO sesiones (user_id, token, fecha_inicio, status) VALUES (%s, %s, %s, %s)",
            (user["id"], token, fecha_inicio, status)
        )
        conn.commit()

        return {"token": token, "name": user["name"]}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al iniciar sesión: {str(e)}")
    finally:
        cursor.close()
        conn.close()


