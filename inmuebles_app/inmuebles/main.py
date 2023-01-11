from fastapi import FastAPI
from pymongo import MongoClient

from .models import Inmueble
from .routes import router

connection_string = "mongodb+srv://uda_prueba_usuario:eficaciacomunicacionentusiasmo@cluster0.shwu1ii.mongodb.net/?retryWrites=true&w=majority"
db_name = "inmueble"


inmuebles = FastAPI()

@inmuebles.on_event("startup")
def start_db_client():
    inmuebles.db_client = MongoClient(connection_string)
    inmuebles.database = inmuebles.db_client[db_name]
    print("Connected successfully to DB")

@inmuebles.on_event("shutdown")
def stop_db_client():
    inmuebles.db_client.close()
    print("Disconnected from DB")

inmuebles.include_router(router, tags=["inmuebles"], prefix="/inmuebles")
