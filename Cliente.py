import socket

miSocket=socket.socket()
miSocket.connect(('localhost',8000))# hacemos la conexion recibe una tupla, direccion a la que necesitamos conectar, puerto para realizar la conexion
miSocket.send(b"Hola desde el cliente") #  Agregamos la 'b'. Ahora envía BYTES.

datos_recibidos = miSocket.recv(1024) #  Paso 1: Recibe los bytes puros del servidor.
respuesta = datos_recibidos.decode('utf-8') #  Paso 2: Transforma esos bytes a texto limpio.

print("Respuesta del servidor:", respuesta)
miSocket.close()#Cerramos la conexion



#miSocket.send(b"Hola desde el cliente")
#respuesta = miSocket.recv(1024).decode('utf-8')#para recibir lo que un socket nos esa enviando metodo recv hacemos referencia al buffer 1024 rack
