from pydantic import BaseModel
import datetime

class updateEntrega(BaseModel):
    fechaEnvio_entrega  : datetime.date = None
    fechaModificacion_entrega  : datetime.date = None
    archivo_entrega  : str = None
    estado_entrega  : str = None
    actividad_entrega  : int = None
    estudiante_entrega  : int = None
    
class addOneCalificacion(BaseModel):
    actividad_entrega : int =None
    estudiante_entrega : int =None
    calificacion_entrega : float =None

class entregaAdmin(BaseModel):
    curso_actividad : int =None
    estudiante_entrega : int =None
    estado_entrega : str =None