from fastapi import APIRouter
from fastapi import  FastAPI,Request

home_router = APIRouter()

@home_router.get("/")
def home(request:Request):
    return {"message":"Hola Mundo"}