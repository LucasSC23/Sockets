'''COMPLETA LA FUNCION FALTANTE '''

import socket
import threading


# --- Configuración del cliente ---
HOST = '127.0.0.1'
PORT = 12345

def crear_socket_cliente(socket_cliente):
    socket_cliente=socket.socket(SOCK_AFINET,SOCK_STREAM)
    socket_cliente.connect(HOST),(PORT)
    print(f"Conexion exitosa{HOST}{PORT}")
    return socket_cliente
#--------------------------------------------------------------
# funcion crear_socket_cliente():
#     # Crear un socket TCP
#     cliente = ???  # Usar socket.socket con parámetros para TCP

#     # Conectar el socket al servidor usando HOST y PORT

#     # Mostrar mensaje de conexión exitosa al servidor {HOST}:{PORT}

#     # Devolver el socket creado y conectado
#---------------------------------------------------------------

def recibir_mensajes(socket_cliente):
    """Bucle para recibir mensajes del servidor."""
    while True:
        try:
            mensaje = socket_cliente.recv(1024).decode('utf-8')
            if not mensaje:
                print("[i] Conexión cerrada por el servidor.")
                break
            print(mensaje)
        except:
            print("[!] Error al recibir mensaje. Cerrando conexión.")
            break

def enviar_mensajes(socket_cliente):
    """Bucle para enviar mensajes al servidor."""
    try:
        while True:
            mensaje = input()
            if mensaje.strip().lower() == "/salir":
                print("[i] Cerrando conexión...")
                break
            socket_cliente.send(mensaje.encode('utf-8'))
    except KeyboardInterrupt:
        print("\n[i] Interrupción por teclado. Cerrando conexión...")

def iniciar_cliente():
    # TODO crear socket  
    socket_cliente = crear_socket_cliente()

    #TODO  Crear hilo para escuchar mensajes entrantes
    hilo_recepcion =threading.Thread(target=(recibir_mensajes),args=(socket_cliente,))
    hilo_recepcion.daemon = True
    hilo_recepcion.start()

    #TODO Enviar mensajes en el hilo principal
    mensaje_enviado=enviar_mensajes(socket_cliente)

    #TODO Cerrar conexión al salir
    socket_cliente.close()
    
    print("[-] Desconectado del servidor.")

if __name__ == "__main__":
    iniciar_cliente()