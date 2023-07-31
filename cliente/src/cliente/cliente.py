import socket
from threading import Thread

SERVER_IP    = "127.0.0.1"
SERVER_PORT  = 3333
separador    = "<->"

server_socket = socket.socket()
server_socket.connect((SERVER_IP, SERVER_PORT))

print("[+] Conectado al servidor.")

usuario = input("Introduce tu nombre: ")
primer_envio = usuario + separador + "servidor" + separador + usuario
server_socket.send(primer_envio.encode())

destinatario = input("Usuario destinatario de los mensajes: ")

def get_mensajes():
    while True:
        mensaje_completo = server_socket.recv(1024).decode()

        emisor   = mensaje_completo.split(separador, 2)[0]
        receptor = mensaje_completo.split(separador, 2)[1] 
        mensaje  = mensaje_completo.split(separador, 2)[2]
        print("\n" + emisor + ": "+ mensaje)

thread = Thread(target=get_mensajes)
thread.daemon = True
thread.start()

while True:
    mensaje_enviar =  input()
    
    if mensaje_enviar.lower() == 'q':
        break

    envio = usuario + separador + destinatario + separador + mensaje_enviar
    server_socket.send(envio.encode())

server_socket.close()
