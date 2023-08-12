from fastapi import  FastAPI,Request
from fastapi import APIRouter
import aiomysql
from configuration.configuration import configuracion
from pydantic import BaseModel
from fastapi.param_functions import Body
from models.ordenPagoMatriculaClass import getOrdenPagoMatriculaByIdPago,addOneOrdenPagoMatriculas

ordenPago_router = APIRouter()

async def getConexion():
    conn = await aiomysql.connect(
        host=configuracion['development'].MYSQL_HOST, 
        user=configuracion['development'].MYSQL_USER, 
        password=configuracion['development'].MYSQL_PASSWORD, 
        db=configuracion['development'].MYSQL_DB, 
        charset='utf8', 
        cursorclass=aiomysql.DictCursor)
    return conn

@ordenPago_router.get("/getItemOrdenPagoMatriculas")
async def getItemOrdenPagoMatriculas():
    conn = await getConexion()
    try:
        itemOrdenPagoMatriculas=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT id_itemMatricula,matricula_pagoMatricula,item_pagoMatricula,
                cantidad_pagoMatricula,subtotal_pagoMatricula,descuento_pagoMatricula,
                total_pagoMatricula 
                FROM OrdenPagoMatricula""")
            resultado = await cur.fetchall()
            for result in resultado:
                itemOrdenPagoMatricula = {
                    'id_itemMatricula': result['id_itemMatricula'],
                    'matricula_pagoMatricula': result['matricula_pagoMatricula'],
                    'item_pagoMatricula': result['item_pagoMatricula'],
                    'cantidad_pagoMatricula': result['cantidad_pagoMatricula'],
                    'subtotal_pagoMatricula': result['subtotal_pagoMatricula'],
                    'descuento_pagoMatricula': result['descuento_pagoMatricula'],
                    'total_pagoMatricula': result['total_pagoMatricula']}
                itemOrdenPagoMatriculas.append(itemOrdenPagoMatricula)
        return {'data': itemOrdenPagoMatriculas, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@ordenPago_router.post("/getItemOrdenPagoMatriculasByMatriculaId")
async def getItemOrdenPagoMatriculasByMatriculaId(request: Request, itemOrdenPagoMatricula: getOrdenPagoMatriculaByIdPago = Body(...)):
    conn = await getConexion()
    try:
        itemOrdenPagoMatriculas=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT id_itemMatricula,matricula_pagoMatricula,item_pagoMatricula,
                cantidad_pagoMatricula,subtotal_pagoMatricula,descuento_pagoMatricula,
                total_pagoMatricula 
                FROM OrdenPagoMatricula WHERE matricula_pagoMatricula = %s""", 
                (itemOrdenPagoMatricula.matricula_pagoMatricula))
            resultado = await cur.fetchall()
            for result in resultado:
                itemOrdenPagoMatricula = {
                    'id_itemMatricula': result['id_itemMatricula'],
                    'matricula_pagoMatricula': result['matricula_pagoMatricula'],
                    'item_pagoMatricula': result['item_pagoMatricula'],
                    'cantidad_pagoMatricula': result['cantidad_pagoMatricula'],
                    'subtotal_pagoMatricula': result['subtotal_pagoMatricula'],
                    'descuento_pagoMatricula': result['descuento_pagoMatricula'],
                    'total_pagoMatricula': result['total_pagoMatricula']}
                itemOrdenPagoMatriculas.append(itemOrdenPagoMatricula)
        return {'data': itemOrdenPagoMatriculas, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()


@ordenPago_router.post("/addOrdenPagoMatriculas")
async def addOrdenPagoMatriculas(request: Request, pagoMatricula: addOneOrdenPagoMatriculas = Body(...)):
    conn = await getConexion()
    try:
        matricula_pagoMatricula = pagoMatricula.matricula_pagoMatricula
        item_pagoMatricula = pagoMatricula.item_pagoMatricula
        cantidad_pagoMatricula =pagoMatricula.cantidad_pagoMatricula
        subtotal_pagoMatricula=pagoMatricula.subtotal_pagoMatricula
        descuento_pagoMatricula=pagoMatricula.descuento_pagoMatricula
        total_pagoMatricula=pagoMatricula.total_pagoMatricula
        global insertado
        insertado=False
        async with conn.cursor() as cur:
            await cur.execute("""INSERT INTO OrdenPagoMatricula (matricula_pagoMatricula, item_pagoMatricula, 
                                cantidad_pagoMatricula, subtotal_pagoMatricula, descuento_pagoMatricula, 
                                total_pagoMatricula) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');
                                """.format(matricula_pagoMatricula,item_pagoMatricula,cantidad_pagoMatricula,
                                           subtotal_pagoMatricula,descuento_pagoMatricula,total_pagoMatricula))
            await conn.commit()
            if cur.rowcount > 0:
                insertado=True
        return {'data': {'insertado':insertado}, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()