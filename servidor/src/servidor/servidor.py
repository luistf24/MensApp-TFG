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
    while True:
        try:
            mensaje_completo = sc.recv(1024).decode()

        except Exception as error:
            print("[!] Error: {}".format(error))

        else:
            if separador in mensaje_completo:
                emisor   = mensaje_completo.split(separador, 2)[0]
                receptor = mensaje_completo.split(separador, 2)[1] 
                mensaje  = mensaje_completo.split(separador, 2)[2]
            else:
                receptor = "NotFoundError"

            if(receptor == "servidor"): # Almacenamos el id del usuario, este caso solo se da cuando se regis-
                                        # tra un usuario con un id que se almacenará en el mensaje sin cifrar.
                sockets_usuarios[sc] = mensaje 

            else:
                temp = False
                for socket_usuario, usuario_id in sockets_usuarios.items():

                    if(receptor == usuario_id): 
                        socket_usuario.send(mensaje_completo.encode())
                        temp = True

                    # if(temp == False):
                        # no_enviado = "servidor" + separador + emisor + separador + noreceptor + receptor
                        # sc.send(no_enviado.encode())


while True:
    socket_cliente, direccion_cliente = socket_servidor.accept()

    print("[+] {} se ha conectado.".format(direccion_cliente))

    sockets_usuarios[socket_cliente] = "UsuarioTemporal"

    thread = Thread(target=escuchar_clientes, args=(socket_cliente,))
    thread.daemon = True
    thread.start()

for usuario in sockets_usuarios.keys():
    usuario.close()

socket_servidor.close()
                    
