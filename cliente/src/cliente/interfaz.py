from tkinter import *
import socket
from threading import Thread
import random

from biblioteca_cliente import *
from interfaz import *


BG_NARANJA = "#F38016"
BG_AZUL = "#004080"
BG_BLANCO = "#ffffff"
BG_GRIS = "#AFAFAF"
TEXT_COLOR = "#EAECEE"
 
FONT = "Roboto 14"
FONT_BOLD = "Helvetica 13 bold"
 

class Ventana1:
    def __init__(self, master, server_socket, emisor, receptor):
        self.usuario = emisor
        self.receptor = receptor
        self.server_socket = server_socket

        self.clave = random.randint(1, 12)
        self.generador = 2
        self.cifrado = False

        self.master = master
        self.frame = Frame(self.master)
        self.label1 = Label(self.master, bg=BG_AZUL, fg=BG_NARANJA, text="Usuario: " + self.usuario, font=FONT_BOLD, pady=10, width=20, height=1).grid(row=0, column=0)
        
        self.txt = Text(self.master, bg=BG_AZUL, fg=BG_BLANCO, font=FONT, width=60)
        self.txt.grid(row=1, column=0, columnspan=2)

        self.scrollbar = Scrollbar(self.txt)
        self.scrollbar.place(relheight=1, relx=0.974)

        self.entrada = Entry(self.master, bg=BG_AZUL, fg=BG_BLANCO, font=FONT, width=55)
        self.entrada.grid(row=2, column=0)

        self.send = Button(self.master, text="Enviar", font=FONT_BOLD, bg=BG_BLANCO, fg=BG_NARANJA, command=self.enviar).grid(row=2, column=1)

        self.thread = Thread(target=self.get_mensajes)
        self.thread.daemon = True
        self.thread.start()

    def enviar(self):
        mensaje_enviar = self.entrada.get()
        self.txt.insert(END, "\n" + self.usuario + ": "+ mensaje_enviar)
        self.entrada.delete(0, END)

        if self.cifrado:
            mensaje_cifrado, tag, nonce = encriptar(mensaje_enviar, str(self.clave))
            envio = self.usuario + separador + self.receptor + separador + mensaje_cifrado + separador + tag + separador + nonce

            self.server_socket.send(envio.encode())

        # Si el usuario inicia la conversación, envía un primer mensaje sin cifrar, una vez recibido empieza el intercambio de claves
        else:
            envio = self.usuario + separador + self.receptor + separador + mensaje_enviar + separador + "intercambio" + separador + str(pow(self.generador, self.clave, 13))
            self.server_socket.send(envio.encode())
            self.cifrado = True

    def get_mensajes(self):

        while True:
            mensaje_completo = self.server_socket.recv(1024).decode()

            emisor   = mensaje_completo.split(separador, 4)[0]
            receptor = mensaje_completo.split(separador, 4)[1] 
            mensaje  = mensaje_completo.split(separador, 4)[2]
            tag      = mensaje_completo.split(separador, 4)[3]
            nonce    = mensaje_completo.split(separador, 4)[4]

            if(tag == "intercambio"):
                # Si este cliente no ha mandado el mensaje inicial, entonces envía su clave
                if self.cifrado == False:
                    self.txt.insert(END, "\n" + emisor + ": "+ mensaje)
                    envio = self.usuario + separador + self.receptor + separador + "  " + separador + "intercambio" + separador + str(pow(self.generador, self.clave, 13)) 
                    self.server_socket.send(envio.encode())
                    self.cifrado = True

                # Operación para obtener la clave común
                self.clave = pow(int(nonce), self.clave, 13)

            else:
                mensaje_descifrado = desencriptar(mensaje, str(self.clave), tag, nonce)
                self.txt.insert(END, "\n" + emisor + ": "+ mensaje_descifrado)


class Ventana2:
    def __init__(self, master, server_socket):
        self.usuario = "temporal"
        self.receptor = "temporal"

        self.server_socket = server_socket
        self.master = master
        self.frame = Frame(self.master, bg='white')
        self.label1 = Label(self.master, bg=BG_BLANCO, fg=BG_AZUL, text="MensApp", font=FONT_BOLD, pady=10, width=20, height=1).grid(row=0, column=0)

        self.label_usuario = Label(self.master, bg=BG_AZUL, fg=BG_BLANCO, text="Usuario emisor:", font=FONT_BOLD, pady=5, width=20).grid(row=2, column=0)
        self.label_destinatario = Label(self.master, bg=BG_AZUL, fg=BG_BLANCO, text="Usuario receptor:", font=FONT_BOLD, pady=5, width=20).grid(row=3, column=0)

        self.entrada_emisor = Entry(self.master, bg=BG_GRIS, fg=TEXT_COLOR, font=FONT, width=55)
        self.entrada_emisor.grid(row=2, column=1)

        self.entrada_receptor = Entry(self.master, bg=BG_GRIS, fg=TEXT_COLOR, font=FONT, width=55)
        self.entrada_receptor.grid(row=3, column=1)

        self.send = Button(self.master, text="Aceptar", font=FONT_BOLD, fg=BG_NARANJA, bg=BG_AZUL,command=self.new_window).grid(row=4, column=1, sticky="nsew")

    def new_window(self):
        self.usuario = self.entrada_emisor.get()
        self.receptor = self.entrada_receptor.get()

        primer_envio = self.usuario + separador + "servidor" + separador + self.usuario + separador + " " + separador + " " 
        self.server_socket.send(primer_envio.encode())

        self.master.destroy() 
        self.master = Tk() 
        self.app = Ventana1(self.master, self.server_socket, self.usuario, self.receptor) 
        self.master.mainloop()


