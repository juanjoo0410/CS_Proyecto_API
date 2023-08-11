from pydantic import BaseModel
import datetime

class getAsistenciaEstudianteId(BaseModel):
    estudiante_asistencia: int = None

class getAsistenciaEstudianteByFechaAndCurso(BaseModel):
    fecha_asistencia: datetime.date = None
    curso_asistencia: int = None

class getAsistenciaEstudianteByCursoAndEstudiante(BaseModel):
    curso_asistencia: int = None
    estudiante_asistencia: int = None

class addAsistencia(BaseModel):
      curso_asistencia: int = None
      estudiante_asistencia: int = None
      fecha_asistencia: datetime.date = None
      estado_asistencia: str = None