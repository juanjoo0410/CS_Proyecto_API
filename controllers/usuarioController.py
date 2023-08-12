from fastapi import  FastAPI,Request
from fastapi import APIRouter
import aiomysql

from configuration.configuration import configuracion

from pydantic import BaseModel
from fastapi.param_functions import Body

from models.usuarioClass import usuarioClass, usuarioCreate, usuarioVerify, addUser

user_router = APIRouter()

async def getConexion():
    conn = await aiomysql.connect(
        host=configuracion['development'].MYSQL_HOST, 
        user=configuracion['development'].MYSQL_USER, 
        password=configuracion['development'].MYSQL_PASSWORD, 
        db=configuracion['development'].MYSQL_DB, 
        charset='utf8', 
        cursorclass=aiomysql.DictCursor)
    return conn

@user_router.get("/getUsers")
async def getUsers():
    conn = await getConexion()
    try:
        usuarios=[]
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Usuario")
            result = await cur.fetchall()
            for data in result:
                usuario = {
                    'id_usuario': data['id_usuario'], 
                    'nombre_usuario': data['nombre_usuario'], 
                    'contrasena_usuario': data['contrasena_usuario'], 
                    'rol_usuario': data['rol_usuario']}
                usuarios.append(usuario)
        return {'data': usuarios, 'accion':True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@user_router.get("/getUsersByUserName/{username}")
async def getUsersByUserName(username:str):
    conn = await getConexion()
    try:
        usuarios=[]
        async with conn.cursor() as cur:
            await cur.execute("Select * from Usuario where nombre_usuario='{0}'".format(username))
            result = await cur.fetchall()
            for data in result:
                usuario = {
                    'id_usuario': data['id_usuario'], 
                    'nombre_usuario': data['nombre_usuario'], 
                    'contrasena_usuario': data['contrasena_usuario'], 
                    'rol_usuario': data['rol_usuario']}
                usuarios.append(usuario)
        return {'data': usuarios, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@user_router.get("/getUsersWithRol")
async def getUsersWithRol():
    conn = await getConexion()
    try:
        usuarios=[]
        async with conn.cursor() as cur:
            await cur.execute("Select * from Usuario INNER JOIN Rol ON Usuario.rol_usuario = Rol.id_rol")
            result = await cur.fetchall()
            for data in result:
                usuario = {
                    'id_usuario': data['id_usuario'], 
                    'nombre_usuario': data['nombre_usuario'], 
                    'contrasena_usuario': data['contrasena_usuario'], 
                    'rol_usuario': data['rol_usuario'],
                    'nombre_rol': data['nombre_rol']}
                usuarios.append(usuario)
        return {'data': usuarios, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@user_router.get("/usuarios/getRol")
async def getRol():
    conn = await getConexion()
    try:
        roles=[]
        async with conn.cursor() as cur:
            await cur.execute("Select * from Rol")
            result = await cur.fetchall()
            for data in result:
                usuario = {
                    'id_rol': data['id_rol'],
                    'nombre_rol': data['nombre_rol']}
                roles.append(usuario)
        return {'data': roles, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@user_router.get("/getUsersById/{id}")
async def getUsersById(id:int):
    conn = await getConexion()
    try:
        usuarios=[]
        async with conn.cursor() as cur:
            await cur.execute(
                "Select * from Usuario INNER JOIN Rol ON Usuario.rol_usuario = Rol.id_rol " + 
                "where id_usuario={0}".format(id))
            result = await cur.fetchall()
            for datos in result:
                usuario = {
                    'id_usuario': datos['id_usuario'], 
                    'nombre_usuario': datos['nombre_usuario'], 
                    'contrasena_usuario': datos['contrasena_usuario'], 
                    'rol_usuario': datos['rol_usuario'],
                    'nombre_rol': datos['nombre_rol']}
                usuarios.append(usuario)
        return {'data': usuarios, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@user_router.get("/getUsersCompleteData/{id}")
async def getUsersCompleteData(id:int):
    conn = await getConexion()
    try:
        usuarios=[]
        async with conn.cursor() as cur:
            await cur.execute(
                "Select * from Usuario INNER JOIN Rol ON Usuario.rol_usuario = Rol.id_rol " +  
                "where id_usuario={0}".format(id))
            result = await cur.fetchone()
            nombre_rol = result['nombre_rol']
            print(nombre_rol)
            if nombre_rol != None:
                if nombre_rol == "Docente":
                    await cur.execute(
                        "Select * from Usuario INNER JOIN Docente ON Usuario.id_usuario = Docente.usuario_docente " +
                        "where Usuario.id_usuario={0}".format(id))
                    result = await cur.fetchone()
                    usuario = {
                        'id_usuario': result['id_usuario'], 
                        'nombre_usuario': result['nombre_usuario'], 
                        'contrasena_usuario': result['nombre_usuario'], 
                        'rol_usuario': result['rol_usuario'],
                        'id_docente': result['id_docente'],
                        'nombres_docente': result['nombres_docente'],
                        'apellidos_docente': result['apellidos_docente'],
                        'cedula_docente': result['cedula_docente'],
                        'fechaNacimiento_docente': result['fechaNacimiento_docente'],
                        'edad_docente': result['edad_docente'],
                        'direccion_docente': result['direccion_docente'],
                        'telefono_docente': result['telefono_docente'],
                        'email_docente': result['email_docente'],
                        'titulo_docente': result['titulo_docente'],
                        'nivelEducacion_docente': result['nivelEducacion_docente'],
                        'estado_docente': result['estado_docente']}
                    usuarios.append(usuario)
                elif nombre_rol == "Estudiante":
                    await cur.execute(
                        "Select * from Usuario INNER JOIN Estudiante ON Usuario.id_usuario = Estudiante.usuario_estudiante " + 
                        "where Usuario.id_usuario={0}".format(id))
                    result = await cur.fetchone()
                    usuario = {
                        'id_usuario': result['id_usuario'], 
                        'nombre_usuario': result['nombre_usuario'], 
                        'contrasena_usuario': result['contrasena_usuario'], 
                        'rol_usuario': result['rol_usuario'],
                        'id_estudiante': result['id_estudiante'],
                        'nombres_estudiante': result['nombres_estudiante'],
                        'apellidos_estudiante': result['apellidos_estudiante'],
                        'cedula_estudiante': result['cedula_estudiante'],
                        'fechaNacimiento_estudiante': result['fechaNacimiento_estudiante'],
                        'edad_estudiante': result['edad_estudiante'],
                        'direccion_estudiante': result['direccion_estudiante'],
                        'telefono_estudiante': result['telefono_estudiante'],
                        'email_estudiante': result['email_estudiante'],
                        'nivelEducacion_estudiante': result['nivelEducacion_estudiante'],
                        'promedioAnterior_estudiante': result['promedioAnterior_estudiante'],
                        'medio_estudiante': result['medio_estudiante'],
                        'estado_estudiante': result['estado_estudiante']}
                    usuarios.append(usuario)
        return {'data': usuarios, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@user_router.post("/verifyUserByUser")
async def getUsersById(request: Request, user: usuarioCreate = Body(...)):
    conn = await getConexion()
    try:
        username = user.nombre_usuario
        resultado={}
        async with conn.cursor() as cur:
            await cur.execute(
                "Select * from Usuario where " + 
                "nombre_usuario='{0}' ".format(username))
            result = await cur.fetchone()
            if result != None:
                resultado={'existe':True}
            else:
                resultado={'existe':False}
        return {'data': resultado, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@user_router.post("/verifyUserByUserAndPassword")
async def getUsersById(request: Request, user: usuarioVerify = Body(...)):
    conn = await getConexion()
    try:
        username = user.nombre_usuario
        password = user.contrasena_usuario
        resultado={}
        async with conn.cursor() as cur:
            await cur.execute(
                "Select * from Usuario " + 
                "where nombre_usuario='{0}' and contrasena_usuario='{1}'".format(username,password))
            result = await cur.fetchone()
            if result != None:
                resultado={'existe':True}
            else:
                resultado={'existe':False}
        return {'data': resultado, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@user_router.post("/addUser")
async def addUser(request: Request, user: addUser = Body(...)):
    conn = await getConexion()
    try:
        username = user.nombre_usuario
        password = user.contrasena_usuario
        rol = user.rol_usuario
        global insertado
        insertado=False
        async with conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO Usuario(nombre_usuario, contrasena_usuario, rol_usuario) " + 
                "VALUES ('{0}','{1}','{2}')".format(username,password,rol))
            await conn.commit()
            if cur.rowcount > 0:
                insertado=True
        return {'data': {'insertado':insertado}, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()