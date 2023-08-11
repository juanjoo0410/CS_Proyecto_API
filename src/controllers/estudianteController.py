from fastapi import  FastAPI,Request
from fastapi import APIRouter
import aiomysql
from configuration.configuration import configuracion
from pydantic import BaseModel
from fastapi.param_functions import Body
from models.estudianteClass import estudianteClass, addUserAndStudent, addEstudianteByUserId, getTop5MayorPuntaje

student_router = APIRouter()

async def getConexion():
    conn = await aiomysql.connect(
        host=configuracion['development'].MYSQL_HOST, 
        user=configuracion['development'].MYSQL_USER, 
        password=configuracion['development'].MYSQL_PASSWORD, 
        db=configuracion['development'].MYSQL_DB, charset='utf8', 
        cursorclass=aiomysql.DictCursor)
    return conn

@student_router.get("/getStudents")
async def getStudents():
    conn = await getConexion()
    try:
        usuarios=[]
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Estudiante")
            resultado = await cur.fetchall()
            for result in resultado:
                usuario = {
                    'usuario_estudiante': result['usuario_estudiante'],
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

@student_router.post("/addUserAndStudents")
async def addUserAndStudents(request: Request, estudiante: addUserAndStudent = Body(...)):
    conn = await getConexion()
    try:
        username = estudiante.nombre_usuario
        password = estudiante.contrasena_usuario
        rol = estudiante.rol_usuario
        nombres=estudiante.nombres_estudiante
        apellidos=estudiante.apellidos_estudiante
        cedula=estudiante.cedula_estudiante
        fechaNacimiento=estudiante.fechaNacimiento_estudiante
        edad=estudiante.edad_estudiante
        direccion=estudiante.direccion_estudiante
        telefono=estudiante.telefono_estudiante
        email=estudiante.email_estudiante
        nivelEducacion=estudiante.nivelEducacion_estudiante
        promedioAnterior=estudiante.promedioAnterior_estudiante
        medio=estudiante.medio_estudiante
        global usuarioInsertado
        usuarioInsertado=False
        async with conn.cursor() as cur:
            await cur.execute(
                """INSERT INTO Usuario(nombre_usuario, contrasena_usuario, rol_usuario) 
                VALUES ('{0}','{1}','{2}')""".
                format(username,password,rol))
            await conn.commit()
            if cur.rowcount > 0:
                usuarioInsertado=True
            else :
                usuarioInsertado=False
        global id_usuario
        if usuarioInsertado:
            id_usuario=0
            async with conn.cursor() as cur:
                await cur.execute(
                    """Select id_usuario from Usuario 
                    where nombre_usuario='{0}' and contrasena_usuario='{1}'""".
                    format(username,password))
                result = await cur.fetchone()
                id_usuario=result['id_usuario']   
        global estudianteInsertado
        if usuarioInsertado ==True and id_usuario > 0:
            estudianteInsertado=False
            async with conn.cursor() as cur:
                await cur.execute (
                    """INSERT INTO Estudiante(usuario_estudiante, nombres_estudiante, 
                    apellidos_estudiante, cedula_estudiante, fechaNacimiento_estudiante, 
                    edad_estudiante, direccion_estudiante, telefono_estudiante, email_estudiante, 
                    nivelEducacion_estudiante, promedioAnterior_estudiante, medio_estudiante) 
                    VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')""".
                    format(id_usuario,nombres,apellidos,cedula,fechaNacimiento,edad,
                           direccion,telefono,email,nivelEducacion,promedioAnterior,medio))
                await conn.commit()
                if cur.rowcount > 0:
                    estudianteInsertado=True
                else:
                    estudianteInsertado=False
        if usuarioInsertado and estudianteInsertado:
            return {'data': [{'usuario':usuarioInsertado,'estudiante':estudianteInsertado}], 'accion':True}
        else:
            return {'data': [{'usuario':usuarioInsertado,'estudiante':estudianteInsertado}], 'accion': False}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@student_router.post("/addEstudianteByUserId")
async def addEstudianteByUserId(request: Request, estudiante: addEstudianteByUserId = Body(...)):
    conn = await getConexion()
    try:
        id_usuario=estudiante.usuario_estudiante
        nombres=estudiante.nombres_estudiante
        apellidos=estudiante.apellidos_estudiante
        cedula=estudiante.cedula_estudiante
        fechaNacimiento=estudiante.fechaNacimiento_estudiante
        edad=estudiante.edad_estudiante
        direccion=estudiante.direccion_estudiante
        telefono=estudiante.telefono_estudiante
        email=estudiante.email_estudiante
        nivelEducacion=estudiante.nivelEducacion_estudiante
        promedioAnterior=estudiante.promedioAnterior_estudiante
        medio=estudiante.medio_estudiante
        global estudianteInsertado
        estudianteInsertado=False
        async with conn.cursor() as cur:
            await cur.execute (
                """INSERT INTO Estudiante(usuario_estudiante, nombres_estudiante, apellidos_estudiante, 
                cedula_estudiante, fechaNacimiento_estudiante, edad_estudiante, direccion_estudiante, 
                telefono_estudiante, email_estudiante, nivelEducacion_estudiante, promedioAnterior_estudiante, 
                medio_estudiante) 
                VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')""".
                format(id_usuario,nombres,apellidos,cedula,fechaNacimiento,edad,direccion,
                       telefono,email,nivelEducacion,promedioAnterior,medio))
            await conn.commit()
            if cur.rowcount > 0:
                estudianteInsertado=True
            else:
                estudianteInsertado=False
        if estudianteInsertado:
            return {'data': [{'estudiante':estudianteInsertado}], 'accion': True}
        else:
            return {'data': [{'estudiante':estudianteInsertado}], 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': "false"}
    finally:
        conn.close()

@student_router.post("/getTop5Estudiantes")
async def getTop5Estudiantes(request: Request, estudiante: getTop5MayorPuntaje = Body(...)):
    conn = await getConexion()
    try:
        top5MayorPuntaje=[]
        ciclo=estudiante.ciclo_matricula
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT id_estudiante, concat(nombres_estudiante, ' ', 
                apellidos_estudiante) AS nombrescompletos_estudiante, 
                ROUND(avg(promedioCalificaciones_itemActa), 2) AS promedio_estudiante 
                FROM Estudiante, Acta, ItemActa, Matricula 
                WHERE estudiante_matricula = id_estudiante AND id_estudiante = estudiante_itemActa AND ciclo_matricula = '{0}' 
                group by id_estudiante ORDER BY avg(promedioCalificaciones_itemActa) DESC LIMIT 5""".format(ciclo))
            result = await cur.fetchall()
            for row in result:
                top5MayorPuntaje.append({
                    'id_estudiante':row['id_estudiante'],
                    'nombrescompletos_estudiante':row['nombrescompletos_estudiante'],
                    'promedio_estudiante':row['promedio_estudiante']})
        return {'data': top5MayorPuntaje, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@student_router.get("/getAdminEstudiantes")
async def getAdminEstudiantes():
    conn = await getConexion()
    try:
        estudiantes=[]
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT id_estudiante, cedula_estudiante, CONCAT(nombres_estudiante, ' ', 
                apellidos_estudiante) AS nombresCompletos_estudiante, MAX(ciclo_matricula) AS ultimo_ciclo, 
                medio_estudiante 
                FROM Estudiante LEFT JOIN Matricula ON id_estudiante = estudiante_matricula 
                GROUP BY id_estudiante 
                ORDER BY STR_TO_DATE(SUBSTRING_INDEX(4, ' ', 1), '%Y-%Y-%b');""")
            resultado = await cur.fetchall()
            for result in resultado:
                estudiante = {'id_estudiante': result['id_estudiante']
                              ,'cedula_estudiante': result['cedula_estudiante']
                              ,'nombresCompletos_estudiante': result['nombresCompletos_estudiante']
                              ,'ultimo_ciclo': result['ultimo_ciclo']
                              ,'medio_estudiante': result['medio_estudiante']}
                estudiantes.append(estudiante)
        return {'data': estudiantes, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()