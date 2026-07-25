import socket
import threading

# Configuración del socket de red (IPv4, TCP)
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Opción para liberar el puerto inmediatamente tras apagar el servidor
socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
socket_servidor.bind(('localhost', 12345))
socket_servidor.listen()
print("[*] Servidor encendido en el puerto 12345. Esperando conexiones...")

# Estructura global en memoria para registrar clientes activos
lista_de_clientes = []

def broadcast(mensaje_en_bytes, socket_emisor):
    """Retransmite los datos recibidos a todos los clientes excepto al emisor."""
    for socket_receptor in lista_de_clientes:  
        if socket_receptor != socket_emisor:
            try:
                socket_receptor.send(mensaje_en_bytes) 
            except:
                # Limpieza automática: remueve sockets rotos o inactivos
                if socket_receptor in lista_de_clientes: 
                    lista_de_clientes.remove(socket_receptor)

def atender_cliente_en_hilo(socket_del_cliente):
    """Maneja de forma asíncrona la recepción de datos de un cliente específico."""
    while True:
        try:
            # Operación I/O bloqueante (espera de datos en red)
            mensaje_recibido_en_bytes = socket_del_cliente.recv(1024)
            
            # Detección de desconexión limpia (paquete TCP FIN)
            if not mensaje_recibido_en_bytes: 
                break 
                
            broadcast(mensaje_recibido_en_bytes, socket_del_cliente)
        except:
            # Captura desconexiones abruptas (caídas de red o cierres forzados)
            print("El cliente se desconecto abruptamente")
            break 
            
    # Clausura del socket y remoción de la lista global
    if socket_del_cliente in lista_de_clientes: 
        lista_de_clientes.remove(socket_del_cliente)
    socket_del_cliente.close()
    print("[-] Conexión cerrada de forma segura.")

# Bucle principal: Acepta clientes y delega su atención a hilos dedicados
while True:
    try:
        # Bloqueo en espera del saludo de tres vías (TCP Handshake)
        socket_del_cliente, datos_de_conexion = socket_servidor.accept()
        print(f"[+] Conexión aceptada desde: {datos_de_conexion}")
        
        lista_de_clientes.append(socket_del_cliente)
        
        # Concurrencia mediante hilos demonio asignados a cada sesión de usuario
        hilo_atencion = threading.Thread(target=atender_cliente_en_hilo, args=(socket_del_cliente,), daemon=True)
        hilo_atencion.start()
    except:
        break