import bcrypt
import secrets
from fastapi import HTTPException

from fastapi import Request

from datetime import datetime
from Servicios.usuariosServicios import get_db_connection  # Asegúrate de tener este método definido

def login_usuario(email: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Buscar el usuario por email
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    usuario = cursor.fetchone()

    if not usuario:
        raise HTTPException(status_code=401, detail="Correo no registrado")

    # Verificar la contraseña
    if not bcrypt.checkpw(password.encode('utf-8'), usuario['password'].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    # Generar token
    token = secrets.token_hex(32)

    # Registrar la sesión
    cursor.execute("""
        INSERT INTO sesiones (user_id, token)
        VALUES (%s, %s)
    """, (usuario['id'], token))
    conn.commit()

    # Devolver datos del usuario y token

    
    return {
        "id": usuario['id'],
        "nombre": usuario['nombre'],
        "email": usuario['email'],
        "role": usuario['perfil'],  # O 'role' según tu campo
        "mensaje": "Inicio de sesión exitoso",
        "token": token
    }


# Simulación de verificación de token desde la tabla de sesiones
def verificar_token(token: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sesiones WHERE token = %s", (token,))
    sesion = cursor.fetchone()

    if not sesion:
        raise HTTPException(status_code=401, detail="Token inválido o sesión no encontrada")

    # Si lo necesitas, podrías incluso obtener el usuario relacionado
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (sesion['user_id'],))
    usuario = cursor.fetchone()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado para el token")

    return usuario  # Puedes retornar el usuario, el token o lo que necesites