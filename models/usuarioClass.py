from pydantic import BaseModel

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