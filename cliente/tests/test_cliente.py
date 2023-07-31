from src.cliente.biblioteca_cliente import *

def test_port():
    assert SERVER_PORT == 3333

def test_ip():
    assert SERVER_IP == "127.0.0.1"

def test_rellenar():
    a = "prueba"
    b = rellenar_bloque(a)

    assert len(b) == 16

def test_vaciar():
    a = rellenar_bloque("prueba")
    b = vaciar_bloque(a) 

    assert len(a) != len(b)

def test_cifrar_descifrar():
    mensaje = "esto es una prueba"

    mensaje_cifrado, tag, nonce = encriptar(mensaje, "prueba")
    mensaje_descifrado = desencriptar(mensaje_cifrado, "prueba", tag, nonce)

    assert mensaje == mensaje_descifrado.decode('utf-8')
