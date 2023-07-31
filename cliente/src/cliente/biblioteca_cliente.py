from Crypto.Cipher import AES
import hashlib

SERVER_IP    = "127.0.0.1"
SERVER_PORT  = 3333
separador    = "<->"

def rellenar_bloque(mensaje): 
    tam_mens = len(mensaje)%16
    padding_necesario = 16 - tam_mens

    return mensaje + padding_necesario*' '

def vaciar_bloque(mensaje):
    return mensaje.rstrip()

def encriptar(mensaje, passw):
    iv = 0
    clave_privada = hashlib.scrypt(passw.encode(), salt=iv.to_bytes(16, 'big'), n=2**14, r=8, p=1, dklen=32)
    aes = AES.new(clave_privada, AES.MODE_GCM)
    mensaje_cifrado, tag= aes.encrypt_and_digest(bytes(mensaje, 'utf-8'))
    nonce = aes.nonce

    return mensaje_cifrado, tag, nonce

def desencriptar(mensaje_cifrado, passw, tag, nonce):
    iv = 0
    clave_privada = hashlib.scrypt(passw.encode(), salt=iv.to_bytes(16, 'big'), n=2**14, r=8, p=1, dklen=32)
    aes = AES.new(clave_privada, AES.MODE_GCM, nonce=nonce)
    mensaje = aes.decrypt_and_verify(mensaje_cifrado, tag)

    return mensaje
