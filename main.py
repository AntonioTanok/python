from fastapi import FastAPI
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

# Incluir los routers
app.include_router(dineroEndpoint.dineroRouter, tags=["Dinero"])

app.include_router(saludoEndpoint.saludoRouter, tags=["Saludar"])


import Endpoints.usuarioEndpoints as usuarioEndpoint

# ...
app.include_router(usuarioEndpoint.usuarioRouter, tags=["Usuarios"])
