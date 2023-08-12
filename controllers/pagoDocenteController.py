from fastapi import  FastAPI,Request
from fastapi import APIRouter
import aiomysql
from configuration.configuration import configuracion
from pydantic import BaseModel
from fastapi.param_functions import Body
from models.pagoDocenteClass import getPagoDocenteByDocenteId,getPagoDocenteId
pagoDocente_router = APIRouter()

async def getConexion():
    conn = await aiomysql.connect(
        host=configuracion['development'].MYSQL_HOST, 
        user=configuracion['development'].MYSQL_USER, 
        password=configuracion['development'].MYSQL_PASSWORD, 
        db=configuracion['development'].MYSQL_DB, 
        charset='utf8', 
        cursorclass=aiomysql.DictCursor)
    return conn

@pagoDocente_router.get("/getPagoDocentes")
async def getPagoDocentes():
    conn = await getConexion()
    try:
        pagoDocentes=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT id_pagoDocente,docente_pagoDocente,fecha_pagoDocente,
                faltas_pagoDocente,descuento_pagoDocente,total_pagoDocente 
                FROM PagoDocente""")
            resultado = await cur.fetchall()
            for result in resultado:
                pagoDocente = {
                    'id_pagoDocente': result['id_pagoDocente'],
                    'docente_pagoDocente': result['docente_pagoDocente'],
                    'fecha_pagoDocente': result['fecha_pagoDocente'],
                    'faltas_pagoDocente': result['faltas_pagoDocente'],
                    'descuento_pagoDocente': result['descuento_pagoDocente'],
                    'total_pagoDocente': result['total_pagoDocente']}
                pagoDocentes.append(pagoDocente)
        return {'data': pagoDocentes, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@pagoDocente_router.post("/getByPagoDocente")
async def getByDocenteId(request: Request, pagoDocente: getPagoDocenteByDocenteId):
    conn = await getConexion()
    try:
        pagoDocentes=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT id_pagoDocente,docente_pagoDocente,fecha_pagoDocente,
                faltas_pagoDocente,descuento_pagoDocente,total_pagoDocente 
                FROM PagoDocente WHERE docente_pagoDocente=%s""",
                (pagoDocente.docente_pagoDocente))
            resultado = await cur.fetchall()
            for result in resultado:
                pagoDocente = {
                    'id_pagoDocente': result['id_pagoDocente'],
                    'docente_pagoDocente': result['docente_pagoDocente'],
                    'fecha_pagoDocente': result['fecha_pagoDocente'],
                    'faltas_pagoDocente': result['faltas_pagoDocente'],
                    'descuento_pagoDocente': result['descuento_pagoDocente'],
                    'total_pagoDocente': result['total_pagoDocente']}
                pagoDocentes.append(pagoDocente)
        return {'data': pagoDocentes, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@pagoDocente_router.get("/getAdminPagoDocentes")
async def getAdminPagoDocentes():
    conn = await getConexion()
    try:
        pagoDocentes=[]
        async with conn.cursor() as cur:
            await cur.execute("""SELECT fecha_pagoDocente, sueldo_contrato, faltas_pagoDocente, 
                                descuento_pagoDocente, total_pagoDocente, cedula_docente, 
                                concat(nombres_docente, ' ', apellidos_docente) AS nombresCompletos_docente
                                FROM Docente, PagoDocente, Contrato
                                WHERE docente_pagoDocente = id_docente = docente_contrato;""")
            resultado = await cur.fetchall()
            for result in resultado:
                pagoDocente = {'fecha_pagoDocente': result['fecha_pagoDocente'],
                               'sueldo_contrato': result['sueldo_contrato'],
                               'faltas_pagoDocente': result['faltas_pagoDocente'],
                               'descuento_pagoDocente': result['descuento_pagoDocente'],
                               'total_pagoDocente': result['total_pagoDocente'],
                               'cedula_docente': result['cedula_docente'],
                               'nombresCompletos_docente': result['nombresCompletos_docente']}
                pagoDocentes.append(pagoDocente)
        return {'data': pagoDocentes, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@pagoDocente_router.post("/getPagoDocenteByDocenteId")
async def getPagoDocenteByDocenteId(request: Request, pagoDocente: getPagoDocenteId):
    conn = await getConexion()
    try:
        docente_pagoDocente=pagoDocente.docente_pagoDocente
        pagoDocentes=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT fecha_pagoDocente, sueldo_contrato, faltas_pagoDocente, 
                descuento_pagoDocente, total_pagoDocente
                FROM PagoDocente, Contrato
                WHERE docente_pagoDocente = docente_contrato 
                AND docente_contrato = '{0}';""".format(docente_pagoDocente))
            resultado = await cur.fetchall()
            for result in resultado:
                pagoDocente = {'fecha_pagoDocente': result['fecha_pagoDocente']
                               ,'sueldo_contrato': result['sueldo_contrato']
                               ,'faltas_pagoDocente': result['faltas_pagoDocente']
                               ,'descuento_pagoDocente': result['descuento_pagoDocente']
                               ,'total_pagoDocente': result['total_pagoDocente']}
                pagoDocentes.append(pagoDocente)
        return {'data': pagoDocentes, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()