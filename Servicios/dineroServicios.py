
def get_fondo_usuario(userid: int):
    #inicializar lo que pienso devolver
    fondo_usuario = None
    
    #intentar obtener lo que voy a devolver
    try:
        if(userid == 1):
            fondo_usuario = 1000
        elif(userid == 2):
            fondo_usuario = 500
        elif(userid == 3):
         fondo_usuario = 100
    except Exception as e:
        fondo_usuario = None

    #devolver lo obtenido
    return fondo_usuario    
      
   