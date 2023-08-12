from pydantic import BaseModel
import datetime

class getItemMatriculasByMatriculaId(BaseModel):
    matricula_itemMatricula: int = None

class addOneItemMatricula(BaseModel):
    matricula_itemMatricula: int = None
    curso_itemMatricula : int = None