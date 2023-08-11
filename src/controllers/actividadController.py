from fastapi import  FastAPI,Request
from fastapi import APIRouter
import aiomysql
from configuration.configuration import configuracion
from pydantic import BaseModel
from fastapi.param_functions import Body
from models.actividadClass import getActividadesByCurso, addActividad, updateActividad,deleteActividad

actividad_router = APIRouter()

async def getConexion():
    conn = await aiomysql.connect(
        host=configuracion['development'].MYSQL_HOST, 
        user=configuracion['development'].MYSQL_USER, 
        password=configuracion['development'].MYSQL_PASSWORD, 
        db=configuracion['development'].MYSQL_DB, charset='utf8', 
        cursorclass=aiomysql.DictCursor)
    return conn

@actividad_router.post("/getActividadByCurso")
async def getActividadByCurso(request: Request, miCurso: getActividadesByCurso = Body(...)):
    conn = await getConexion()
    try:
        curso_actividad = miCurso.curso_actividad
        actividades=[]
        async with conn.cursor() as cur:
            await cur.execute("""SELECT id_actividad, fechaPublicacion_actividad, 
                    fechaVencimiento_actividad, nombre_actividad, 
                    descripcion_actividad, archivosPermitidos_actividad, 
                    tipo_actividad, count(archivo_entrega) AS envios
                    from Actividad, Entrega
                    where curso_actividad = '{0}'
                    AND actividad_entrega = id_actividad
                    GROUP BY id_actividad;
                    """.format(curso_actividad))
            resultado = await cur.fetchall()
            for result in resultado:
                actividad = {
                    'id_actividad': result['id_actividad'],
                    'fechaPublicacion_actividad': result['fechaPublicacion_actividad'],
                    'fechaVencimiento_actividad': result['fechaVencimiento_actividad'],
                    'nombre_actividad': result['nombre_actividad'],
                    'descripcion_actividad': result['descripcion_actividad'],
                    'archivosPermitidos_actividad': result['archivosPermitidos_actividad'],
                    'tipo_actividad': result['tipo_actividad'],
                    'envios': result['envios']}
                actividades.append(actividad)
        return {'data': actividades, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@actividad_router.post("/entregaActividad")
async def entregaActividad(request: Request, miCurso: getActividadesByCurso = Body(...)):
    conn = await getConexion()
    try:
        curso_actividad = miCurso.curso_actividad
        entregas=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT actividad_entrega, estudiante_entrega, 
                fechaEnvio_entrega, fechaModificacion_entrega, 
                archivo_entrega, calificacion_entrega, estado_entrega 
                from Actividad, Entrega 
                where curso_actividad = '{0}' AND actividad_entrega = id_actividad;""".format(curso_actividad))
            resultado = await cur.fetchall()
            for result in resultado:
                entrega = {
                    'actividad_entrega': result['actividad_entrega'],
                    'estudiante_entrega': result['estudiante_entrega'],
                    'fechaEnvio_entrega': result['fechaEnvio_entrega'],
                    'fechaModificacion_entrega': result['fechaModificacion_entrega'],
                    'archivo_entrega': result['archivo_entrega'],
                    'calificacion_entrega': result['calificacion_entrega'],
                    'estado_entrega': result['estado_entrega']}
                entregas.append(entrega)
        return {'data': entregas, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@actividad_router.post("/addActividad")
async def addActividad(request: Request, miActividad: addActividad = Body(...)):
    conn = await getConexion()
    try:
        curso_actividad = miActividad.curso_actividad
        fechaVencimiento_actividad = miActividad.fechaVencimiento_actividad
        fechaPublicacion_actividad = miActividad.fechaPublicacion_actividad
        nombre_actividad = miActividad.nombre_actividad
        descripcion_actividad = miActividad.descripcion_actividad
        archivosPermitidos_actividad = miActividad.archivosPermitidos_actividad
        tipo_actividad = miActividad.tipo_actividad
        async with conn.cursor() as cur:
            await cur.execute(
                """INSERT INTO Actividad (curso_actividad, fechaPublicacion_actividad, 
                fechaVencimiento_actividad, nombre_actividad, descripcion_actividad, 
                archivosPermitidos_actividad, tipo_actividad) 
                VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}');""".
                format(curso_actividad, 
                       fechaPublicacion_actividad, 
                       fechaVencimiento_actividad, 
                       nombre_actividad, 
                       descripcion_actividad, 
                       archivosPermitidos_actividad, 
                       tipo_actividad))
            result= await conn.commit()
            if cur.rowcount > 0:
                return {'data': {'insertado':True}, 'accion': True}
            else:
                return {'data': {'insertado':False}, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@actividad_router.put("/updateActividad")
async def updateActividad(request: Request, miActividad: updateActividad = Body(...)):
    conn = await getConexion()
    try:
        id_actividad = miActividad.id_actividad
        fechaVencimiento_actividad = miActividad.fechaVencimiento_actividad
        fechaPublicacion_actividad = miActividad.fechaPublicacion_actividad
        nombre_actividad = miActividad.nombre_actividad
        descripcion_actividad = miActividad.descripcion_actividad
        archivosPermitidos_actividad = miActividad.archivosPermitidos_actividad
        tipo_actividad = miActividad.tipo_actividad
        async with conn.cursor() as cur:
            await cur.execute(
                """UPDATE Actividad SET fechaPublicacion_actividad = '{0}', 
                fechaVencimiento_actividad = '{1}', nombre_actividad = '{2}', 
                descripcion_actividad = '{3}', archivosPermitidos_actividad = '{4}', 
                tipo_actividad = '{5}' WHERE id_actividad = '{6}';""".
                format(fechaPublicacion_actividad, 
                       fechaVencimiento_actividad, 
                       nombre_actividad, 
                       descripcion_actividad, 
                       archivosPermitidos_actividad, 
                       tipo_actividad, 
                       id_actividad))
            result= await conn.commit()
            if cur.rowcount>0:
                return {'data': {'actualizado':True}, 'accion': True}
            else:
                return {'data': {'actualizado':False}, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@actividad_router.delete("/deleteActividad")
async def deleteActividad(request: Request, miActividad: deleteActividad = Body(...)):
    conn = await getConexion()
    try:
        id_actividad = miActividad.id_actividad
        async with conn.cursor() as cur:
            resultEntrega = await cur.execute("delete from Entrega WHERE actividad_entrega = '{0}';".format(id_actividad))
            await cur.execute("delete from Actividad WHERE id_actividad = '{0}';".format(id_actividad))
            resultActividad = await conn.commit()
        return {'data': {'resultEntrega':resultEntrega,'resultActividad':resultActividad}, 'accion': True}    
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()