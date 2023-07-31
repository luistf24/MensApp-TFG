from src.cliente.biblioteca_cliente import *

def test_port():
    assert SERVER_PORT == 3333

def test_ip():
    assert SERVER_IP == "127.0.0.1"
