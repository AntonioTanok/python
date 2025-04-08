import Endpoints.usuarioEndpoints as usuarioEndpoint

# ...
app.include_router(usuarioEndpoint.usuarioRouter, tags=["Usuarios"])
