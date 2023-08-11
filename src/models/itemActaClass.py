from pydantic import BaseModel
import datetime

class getItemActaByEstudianteId(BaseModel):
    estudiante_itemActa: int = None