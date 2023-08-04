#!/usr/bin/env python

import socket
from tkinter import *
from biblioteca_cliente import *
from interfaz import *

def main(): 
    server_socket = socket.socket()
    server_socket.connect((SERVER_IP, SERVER_PORT))

    print("[+] Conectado al servidor.")

    root = Tk()
    app = Ventana2(root, server_socket)
    root.mainloop()
    server_socket.close()

if __name__ == '__main__':
    main()

