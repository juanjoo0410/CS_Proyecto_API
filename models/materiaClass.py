from pydantic import BaseModel
import datetime

class getItemMateriaByName(BaseModel):
    nombre_materia: str = None