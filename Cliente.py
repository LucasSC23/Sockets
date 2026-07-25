import socket
import threading
import sys
import time


# Movimos esto aquí afuera para que no te vuelva a pedir el nombre en cada reconexión.
nombre_usuario = input("Ingresá tu nombre o nickname para el chat: ")
if not nombre_usuario.strip():
    nombre_usuario = "Anónimo"
print(f"[+] Bienvenido {nombre_usuario}. Escribí tu mensaje o usa el comando /exit para salir.\n")


# ==============================================================================
# 🚨 SECCIÓN 1: EL BUCLE MAESTRO (NUEVA ESTRUCTURA)
# ==============================================================================
while True: # Atrapa el programa en un ciclo infinito para que no muera.
    chat_activo = True
    
    # 🆕 [LÍNEA MOVIDA AQUÍ ADENTRO]: Cada vez que el bucle da la vuelta, 
    # crea un objeto socket desde cero (el enchufe nuevo).
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("[*] Esperando a que el servidor esté activo...")
    while True:
        try:
            socket_cliente.connect(('localhost', 12345))
            print("[+] ¡Conectado al servidor! Podés chatear.")
            break 
        except:
            time.sleep(3) # Bucle de reintentos infinitos cada 3 segundos.

    def escuchar_servidor_en_hilo():
        global chat_activo
        while chat_activo:
            try:
                mensaje_entrante = socket_cliente.recv(1024)
                if not mensaje_entrante or not chat_activo:
                    break
                print(f"\n{mensaje_entrante.decode('utf-8')}\n> ", end="")
            except:
                break
                
        if chat_activo:
            print("\n[!] El servidor se apagó repentinamente.")
            print("[*] Presioná ENTER para reconectar o escribí '/exit' para salir.")
            #  El hilo de red le avisa al del teclado que el server murió.
            chat_activo = False 

    threading.Thread(target=escuchar_servidor_en_hilo).start()

    try:
        while chat_activo:
            texto_ingresado = input("> ")
            
            # ==============================================================================
            # 🚨 SECCIÓN 2: EL BLOQUE DE EVALUACIÓN POST-CAÍDA (NUEVA LÓGICA)
            # ==============================================================================
            #Se ejecuta justo cuando el usuario presiona ENTER
            # después de que el servidor se cayó.
            if not chat_activo:
                opcion = texto_ingresado.strip().lower()
                if opcion in ["/exit", "s", "salir"]:
                    print("[*] Has decidido salir. Cerrando el programa...")
                    socket_cliente.close()
                    sys.exit(0) 
                else:
                    print("[*] Iniciando proceso de reconexión...")
                    # 🆕 [LÍNEA CLAVE]: Rompe el bucle de mensajes actual para saltar 
                    # a la limpieza e ir directo al Bucle Maestro de arriba.
                    break 
            # ==============================================================================

            if texto_ingresado.strip().lower() == "/exit":
                print("[*] Saliendo del chat...")
                chat_activo = False
                socket_cliente.close()
                sys.exit(0)

            if texto_ingresado.strip():
                try:
                    mensaje_formateado = f"[{nombre_usuario}]: {texto_ingresado}"
                    socket_cliente.send(mensaje_formateado.encode('utf-8'))
                except:
                    break 
                    
    except KeyboardInterrupt:
        print("\n[*] Saliendo del chat de forma segura (Ctrl+C)...")
        chat_activo = False
        socket_cliente.close()
        sys.exit(0)

    # ==============================================================================
    # 🚨 SECCIÓN 3: LIMPIEZA ANTES DEL REINICIO
    # ==============================================================================
    #Al llegar acá (gracias al 'break' de la Sección 2),
    # apagamos todo formalmente, cerramos el socket roto y dejamos que el código 
    # "toque el fondo" del while True para volver a empezar desde la Sección 1.
    chat_activo = False
    socket_cliente.close()