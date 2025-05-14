# Endpoints/usuarioEndpoints.py

from fastapi import APIRouter
import Servicios.usuariosServicios as usuarioServicio
from pydantic import BaseModel, EmailStr
from modelos.usuarioModel import LoginRequest
from fastapi import Depends
from utils.auth import verificar_token


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

class CredencialesUsuario(BaseModel):
    email: EmailStr
    password: str


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


@usuarioRouter.post("/login")
def login_usuario(credenciales: CredencialesUsuario):
    return usuarioServicio.iniciar_sesion(
        credenciales.email,
        credenciales.password
    )



@usuarioRouter.get("/perfil")
def perfil_usuario(usuario = Depends(verificar_token)):
    return {
        "usuario_id": usuario["user_id"],
        "nombre": usuario["name"],
        "email": usuario["email"],
        "sesion_inicio": usuario["fecha_inicio"]
    }








# @usuarioRouter.post("/login")
# def login(request: LoginRequest):
#     return usuarioServicio.login_usuario(request.email, request.password)



# @usuarioRouter.get("/usuarios/{user_id}")
# def obtener_usuario_por_id(user_id: int):

#     return usuarioServicio.get_usuario_por_id(user_id)
