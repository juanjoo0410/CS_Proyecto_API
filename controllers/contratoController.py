from fastapi import  FastAPI,Request
from fastapi import APIRouter
import aiomysql
from configuration.configuration import configuracion
from pydantic import BaseModel
from fastapi.param_functions import Body
from models.contratoClass import getContratosDocenteId,addOneContrato

contrato_router = APIRouter()

async def getConexion():
    conn = await aiomysql.connect(
        host=configuracion['development'].MYSQL_HOST, 
        user=configuracion['development'].MYSQL_USER, 
        password=configuracion['development'].MYSQL_PASSWORD, 
        db=configuracion['development'].MYSQL_DB, 
        charset='utf8', 
        cursorclass=aiomysql.DictCursor)
    return conn

@contrato_router.get("/getContratos")
async def getContratos():
    conn = await getConexion()
    try:
        contratos=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT id_contrato,docente_contrato,fecha_contrato,
                ciclo_contrato,nombramiento_contrato,especialidad_contrato,
                tipo_contrato,jornada_contrato,sueldo_contrato 
                FROM Contrato""")
            resultado = await cur.fetchall()
            for result in resultado:
                contrato = {
                    'id_contrato': result['id_contrato'],
                    'docente_contrato': result['docente_contrato'],
                    'fecha_contrato': result['fecha_contrato'],
                    'ciclo_contrato': result['ciclo_contrato'],
                    'nombramiento_contrato': result['nombramiento_contrato'],
                    'especialidad_contrato': result['especialidad_contrato'],
                    'tipo_contrato': result['tipo_contrato'],
                    'jornada_contrato': result['jornada_contrato'],
                    'sueldo_contrato': result['sueldo_contrato']}
                contratos.append(contrato)
        return {'data': contratos, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@contrato_router.post("/getContratosByIdDocente")
async def getContratosByIdDocente(request: Request, contrato: getContratosDocenteId = Body(...)):
    conn = await getConexion()
    try:
        contratos=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT id_contrato,docente_contrato,fecha_contrato,
                ciclo_contrato,nombramiento_contrato,especialidad_contrato,
                tipo_contrato,jornada_contrato,sueldo_contrato 
                FROM Contrato 
                WHERE docente_contrato=%s""", (contrato.docente_contrato))
            resultado = await cur.fetchall()
            for result in resultado:
                contrato = {
                    'id_contrato': result['id_contrato'],
                    'docente_contrato': result['docente_contrato'],
                    'fecha_contrato': result['fecha_contrato'],
                    'ciclo_contrato': result['ciclo_contrato'],
                    'nombramiento_contrato': result['nombramiento_contrato'],
                    'especialidad_contrato': result['especialidad_contrato'],
                    'tipo_contrato': result['tipo_contrato'],
                    'jornada_contrato': result['jornada_contrato'],
                    'sueldo_contrato': result['sueldo_contrato']}
                contratos.append(contrato)
        return {'data': contratos, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@contrato_router.post("/addContrato")
async def addContrato(request: Request, contrato: addOneContrato = Body(...)):
    conn = await getConexion()
    try:
        docente_contrato=contrato.docente_contrato
        fecha_contrato=contrato.fecha_contrato
        nombramiento_contrato=contrato.nombramiento_contrato
        especialidad_contrato=contrato.especialidad_contrato
        tipo_contrato=contrato.tipo_contrato
        jornada_contrato=contrato.jornada_contrato
        sueldo_contrato=contrato.sueldo_contrato
        insertado=False
        actualizado=False
        async with conn.cursor() as cur:
            await cur.execute("""INSERT INTO Contrato (docente_contrato, fecha_contrato, 
                                nombramiento_contrato, especialidad_contrato, tipo_contrato, jornada_contrato, 
                                sueldo_contrato) VALUES 
                                ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');"""
                              .format(docente_contrato,fecha_contrato,nombramiento_contrato,
                                      especialidad_contrato,tipo_contrato,jornada_contrato
                                      ,sueldo_contrato))
            result= await conn.commit()
            if cur.rowcount > 0:
                insertado=True
                return {'data': {'insertado':True}, 'accion': True}
            update=await cur.execute(
                "UPDATE Docente SET estado_docente = 'Activo' WHERE id_docente = '{0}';".
                format(docente_contrato))
            result2= await conn.commit()
            if cur.rowcount>0:
                actualizado=True
            return {'data': {'insertado':insertado,'actualizado':actualizado}, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()