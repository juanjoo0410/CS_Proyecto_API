from pydantic import BaseModel
import datetime

class getOrdenPagoMatriculaByIdPago(BaseModel):
    matricula_pagoMatricula: int = None

class addOneOrdenPagoMatriculas(BaseModel):
    matricula_pagoMatricula : int =None
    item_pagoMatricula : str =None
    cantidad_pagoMatricula : int =None
    subtotal_pagoMatricula : float =None
    descuento_pagoMatricula : float =None
    total_pagoMatricula : float =None