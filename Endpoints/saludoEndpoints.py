from fastapi import APIRouter
import Servicios.saludoServicios as saludoServicio

saludoRouter = APIRouter()

@saludoRouter.get("/Saludar")
def get_saludo(nombre: str):

    saludo = None


    saludo = saludoServicio.get_saludo_complejo(nombre)

    return saludo

@saludoRouter.get("/saludo_Normal")
def  get_saludo_sencillo():

    saludo_sencillo = None

    saludo_sencillo = saludoServicio.get_saludo()

    return saludo_sencillo