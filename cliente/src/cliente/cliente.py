#!/usr/bin/env python

import socket
from Crypto.Cipher import AES
from threading import Thread
from biblioteca_cliente import *
import random

server_socket = socket.socket()
server_socket.connect((SERVER_IP, SERVER_PORT))

print("[+] Conectado al servidor.")

usuario = input("Introduce tu nombre: ")

primer_envio = usuario + separador + "servidor" + separador + usuario + separador + " " + separador + " " 
server_socket.send(primer_envio.encode())

destinatario = input("Usuario destinatario de los mensajes: ")



cifrado = False

clave = random.randint(1, 9)


def get_mensajes():
    global clave
    global cifrado

    while True:
        mensaje_completo = server_socket.recv(1024).decode()

        emisor   = mensaje_completo.split(separador, 4)[0]
        receptor = mensaje_completo.split(separador, 4)[1] 
        mensaje  = mensaje_completo.split(separador, 4)[2]
        tag      = mensaje_completo.split(separador, 4)[3]
        nonce    = mensaje_completo.split(separador, 4)[4]

        if(tag == "intercambio"):
            # Si este cliente no ha mandado el mensaje inicial, entonces envía su clave
            if cifrado == False:
                print("\n" + emisor + ": "+ mensaje)
                envio = usuario + separador + destinatario + separador + "  " + separador + "intercambio" + separador + str(clave) 
                server_socket.send(envio.encode())
                cifrado = True

            # Operación para obtener la clave común
            clave = clave * int(nonce)

        else:
            mensaje_descifrado = desencriptar(mensaje, str(clave), tag, nonce)
            print("\n" + emisor + ": "+ mensaje_descifrado)

thread = Thread(target=get_mensajes)
thread.daemon = True
thread.start()

while True:
    mensaje_enviar =  input()
    
    if mensaje_enviar.lower() == 'q':
        break

    if cifrado:
        mensaje_cifrado, tag, nonce = encriptar(mensaje_enviar, str(clave))
        envio = usuario + separador + destinatario + separador + mensaje_cifrado + separador + tag + separador + nonce

        server_socket.send(envio.encode())

    # Si el usuario inicia la conversación, envía un primer mensaje sin cifrar, una vez recibido empieza el intercambio de claves
    else:
        envio = usuario + separador + destinatario + separador + mensaje_enviar + separador + "intercambio" + separador + str(clave)
        server_socket.send(envio.encode())
        cifrado = True

server_socket.close()
