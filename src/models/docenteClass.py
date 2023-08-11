from pydantic import BaseModel
import datetime

class docenteClass(BaseModel):
    id_docente: int = None
    usuario_docente: int = None
    nombres_docente: str = None
    apellidos_docente: str = None
    cedula_docente: str = None
    fechaNacimiento_docente: datetime.date = None
    edad_docente: int = None
    direccion_docente: str = None
    telefono_docente: str = None
    email_docente: str = None
    titulo_docente: str = None
    nivelEducacion_docente: str = None
    promedio_docente: float = None

class addUserAndDocente(BaseModel):
    nombre_usuario: str
    contrasena_usuario: str
    rol_usuario: int = None
    nombres_docente: str = None
    apellidos_docente: str = None
    cedula_docente: str = None
    fechaNacimiento_docente: datetime.date = None
    edad_docente: int = None
    direccion_docente: str = None
    telefono_docente: str = None
    email_docente: str = None
    titulo_docente: str = None
    nivelEducacion_docente: str = None
    promedio_docente: float = None

class addDocenteByUserId(BaseModel):
    usuario_docente: int = None
    nombres_docente: str = None
    apellidos_docente: str = None
    cedula_docente: str = None
    fechaNacimiento_docente: datetime.date = None
    edad_docente: int = None
    direccion_docente: str = None
    telefono_docente: str = None
    email_docente: str = None
    titulo_docente: str = None
    nivelEducacion_docente: str = None
    promedio_docente: float = None

class addPagoDocente(BaseModel):
    id_pagoDocente: int = None
    docente_pagoDocente: int = None
    fecha_pagoDocente: datetime.date = None
    faltas_pagoDocente: int = None
    descuento_pagoDocente: float = None
    total_pagoDocente: float = None

class getTop5MayorPuntaje(BaseModel):
    ciclo_contrato : str = None

class updateOnePromedioDocente(BaseModel):
    promedio_docente: int = None
    id_docente: int = None