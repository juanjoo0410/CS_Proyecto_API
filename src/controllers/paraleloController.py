from fastapi import  FastAPI,Request
from fastapi import APIRouter
import aiomysql
from configuration.configuration import configuracion
from pydantic import BaseModel
from fastapi.param_functions import Body
from models.estudianteClass import estudianteClass

paralelo_router = APIRouter()

async def getConexion():
    conn = await aiomysql.connect(
        host=configuracion['development'].MYSQL_HOST, 
        user=configuracion['development'].MYSQL_USER, 
        password=configuracion['development'].MYSQL_PASSWORD, 
        db=configuracion['development'].MYSQL_DB, 
        charset='utf8', 
        cursorclass=aiomysql.DictCursor)
    return conn

@paralelo_router.get("/getParalelos")
async def getParalelos():
    conn = await getConexion()
    try:
        usuarios=[]
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Paralelo")
            resultado = await cur.fetchall()
            for result in resultado:
                usuario = {
                    'id_paralelo': result['id_paralelo'],
                    'nombre_paralelo': result['nombre_paralelo']}
                usuarios.append(usuario)
        return {'data': usuarios, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()