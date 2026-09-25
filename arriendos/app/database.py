import os

from pymongo import MongoClient

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017"
)

MONGO_DB = os.getenv(
    "MONGO_DB",
    "arriendos_db"
)

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS = 5000
)

db = client[MONGO_DB]

clientes_collection = db["clientes"]
arriendos_collection = db["arriendos"]

def verificar_conexion():
    client.admin.command("ping")