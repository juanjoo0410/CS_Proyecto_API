from controllers.usuarioController import user_router
from controllers.homeController import home_router
from controllers.docenteController import teacher_router
from controllers.estudianteController import student_router
from controllers.moduloController import modulo_router
from controllers.paraleloController import paralelo_router
from controllers.medioController import medio_router
from controllers.rolController import rol_router
from controllers.cursoController import course_router
from controllers.actaController import acta_router
from controllers.horarioController import horario_router
from controllers.asistenciaController import asistencia_router
from controllers.contratoController import contrato_router
from controllers.evaluacionController import evaluacion_router
from controllers.itemActaController import itemActa_router
from controllers.itemMatriculaController import itemMatricula_router
from controllers.materiaController import materia_router
from controllers.matriculaController import matricula_router
from controllers.ordenPagoMatriculaController import ordenPago_router
from controllers.pagoDocenteController import pagoDocente_router
from controllers.actividadController import actividad_router
from controllers.entregaController import entrega_router

from configuration.configuration import configuracion

from fastapi import  FastAPI,Request
from fastapi import APIRouter
import uvicorn
from pydantic import BaseModel

from fastapi.param_functions import Body
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    entrega_router,
    prefix='/api/v1/entregas',
    tags=['Entregas'],
    responses={404: {'description': 'Error de acceso a la ventana de entregas'}},
)

app.include_router(
    actividad_router,
    prefix='/api/v1/actividades',
    tags=['Actividades'],
    responses={404: {'description': 'Error de acceso a la ventana de actividades'}},
)

app.include_router(
    pagoDocente_router,
    prefix='/api/v1/pagoDocentes',
    tags=['PagoDocentes'],
    responses={404: {'description': 'Error de acceso a la ventana de pagoDocentes'}},
)

app.include_router(
    ordenPago_router,
    prefix='/api/v1/ordenPagoMatriculas',
    tags=['OrdenPagoMatriculas'],
    responses={404: {'description': 'Error de acceso a la ventana de ordenPagoMatriculas'}},
)

app.include_router(
    matricula_router,
    prefix='/api/v1/matriculas',
    tags=['Matriculas'],
    responses={404: {'description': 'Error de acceso a la ventana de matriculas'}},
)

app.include_router(
    materia_router,
    prefix='/api/v1/materias',
    tags=['Materias'],
    responses={404: {'description': 'Error de acceso a la ventana de materias'}},
)

app.include_router(
    itemMatricula_router,
    prefix='/api/v1/itemMatriculas',
    tags=['ItemMatriculas'],
    responses={404: {'description': 'Error de acceso a la ventana de itemMatriculas'}},
)

app.include_router(
    itemActa_router,
    prefix='/api/v1/itemActas',
    tags=['ItemActas'],
    responses={404: {'description': 'Error de acceso a la ventana de itemActas'}},
)

app.include_router(
    evaluacion_router,
    prefix='/api/v1/evaluaciones',
    tags=['Evaluaciones'],
    responses={404: {'description': 'Error de acceso a la ventana de evaluaciones'}},
)

app.include_router(
    contrato_router,
    prefix='/api/v1/contratos',
    tags=['Contratos'],
    responses={404: {'description': 'Error de acceso a la ventana de contratos'}},
)

app.include_router(
    asistencia_router,
    prefix='/api/v1/asistencias',
    tags=['Asistencias'],
    responses={404: {'description': 'Error de acceso a la ventana de asistencias'}},
)

app.include_router(
    horario_router,
    prefix='/api/v1/horarios',
    tags=['Horarios'],
    responses={404: {'description': 'Error de acceso a la ventana de horarios'}},
)

app.include_router(
    acta_router,
    prefix='/api/v1/actas',
    tags=['Actas'],
    responses={404: {'description': 'Error de acceso a la ventana de actas'}},
)

app.include_router(
    course_router,
    prefix='/api/v1/cursos',
    tags=['Cursos'],
    responses={404: {'description': 'Error de acceso a la ventana de cursos'}},
)

app.include_router(
    rol_router,
    prefix='/api/v1/roles',
    tags=['Roles'],
    responses={404: {'description': 'Error de acceso a la ventana de roles'}},
)

app.include_router(
    medio_router,
    prefix='/api/v1/medios',
    tags=['Medios'],
    responses={404: {'description': 'Error de acceso a la ventana de medios'}}
)

app.include_router(
    paralelo_router,
    prefix='/api/v1/paralelos',
    tags=['Paralelos'],
    responses={404: {'description': 'Error de acceso a la ventana de paralelos'}}
)

app.include_router(
    modulo_router,
    prefix='/api/v1/modulos',
    tags=['Modulos'],
    responses={404: {'description': 'Error de acceso a la ventana de modulos'}}
)

app.include_router(
    student_router,
    prefix='/api/v1/estudiantes',
    tags=['Estudiantes'],
    responses={404: {'description': 'Error de acceso a la ventana de estudiantes'}}
)

app.include_router(
    teacher_router,
    prefix='/api/v1/docentes',
    tags=['Docentes'],
    responses={404: {'description': 'Error de acceso a la ventana de docentes'}}
)

app.include_router(
    user_router,
    prefix='/api/v1/usuarios',
    tags=['Usuarios'],
    responses={404: {'description': 'Error de acceso a la ventana de usuarios'}}
)

app.include_router(
    home_router,
    prefix='/home',
    tags=['Inicio'],
    responses={404: {'description': 'Error de acceso a la ventana en home'}}
)

if __name__=="__main__":
    uvicorn.run(app,host=configuracion['development'].HOST,port=configuracion['development'].PORT)