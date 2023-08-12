from fastapi import  FastAPI,Request
from fastapi import APIRouter
import aiomysql
from configuration.configuration import configuracion
from pydantic import BaseModel
from fastapi.param_functions import Body
from models.asistenciaClass import addAsistencia,getAsistenciaEstudianteId,getAsistenciaEstudianteByFechaAndCurso,getAsistenciaEstudianteByCursoAndEstudiante

asistencia_router = APIRouter()

async def getConexion():
    conn = await aiomysql.connect(
        host=configuracion['development'].MYSQL_HOST, 
        user=configuracion['development'].MYSQL_USER, 
        password=configuracion['development'].MYSQL_PASSWORD, 
        db=configuracion['development'].MYSQL_DB, 
        charset='utf8', 
        cursorclass=aiomysql.DictCursor)
    return conn

@asistencia_router.get("/getAsistenciasEstudiante")
async def getAsistenciasEstudiante():
    conn = await getConexion()
    try:
        asistencias=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT id_asistencia,curso_asistencia,estudiante_asistencia,fecha_asistencia,estado_asistencia 
                FROM Asistencia""")
            resultado = await cur.fetchall()
            for result in resultado:
                asistencia = {
                    'id_asistencia': result['id_asistencia'],
                    'curso_asistencia': result['curso_asistencia'],
                    'estudiante_asistencia': result['estudiante_asistencia'],
                    'fecha_asistencia': result['fecha_asistencia'],
                    'estado_asistencia': result['estado_asistencia']}
                asistencias.append(asistencia)
        return {'data': asistencias, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@asistencia_router.post("/getAsistenciasByIdEstudiante")
async def getAsistenciasByIdEstudiante(request: Request, asistencia: getAsistenciaEstudianteId = Body(...)):
    conn = await getConexion()
    try:
        asistencias=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT id_asistencia,curso_asistencia,estudiante_asistencia,
                fecha_asistencia,estado_asistencia 
                FROM Asistencia 
                WHERE estudiante_asistencia=%s""", (asistencia.estudiante_asistencia))
            resultado = await cur.fetchall()
            for result in resultado:
                asistencia = {
                    'id_asistencia': result['id_asistencia'],
                    'curso_asistencia': result['curso_asistencia'],
                    'estudiante_asistencia': result['estudiante_asistencia'],
                    'fecha_asistencia': result['fecha_asistencia'],
                    'estado_asistencia': result['estado_asistencia']}
                asistencias.append(asistencia)
        return {'data': asistencias, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@asistencia_router.post("/getAsistenciasByFechaAndCurso")
async def getAsistenciasByFechaAndCurso(request: Request, asistencia: getAsistenciaEstudianteByFechaAndCurso = Body(...)):
    conn = await getConexion()
    try:
        asistencias=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT id_estudiante, concat(nombres_estudiante, ' ', 
                apellidos_estudiante) as nombrescompletos_estudiante, estado_asistencia 
                FROM Asistencia, Estudiante 
                WHERE fecha_asistencia = %s AND curso_asistencia = %s AND estudiante_asistencia = id_estudiante""", 
                (asistencia.fecha_asistencia,asistencia.curso_asistencia))
            resultado = await cur.fetchall()
            for result in resultado:
                asistencia = {
                    'id_estudiante': result['id_estudiante'],
                    'nombrescompletos_estudiante': result['nombrescompletos_estudiante'],
                    'estado_asistencia': result['estado_asistencia']}
                asistencias.append(asistencia)
        return {'data': asistencias, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@asistencia_router.post("/getAsistenciasByCursoAndEstudiante")
async def getAsistenciasByCursoAndEstudiante(request: Request, asistencia: getAsistenciaEstudianteByCursoAndEstudiante = Body(...)):
    conn = await getConexion()
    try:
        asistencias=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT  fecha_asistencia, estado_asistencia 
                FROM Asistencia, Estudiante 
                WHERE curso_asistencia = %s AND estudiante_asistencia = id_estudiante AND estudiante_asistencia = %s""", 
                (asistencia.curso_asistencia,asistencia.estudiante_asistencia))
            resultado = await cur.fetchall()
            for result in resultado:
                asistencia = {
                    'fecha_asistencia': result['fecha_asistencia'],
                    'estado_asistencia': result['estado_asistencia']}
                asistencias.append(asistencia)
        return {'data': asistencias, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@asistencia_router.post("/addAsistencia")
async def addAsistencia(request: Request, asistencia: addAsistencia = Body(...)):
    conn = await getConexion()
    try:
        curso_asistencia = asistencia.curso_asistencia
        estudiante_asistencia = asistencia.estudiante_asistencia
        fecha_asistencia = asistencia.fecha_asistencia
        estado_asistencia = asistencia.estado_asistencia
        global insertado
        insertado=False
        async with conn.cursor() as cur:
            await cur.execute(
                """INSERT INTO Asistencia (curso_asistencia, estudiante_asistencia, 
                fecha_asistencia, estado_asistencia) 
                VALUES ('{0}','{1}','{2}', '{3}');""".
                format(curso_asistencia,estudiante_asistencia,fecha_asistencia,estado_asistencia))
            await conn.commit()
            if cur.rowcount > 0:
                insertado=True
        return {'data': {'insertado':insertado}, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()