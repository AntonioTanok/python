from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils.auth import login_usuario
from fastapi.middleware.cors import CORSMiddleware
import Endpoints.dineroEndpoints as dineroEndpoint
import Endpoints.saludoEndpoints as saludoEndpoint

app = FastAPI()
# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiar "*" por dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelo de entrada
class LoginInput(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(input: LoginInput):
    return login_usuario(input.email, input.password)















# Incluir los routers
app.include_router(dineroEndpoint.dineroRouter, tags=["Dinero"])

app.include_router(saludoEndpoint.saludoRouter, tags=["Saludar"])


import Endpoints.usuarioEndpoints as usuarioEndpoint

# ...
app.include_router(usuarioEndpoint.usuarioRouter, tags=["Usuarios"])
