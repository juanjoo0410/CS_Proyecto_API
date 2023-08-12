from fastapi import  FastAPI,Request
from fastapi import APIRouter
import aiomysql
from configuration.configuration import configuracion
from pydantic import BaseModel
from fastapi.param_functions import Body
from models.entregaClass import updateEntrega,addOneCalificacion,entregaAdmin

entrega_router = APIRouter()

async def getConexion():
    conn = await aiomysql.connect(
        host=configuracion['development'].MYSQL_HOST, 
        user=configuracion['development'].MYSQL_USER, 
        password=configuracion['development'].MYSQL_PASSWORD, 
        db=configuracion['development'].MYSQL_DB, charset='utf8', 
        cursorclass=aiomysql.DictCursor)
    return conn

@entrega_router.put("/updateEntrega")
async def updateEntrega(request: Request, miEntrega: updateEntrega = Body(...)):
    conn = await getConexion()
    try:
        fechaEnvio_entrega = miEntrega.fechaEnvio_entrega
        fechaModificacion_entrega = miEntrega.fechaModificacion_entrega
        archivo_entrega = miEntrega.archivo_entrega
        estado_entrega = miEntrega.estado_entrega
        actividad_entrega = miEntrega.actividad_entrega
        estudiante_entrega = miEntrega.estudiante_entrega
        async with conn.cursor() as cur:
            await cur.execute(
                """UPDATE Entrega SET fechaEnvio_entrega = '{0}', fechaModificacion_entrega = '{1}', 
                archivo_entrega = '{2}', estado_entrega = '{3}' 
                WHERE actividad_entrega = '{4}'  AND estudiante_entrega ='{5}';""".
                format(fechaEnvio_entrega, fechaModificacion_entrega, archivo_entrega, 
                       estado_entrega,actividad_entrega,estudiante_entrega))
            resultado=await conn.commit()
            if resultado == 1:
                return {'data': {'actualizado':True}, 'accion': True}
            else:
                return {'data': {'actualizado':False}, 'accion': True}
    except Exception as e:
         return {'data': '', 'accion': False}
    finally:
        conn.close()

@entrega_router.get("/getEntregas")
async def getEntregas():
    conn = await getConexion()
    try:
        entrega=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT id_entrega,actividad_entrega,estudiante_entrega,
                fechaEnvio_entrega,fechaModificacion_entrega,archivo_entrega,
                calificacion_entrega,estado_entrega 
                FROM Entrega""")
            resultado=await cur.fetchall()
            for row in resultado:
                entrega.append({
                    'id_entrega': row['id_entrega'], 
                    'actividad_entrega': row['actividad_entrega'], 
                    'estudiante_entrega': row['estudiante_entrega'], 
                    'fechaEnvio_entrega': row['fechaEnvio_entrega'], 
                    'fechaModificacion_entrega': row['fechaModificacion_entrega'], 
                    'archivo_entrega': row['archivo_entrega'], 
                    'calificacion_entrega': row['calificacion_entrega'], 
                    'estado_entrega': row['estado_entrega']})
            return {'data': entrega, 'accion': True}
    except Exception as e:
         return {'data': '', 'accion': False}
    finally:
        conn.close()

@entrega_router.put("/addCalificacion")
async def addCalificacion(request: Request, entrega: addOneCalificacion = Body(...)):
    conn = await getConexion()
    try:
        actividad_entrega=entrega.actividad_entrega
        estudiante_entrega=entrega.estudiante_entrega
        calificacion_entrega=entrega.calificacion_entrega
        async with conn.cursor() as cur:
            await cur.execute(
                """UPDATE Entrega 
                SET calificacion_entrega = '{0}' 
                WHERE actividad_entrega = '{1}' 
                AND estudiante_entrega = '{2}';""".
                format(calificacion_entrega, actividad_entrega, estudiante_entrega))
            result= await conn.commit()
            print(result)
            if cur.rowcount>0:
                return {'data': {'actualizado':True}, 'accion': True}
            else:
                return {'data': {'actualizado':False}, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@entrega_router.post("/GetEntregasAdmin")
async def GetEntregasAdmin(request: Request, miEntrega: entregaAdmin = Body(...)):
    conn = await getConexion()
    try:
        curso_actividad = miEntrega.curso_actividad
        estudiante_entrega=miEntrega.estudiante_entrega
        estado_entrega=miEntrega.estado_entrega
        entregas=[]
        async with conn.cursor() as cur:
            await cur.execute("""SELECT nombre_actividad
                from Actividad, Entrega
                where curso_actividad = '{0}'
                AND actividad_entrega = id_actividad
                AND estado_entrega = '{1}'
                AND estudiante_entrega = '{2}';""".
                format(curso_actividad, estado_entrega, estudiante_entrega))
            resultado=await conn.commit()
            resultado = await cur.fetchall()
            for result in resultado:
                entrega = {'nombre_actividad': result['nombre_actividad']}
                entregas.append(entrega)
        return {'data': entregas, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()