from pydantic import BaseModel
import datetime

class actaClass(BaseModel):
    id_acta: int = None
    curso_acta: int = None

class getActaEstudiante(BaseModel):
    estudiante_itemacta: int = None

class getActaCurso(BaseModel):
    curso_acta: int = None

class addActaCurso(BaseModel):
    curso_acta: int = None  