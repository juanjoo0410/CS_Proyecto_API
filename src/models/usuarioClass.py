from pydantic import BaseModel
from cryptography.fernet import Fernet

class usuarioClass(BaseModel):
    id_usuario: int = None
    nombre_usuario: str = None
    contrasena_usuario: str = None
    rol_usuario: int = None

class usuarioCreate(BaseModel):
    nombre_usuario: str

class usuarioVerify(BaseModel):
    nombre_usuario: str
    contrasena_usuario: str

class addUser(BaseModel):
    nombre_usuario: str
    contrasena_usuario: str
    rol_usuario: int = None

    # Encripta un mensaje utilizando una clave
def encriptar(password):
    f = Fernet.generate_key()
    return f.encrypt(password.encode())

# Descifra un mensaje utilizando una clave
def descifrar(password):
    f = Fernet.generate_key()
    return f.decrypt(password).decode()