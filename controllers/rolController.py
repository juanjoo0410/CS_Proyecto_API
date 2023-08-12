from fastapi import  FastAPI,Request
from fastapi import APIRouter
import aiomysql
from configuration.configuration import configuracion
from pydantic import BaseModel
from fastapi.param_functions import Body

rol_router = APIRouter()

async def getConexion():
    conn = await aiomysql.connect(
        host=configuracion['development'].MYSQL_HOST, 
        user=configuracion['development'].MYSQL_USER, 
        password=configuracion['development'].MYSQL_PASSWORD, 
        db=configuracion['development'].MYSQL_DB, 
        charset='utf8', 
        cursorclass=aiomysql.DictCursor)
    return conn

@rol_router.get("/getRolId/{nombre_rol}")
async def getRolId(nombre_rol:str):
    conn = await getConexion()
    try:      
        usuarios=[]
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT id_rol FROM Rol where nombre_rol = '{0}'".format(nombre_rol))
            resultado = await cur.fetchone()
            if resultado != None:
                usuario = {'id_rol': resultado['id_rol']}
                usuarios.append(usuario)
        return {'data': usuarios, 'accion': "true"}
    except Exception as e:
        return {'data': '', 'accion': "false"}
    finally:
        conn.close()

@rol_router.get("/getRolName/{id_rol}")
async def getRolName(id_rol:str):
    conn = await getConexion()
    try:      
        usuarios=[]
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT nombre_rol FROM Rol where id_rol = {0}".format(id_rol))
            resultado = await cur.fetchone()
            if resultado != None:
                usuario = {'nombre_rol': resultado['nombre_rol']}
                usuarios.append(usuario)
        return {'data': usuarios, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()