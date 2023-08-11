from pydantic import BaseModel

class medioClass(BaseModel):
    id_medio: int = None
    nombre_medio: str = None