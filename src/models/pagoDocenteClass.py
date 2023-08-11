from pydantic import BaseModel
import datetime

class getPagoDocenteByDocenteId(BaseModel):
    docente_pagoDocente: int = None

class getPagoDocenteId(BaseModel):
    docente_pagoDocente: int = None 