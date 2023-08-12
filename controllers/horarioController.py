from fastapi import  FastAPI,Request
from fastapi import APIRouter
import aiomysql
from configuration.configuration import configuracion
from pydantic import BaseModel
from fastapi.param_functions import Body
from models.horarioClass import horarioClass,getHorarioPersonalizado,getHorarioDocente,getHorarioEstudiante

horario_router = APIRouter()

async def getConexion():
    conn = await aiomysql.connect(
        host=configuracion['development'].MYSQL_HOST, 
        user=configuracion['development'].MYSQL_USER, 
        password=configuracion['development'].MYSQL_PASSWORD, 
        db=configuracion['development'].MYSQL_DB, charset='utf8', 
        cursorclass=aiomysql.DictCursor)
    return conn

@horario_router.get("/getAllHorarios")
async def getAllHorarios():
    conn = await getConexion()
    try:
        horarios=[]
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Horario")
            resultado = await cur.fetchall()
            for result in resultado:
                horario = {
                    'id_Horario': result['id_Horario'],
                    'curso_horario': result['curso_horario'],
                    'dia_horario': result['dia_horario'],
                    'horaInicio_horario': result['horaInicio_horario'],
                    'horaFin_horario': result['horaFin_horario']}
                horarios.append(horario)
        return {'data': horarios, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@horario_router.post("/getHorarioDocente")
async def getHorarioDocente(request: Request, miHorario: getHorarioDocente = Body(...)):
    conn = await getConexion()
    try:
        docente_curso = miHorario.docente_curso
        horarios=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """Select id_curso, nombre_materia, modulo_materia, nombre_paralelo, 
                dia_horario, concat(horaInicio_horario, ' - ',horaFin_horario) as hora_horario 
                from Horario, Curso, Materia, Paralelo 
                where docente_curso = '{0}' and curso_horario = id_curso and 
                materia_curso = id_materia and paralelo_curso = id_paralelo;""".
                format(docente_curso))
            resultado = await cur.fetchall()
            for result in resultado:
                horario = {
                    'id_curso': result['id_curso'],
                    'nombre_materia': result['nombre_materia'],
                    'modulo_materia': result['modulo_materia'],
                    'nombre_paralelo': result['nombre_paralelo'],
                    'dia_horario': result['dia_horario'],
                    'hora_horario': result['hora_horario']}
                horarios.append(horario)
        return {'data': horarios, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@horario_router.post("/getHorarioEstudiante")
async def getHorarioEstudiante(request: Request, miHorario: getHorarioEstudiante = Body(...)):
    conn = await getConexion()
    try:
        estudiante_matricula = miHorario.estudiante_matricula
        horarios=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """Select id_curso, nombre_materia, modulo_materia, nombre_paralelo, 
                concat(nombres_docente, ' ',apellidos_docente) as docente_curso, dia_horario, 
                concat(horaInicio_horario, ' - ',horaFin_horario) as hora_horario 
                from Horario, Curso, Materia, Paralelo, Docente, Matricula, ItemMatricula 
                where estudiante_matricula = '{0}' and matricula_itemMatricula = id_matricula and 
                curso_horario = curso_itemMatricula and curso_horario = id_curso and 
                materia_curso = id_materia and paralelo_curso = id_paralelo and docente_curso = id_docente;""".
                format(estudiante_matricula))
            resultado = await cur.fetchall()
            for result in resultado:
                horario = {
                    'id_curso': result['id_curso'],
                    'nombre_materia': result['nombre_materia'],
                    'modulo_materia': result['modulo_materia'],
                    'nombre_paralelo': result['nombre_paralelo'],
                    'docente_curso': result['docente_curso'],
                    'dia_horario': result['dia_horario'],
                    'hora_horario': result['hora_horario']}
                horarios.append(horario)
        return {'data': horarios, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()