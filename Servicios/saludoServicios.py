def get_saludo(): 
    #Inicializar lo que pienso devolver
    saludo_saludo = None
    print("saludo 1", saludo_saludo)

    #intentar asignar valores a lo que uqiero devolver
    try:
        
        saludo_saludo = "valor de  Saludo"
        print("saludo 2", saludo_saludo)
    
    except Exception as error:

        saludo_saludo = None
        print("saludo 3", saludo_saludo)


    print("saludo 4", saludo_saludo)
    return saludo_saludo


def get_saludo_complejo(nombre: str): 
    #Inicializar lo que pienso devolver
    saludo_nombre = None
    print("saludo_nombre", saludo_nombre)

    #intentar asignar valores a lo que uqiero devolver
    try:
        
        saludo_nombre = "hola " + nombre
        print("saludo_nombre", saludo_nombre)
    
    except Exception as error:

        saludo_nombre = None
        print("saludo_nombre", saludo_nombre)


    print("saludo_nombre", saludo_nombre)
    return saludo_nombre

