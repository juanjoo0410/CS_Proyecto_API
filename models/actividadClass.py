from pydantic import BaseModel
import datetime

class getActividadesByCurso(BaseModel):
    curso_actividad : int = None

class addActividad(BaseModel):
    curso_actividad : int = None
    fechaVencimiento_actividad  : datetime.date = None
    fechaPublicacion_actividad  : datetime.date = None
    nombre_actividad  : str = None
    descripcion_actividad  : str = None
    archivosPermitidos_actividad  : str = None
    tipo_actividad  : str = None

class updateActividad(BaseModel):
    id_actividad : int = None
    curso_actividad : int = None
    fechaVencimiento_actividad  : datetime.date = None
    fechaPublicacion_actividad  : datetime.date = None
    nombre_actividad  : str = None
    descripcion_actividad  : str = None
    archivosPermitidos_actividad  : str = None
    tipo_actividad  : str = None

class deleteActividad(BaseModel):
    id_actividad : int = None 