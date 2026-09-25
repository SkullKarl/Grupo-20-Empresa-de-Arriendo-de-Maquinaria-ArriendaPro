import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["equipos_db"]
equipos_collection = db["equipos"]

def init_db():
    #Inicializar la base de datos con datos de prueba si está vacía
    if equipos_collection.count_documents({}) == 0:
        equipos_iniciales = [
            {
                "id": "001",
                "name": "Excavadora Hidráulica 3200g",
                "type": "Maquinaria Pesada",
                "total_units": 69,
                "available_units": 67
            },
            {
                "id": "002",
                "name": "Freidora de Aire Portátil",
                "type": "Herramientas Menores",
                "total_units": 10,
                "available_units": 9
            }
        ]
        equipos_collection.insert_many(equipos_iniciales)
        print("Base de datos de MongoDB inicializada.")