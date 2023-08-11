from pydantic import BaseModel
import datetime

class horarioClass(BaseModel):
    id_horario: int = None
    curso_horario: int = None
    dia_horario: str = None
    horaInicio_horario: str = None
    horaFin_horario: str = None

class getHorarioPersonalizado(BaseModel):
    pass

class getHorarioDocente(BaseModel):
    docente_curso: int = None

class getHorarioEstudiante(BaseModel):
    estudiante_matricula: int = None