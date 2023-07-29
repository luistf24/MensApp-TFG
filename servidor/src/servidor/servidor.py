import socket
from threading import Thread
from biblioteca_servidor import *


# Diccionario donde se van a almacenar los sockets de los usuarios, SocketCliente:UsuarioCliente
sockets_usuarios = {}

socket_servidor = socket.socket()
socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_servidor.bind((SERVER_IP, SERVER_PORT))

socket_servidor.listen(5)

def escuchar_clientes(sc):
    try:
        mensaje = sc.recv(1024).decode()
    
    except Exception as error:
        print("[!] Error: {error}")

    else:
        emisor   = mensaje.split(separador, 2)[0]
        receptor = mensaje.split(separador, 2)[1] 
        mensaje  = mensaje.split(separador, 2)[2]

        if(receptor == "servidor"): # Almacenamos el id del usuario, este caso solo se da cuando se regis-
                                    # tra un usuario con un id que se almacenará en el mensaje sin cifrar.
           sockets_usuarios[sc] = mensaje 

        else:
            temp = False
            for usuario in sockets_usuarios.keys():
                if(receptor == sockets_usuarios[usuario]):
                    usuario.send(msg.encode())
                    temp = True

            if(temp == False):
                no_enviado = "servidor" + separador + emisor + separador + noreceptor + receptor
                sc.send(no_enviado.encode())


while True:
    socket_cliente, direccion_cliente = socket_servidor.accept()

    print("[+] {direccion_cliente} se ha conectado.")

    sockets_usuarios[socket_cliente] = "UsuarioTemporal"

    thread = Thread(target=escuchar_clientes, args=(socket_cliente,))
    thread.daemon = True
    thread.start()

for usuario in sockets_usuarios.keys():
    usuario.close()

socket_servidor.close()
                    
