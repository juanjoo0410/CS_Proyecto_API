from fastapi import  FastAPI,Request
from fastapi import APIRouter
import aiomysql
from configuration.configuration import configuracion
from pydantic import BaseModel
from fastapi.param_functions import Body
from models.docenteClass import docenteClass, addUserAndDocente, addDocenteByUserId, addPagoDocente, getTop5MayorPuntaje, updateOnePromedioDocente

teacher_router = APIRouter()

async def getConexion():
    conn = await aiomysql.connect(
        host=configuracion['development'].MYSQL_HOST, 
        user=configuracion['development'].MYSQL_USER, 
        password=configuracion['development'].MYSQL_PASSWORD, 
        db=configuracion['development'].MYSQL_DB, charset='utf8', 
        cursorclass=aiomysql.DictCursor)
    return conn


@teacher_router.get("/getTeachers")
async def getTeachers():
    conn = await getConexion()
    try:
        usuarios=[]
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM Docente")
            resultado = await cur.fetchall()
            for result in resultado:
                usuario = {
                    'usuario_docente': result['usuario_docente'],
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
        return {'data': usuarios, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@teacher_router.post("/addUserAndTeachers")
async def addUserAndTeachers(request: Request, docente: addUserAndDocente = Body(...)):
    conn = await getConexion()
    try:
        username = docente.nombre_usuario
        password = docente.contrasena_usuario
        rol = docente.rol_usuario
        nombres = docente.nombres_docente
        apellidos = docente.apellidos_docente
        cedula = docente.cedula_docente
        fechaNacimiento = docente.fechaNacimiento_docente
        edad = docente.edad_docente
        direccion = docente.direccion_docente
        telefono = docente.telefono_docente
        email = docente.email_docente
        titulo = docente.titulo_docente
        nivelEducacion = docente.nivelEducacion_docente
        promedio = docente.promedio_docente
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
                    """Select id_usuario 
                    from Usuario 
                    where nombre_usuario='{0}' and contrasena_usuario='{1}'""".
                    format(username,password))
                result = await cur.fetchone()
                id_usuario=result['id_usuario']   
        global docenteInsertado
        if usuarioInsertado ==True and id_usuario > 0:
            docenteInsertado=False
            async with conn.cursor() as cur:
                await cur.execute(
                    """INSERT INTO Docente(usuario_docente, nombres_docente, apellidos_docente, 
                    cedula_docente, fechaNacimiento_docente, edad_docente, direccion_docente, 
                    telefono_docente, email_docente, titulo_docente, nivelEducacion_docente,promedio_docente) 
                    VALUES ({0},'{1}','{2}','{3}','{4}',{5},'{6}','{7}','{8}','{9}','{10}','{11}')""".
                    format(id_usuario,nombres,apellidos,cedula,fechaNacimiento,edad,
                           direccion,telefono,email,titulo,nivelEducacion,promedio))
                await conn.commit()
                if cur.rowcount > 0:
                    docenteInsertado=True
                else:
                    docenteInsertado=False
        if usuarioInsertado and docenteInsertado:
            return {'data': [{'usuario':usuarioInsertado,'docente':docenteInsertado}], 'accion':True}
        else:
            return {'data': [{'usuario':usuarioInsertado,'docente':docenteInsertado}], 'accion': False}
    except Exception as error:
        return {'data': error, 'accion': False}
    finally:
        conn.close()

@teacher_router.post("/addTeachersByUserId")
async def addTeachersByUserId(request: Request, docente: addDocenteByUserId = Body(...)):
    conn = await getConexion()
    try: 
        id_usuario = docente.usuario_docente
        nombres = docente.nombres_docente
        apellidos = docente.apellidos_docente
        cedula = docente.cedula_docente
        fechaNacimiento = docente.fechaNacimiento_docente
        edad = docente.edad_docente
        direccion = docente.direccion_docente
        telefono = docente.telefono_docente
        email = docente.email_docente
        titulo = docente.titulo_docente
        nivelEducacion = docente.nivelEducacion_docente
        promedio = docente.promedio_docente
        global docenteInsertado
        docenteInsertado=False
        async with conn.cursor() as cur:
            await cur.execute(
                """INSERT INTO Docente(usuario_docente, nombres_docente, apellidos_docente, cedula_docente, 
                fechaNacimiento_docente, edad_docente, direccion_docente, telefono_docente, email_docente, 
                titulo_docente, nivelEducacion_docente,promedio_docente) 
                VALUES ({0},'{1}','{2}','{3}','{4}',{5},'{6}','{7}','{8}','{9}','{10}','{11}')""".
                format(id_usuario,nombres,apellidos,cedula,fechaNacimiento,edad,
                       direccion,telefono,email,titulo,nivelEducacion,promedio))
            await conn.commit()
            if cur.rowcount > 0:
                docenteInsertado=True
            else:
                docenteInsertado=False
        if docenteInsertado:
            return {'data': [{'docente':docenteInsertado}], 'accion': True}
        else:
            return {'data': [{'docente':docenteInsertado}], 'accion': False}
    except:
        pass
    finally:
        conn.close()

@teacher_router.get("/getPaymentTeacher")
async def getPaymentTeacher(request: Request):
    conn = await getConexion()
    try:
        pagoDocente = []
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM PagoDocente")
            result = await cur.fetchall()
            for pago in result:
                pagoDocente.append(pago)
        return {'data': pagoDocente, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@teacher_router.post("/addPaymentTeacher")
async def addPaymentTeacher(request: Request, pago: addPagoDocente = Body(...)):
    conn = await getConexion()
    try:
        idDocente= pago.docente_pagoDocente
        fecha = pago.fecha_pagoDocente
        faltas = pago.faltas_pagoDocente
        descuento = pago.descuento_pagoDocente
        total = pago.total_pagoDocente
        global pagoInsertado
        pagoInsertado=False
        async with conn.cursor() as cur:
            await cur.execute(
                """INSERT INTO PagoDocente(docente_pagoDocente, fecha_pagoDocente, 
                faltas_pagoDocente, descuento_pagoDocente, total_pagoDocente) 
                VALUES ({0},'{1}',{2},{3},{4})""".
                format(idDocente,fecha,faltas,descuento,total))
            await conn.commit()
            if cur.rowcount > 0:
                pagoInsertado=True
            else:
                pagoInsertado=False
        if pagoInsertado:
            return {'data': [{'pago':pagoInsertado}], 'accion': True}
        else:
            return {'data': [{'pago':pagoInsertado}], 'accion': False}
    except Exception as error:
        return {'data': error, 'accion': False}
    finally:
        conn.close()

@teacher_router.post("/getTop5Teacher")
async def getTop5Teacher(request: Request, puntaje: getTop5MayorPuntaje = Body(...)):
    conn = await getConexion()
    try:
        top5mayorPuntaje = []
        ciclo = puntaje.ciclo_contrato
        async with conn.cursor() as cur:
            await cur.execute(
                """SELECT id_docente, concat(nombres_docente, ' ', 
                apellidos_docente) AS nombrescompletos_docente, promedio_docente 
                FROM Docente, Contrato 
                WHERE docente_contrato = id_docente AND ciclo_contrato = '{0}' 
                ORDER BY promedio_docente DESC LIMIT 5""".format(ciclo))
            result = await cur.fetchall()
            for top in result:
                docente= {
                    'id_docente': top['id_docente'], 
                    'nombrescompletos_docente': top['nombrescompletos_docente'], 
                    'promedio_docente': top['promedio_docente']}
                top5mayorPuntaje.append(docente)
        return {'data': top5mayorPuntaje, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@teacher_router.get("/getAdminDocentes")
async def getAdminDocentes():
    conn = await getConexion()
    try:
        AdminDocentes = []
        async with conn.cursor() as cur:
            await cur.execute("""SELECT id_docente, cedula_docente, concat(nombres_docente, ' ', 
                                apellidos_docente) AS nombresCompletos_docente, ciclo_contrato, estado_docente, 
                                tipo_contrato
                                FROM Docente, Contrato
                                WHERE docente_contrato = id_docente
                                UNION
                                SELECT id_docente, cedula_docente, CONCAT(nombres_docente, ' ', 
                                apellidos_docente) AS nombresCompletos_docente, NULL AS ciclo_contrato, NULL AS 
                                estado_docente, NULL AS tipo_contrato
                                FROM Docente
                                WHERE id_docente NOT IN (SELECT DISTINCT docente_contrato FROM 
                                Contrato);
                                """)
            result = await cur.fetchall()
            for top in result:
                AdminDocente= {
                    'id_docente': top['id_docente'], 
                    'cedula_docente': top['cedula_docente'], 
                    'nombresCompletos_docente': top['nombresCompletos_docente'],
                    'ciclo_contrato': top['ciclo_contrato'],
                    'estado_docente': top['estado_docente'],
                    'tipo_contrato': top['tipo_contrato']}
                AdminDocentes.append(AdminDocente)
        return {'data': AdminDocentes, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()

@teacher_router.put("/updatePromedioDocente")
async def updatePromedioDocente(request: Request, docente: updateOnePromedioDocente = Body(...)):
    conn = await getConexion()
    try:
        promedio_docente = docente.promedio_docente
        id_docente=docente.id_docente
        async with conn.cursor() as cur:
            await cur.execute(
                """UPDATE Docente SET promedio_docente = '{0}' 
                WHERE id_docente = '{1}';""".
                format(promedio_docente,id_docente))
            result= await conn.commit()
            print(cur.rownumber)
            print(cur.rowcount)
            if cur.rowcount>0:
                return {'data': {'actualizado':True}, 'accion': True}
            else:
                return {'data': {'actualizado':False}, 'accion': True}
    except Exception as e:
        return {'data': '', 'accion': False}
    finally:
        conn.close()