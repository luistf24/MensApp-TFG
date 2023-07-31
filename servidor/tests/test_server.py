from src.servidor.biblioteca_servidor import *

def test_port():
    assert SERVER_PORT == 3333

def test_ip():
    assert SERVER_IP == "0.0.0.0"
