#!/usr/bin/env python

import socket
from Crypto.Cipher import AES
from threading import Thread
from biblioteca_cliente import *

server_socket = socket.socket()
server_socket.connect((SERVER_IP, SERVER_PORT))

print("[+] Conectado al servidor.")

usuario = input("Introduce tu nombre: ")

primer_envio = usuario + separador + "servidor" + separador + usuario + separador + " " + separador + " " 
server_socket.send(primer_envio.encode())

destinatario = input("Usuario destinatario de los mensajes: ")

def get_mensajes():
    while True:
        mensaje_completo = server_socket.recv(1024).decode()

        emisor   = mensaje_completo.split(separador, 4)[0]
        receptor = mensaje_completo.split(separador, 4)[1] 
        mensaje  = mensaje_completo.split(separador, 4)[2]
        tag      = mensaje_completo.split(separador, 4)[3]
        nonce    = mensaje_completo.split(separador, 4)[4]

        mensaje_descifrado = desencriptar(mensaje, "prueba", tag, nonce)

        print("\n" + emisor + ": "+ mensaje_descifrado)

thread = Thread(target=get_mensajes)
thread.daemon = True
thread.start()

while True:
    mensaje_enviar =  input()
    
    if mensaje_enviar.lower() == 'q':
        break

    mensaje_cifrado, tag, nonce = encriptar(mensaje_enviar, "prueba")

    envio = usuario + separador + destinatario + separador + mensaje_cifrado + separador + tag + separador + nonce

    server_socket.send(envio.encode())

server_socket.close()
