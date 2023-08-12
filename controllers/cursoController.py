from fastapi import  FastAPI,Request
from fastapi import APIRouter
import aiomysql
from configuration.configuration import configuracion
from pydantic import BaseModel
from fastapi.param_functions import Body
from models.cursoClass import cursoClass, getCursoDocente, getCursoEstudiante, getParticipantesCurso

course_router = APIRouter()

async def getConexion():
    conn = await aiomysql.connect(
        host=configuracion['development'].MYSQL_HOST, 
        user=configuracion['development'].MYSQL_USER, 
        password=configuracion['development'].MYSQL_PASSWORD, 
        db=configuracion['development'].MYSQL_DB, charset='utf8', 
        cursorclass=aiomysql.DictCursor)
    return conn

@course_router.get("/getCursos")
async def getCursos():
    conn = await getConexion()
    try:
        cursos=[]
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Curso")
            resultado = await cur.fetchall()
            for result in resultado:
                curso = {
                    'id_curso': result['id_curso'],
                    'paralelo_curso': result['paralelo_curso'],
                    'materia_curso': result['materia_curso'],
                    'docente_curso': result['docente_curso'],
                    'estudiantes_curso': result['estudiantes_curso'],
                    'ciclo_curso': result['ciclo_curso']}
                cursos.append(curso)
        return {'data': cursos, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@course_router.post("/getCursosDocente")
async def getCursosDocente(request: Request, miCurso: getCursoDocente = Body(...)):
    conn = await getConexion()
    try:
        docente_curso = miCurso.docente_curso
        cursos=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT id_curso, nombre_materia, nombre_paralelo 
                FROM Curso, Paralelo, Materia  
                WHERE docente_curso = '{0}' and id_paralelo = paralelo_curso  and id_materia = materia_curso;""".
                format(docente_curso))
            resultado = await cur.fetchall()
            for result in resultado:
                curso = {
                    'id_curso': result['id_curso'],
                    'nombre_materia': result['nombre_materia'],
                    'nombre_paralelo': result['nombre_paralelo']}
                cursos.append(curso)
        return {'data': cursos, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@course_router.post("/getCursosEstudiante")
async def getCursosEstudiante(request: Request, miCurso: getCursoEstudiante = Body(...)):
    conn = await getConexion()
    try:
        estudiante_matricula = miCurso.estudiante_matricula
        cursos=[]
        async with conn.cursor() as cur:
            await cur.execute("""SELECT id_curso, nombre_materia, nombre_paralelo, ciclo_curso
                                FROM Curso 
                                JOIN Paralelo ON id_paralelo = paralelo_curso
                                JOIN Materia ON id_materia = materia_curso
                                JOIN ItemMatricula ON id_curso = curso_itemMatricula
                                JOIN Matricula ON id_matricula = matricula_itemMatricula
                                WHERE estudiante_matricula = '{0}'
                                AND ciclo_curso = (SELECT MAX(ciclo_curso) FROM Curso c2 JOIN ItemMatricula 
                                ON id_curso = curso_itemMatricula JOIN Matricula ON id_matricula = 
                                matricula_itemMatricula WHERE estudiante_matricula = 340)
                                ORDER BY nombre_paralelo ASC;""".format(estudiante_matricula))
            resultado = await cur.fetchall()
            for result in resultado:
                curso = {
                    'id_curso': result['id_curso'],
                    'nombre_materia': result['nombre_materia'],
                    'nombre_paralelo': result['nombre_paralelo'],
                    'ciclo_curso':result['ciclo_curso']}
                cursos.append(curso)
        return {'data': cursos, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@course_router.post("/getParticipantesCurso")
async def getParticipantesCurso(request: Request, miCurso: getParticipantesCurso = Body(...)):
    conn = await getConexion()
    try:
        id_curso = miCurso.id_curso
        participantes=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT id_estudiante,  concat(nombres_estudiante, ' ',
                apellidos_estudiante) AS nombrescompletos_estudiante, email_estudiante, nombre_rol 
                from Matricula, ItemMatricula, Estudiante, Rol, Usuario 
                where  matricula_itemMatricula = id_matricula  AND 
                estudiante_matricula = id_estudiante AND curso_itemMatricula = '{0}' AND 
                id_rol = rol_usuario AND id_usuario = usuario_estudiante 
                UNION SELECT id_docente,  concat(nombres_docente, ' ',
                apellidos_docente) AS nombrescompletos_docente, email_docente, nombre_rol 
                from Curso, Docente, Rol, Usuario 
                where  id_curso = '{0}' AND docente_curso = id_docente AND id_rol = rol_usuario AND 
                id_usuario = usuario_docente;""".
                format(id_curso))
            resultado = await cur.fetchall()
            for result in resultado:
                participante = {
                    'id_participante': result['id_estudiante'],
                    'nombrescompletos_participante': result['nombrescompletos_estudiante'],
                    'email_participante': result['email_estudiante'],
                    'rol_participante': result['nombre_rol']}
                participantes.append(participante)
        return {'data': participantes, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()