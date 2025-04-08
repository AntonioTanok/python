from fastapi import APIRouter
import Servicios.dineroServicios as dineroServicios

dineroRouter = APIRouter()

@dineroRouter.get("/balance")
def get_balance(userid: int):
    #inicializa
    saldo = None

    #intentar asignar valor
    saldo = dineroServicios.get_fondo_usuario(userid)

    #returnar
    return saldo


