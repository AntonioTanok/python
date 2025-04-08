# Endpoints/usuarioEndpoints.py

from fastapi import APIRouter
import Servicios.usuariosServicios as usuarioServicio
from pydantic import BaseModel, EmailStr

usuarioRouter = APIRouter()

class Usuario(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "user"

class UsuarioActualizar(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

@usuarioRouter.get("/usuarios")
def obtener_usuarios():

    usuarios = []

    usuario = usuarioServicio.get_todos_los_usuarios()

    return usuario

@usuarioRouter.post("/registrar")
def crear_usuario_endpoint(usuario: Usuario):
    return usuarioServicio.crear_usuario(
        usuario.name,
        usuario.email,
        usuario.password,
        usuario.role
    )

@usuarioRouter.put("/editar/{id}")
def actualizar_usuario(id: int, usuario: UsuarioActualizar):
    return usuarioServicio.editar_usuario(
        id,
        usuario.name,
        usuario.email,
        usuario.password,
        usuario.role
    )

@usuarioRouter.delete("/eliminar/{id}")
def eliminar_usuario_endpoint(id: int):
    return usuarioServicio.eliminar_usuario(id)









# @usuarioRouter.get("/usuarios/{user_id}")
# def obtener_usuario_por_id(user_id: int):

#     return usuarioServicio.get_usuario_por_id(user_id)
