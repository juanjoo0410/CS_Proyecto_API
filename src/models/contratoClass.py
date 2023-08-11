from pydantic import BaseModel
import datetime

class getContratosDocenteId(BaseModel):
    docente_contrato: int = None

class addOneContrato(BaseModel):
    docente_contrato : int = None
    fecha_contrato : datetime.date = None
    nombramiento_contrato : str = None
    especialidad_contrato : str = None
    tipo_contrato : str = None
    jornada_contrato : str = None
    sueldo_contrato : float = None