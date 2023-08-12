from pydantic import BaseModel

class moduloClass(BaseModel):
    id_modulo: int = None
    nombre_modulo: str = None
    precio_modulo: float = None