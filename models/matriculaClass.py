from pydantic import BaseModel
import datetime

class getItemMatriculaByEstudianteId(BaseModel):
    estudiante_matricula: int = None

class addOneMatricula(BaseModel):
    estudiante_matricula: int = None
    fecha_matricula : datetime.date = None