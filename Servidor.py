#Genero un servidor utilizando sockets
import socket

miSocket = socket.socket() #generamos un nuevo socket con los valores de default
miSocket.bind(('localhost',8000))#conexion, recibe una tupla, 1) el host, 2) en que puesto estan escuchando el socket
miSocket.listen(5)#cantidad de peticiones que uede manejar nuestro socket en cola
while True:
    conexion, addr= miSocket.accept()#aceptamos las peticiones retorna dos valores
    print ("Nueva conexion establecida")
    print (addr)#Imprimimos la direccion en la cual se hizo la peticion


    datos_recibidos = conexion.recv(1024) #  Paso 1: Guarda los bytes que envió el cliente.
    mensaje_cliente = datos_recibidos.decode('utf-8') #  Paso 2: Los decodifica de forma segura.
    print("El cliente dice:", mensaje_cliente)

    conexion.send(b"Hola, te saludo desde el servidor")#Enviamos una peticio al cliente
    conexion.close()#Cerramos la conexion con el cliente

    
    #Recibimos lo que el cliente nos mandó (¡importante!)
    #mensaje_cliente = conexion.recv(1024).decode('utf-8')
    #print("El cliente dice:", mensaje_cliente.decode('utf-8')) # .decode() pasa de bytes a texto
