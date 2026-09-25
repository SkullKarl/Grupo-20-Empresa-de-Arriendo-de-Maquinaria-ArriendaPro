from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status
from pymongo.errors import DuplicateKeyError

from app.database import clientes_collection
from app.models.cliente import Cliente, ClienteInput

router = APIRouter(
    prefix = "/v1/clientes",
    tags = ["Clientes"]
)

@router.get("", response_model = list[Cliente])
def listar_clientes():

    documentos = clientes_collection.find(
        {},
        {"_id": 0}
    )
    return list(documentos)

@router.post("", response_model = Cliente, status_code = status.HTTP_201_CREATED)
def crear_clientes(cliente: ClienteInput):

    nuevo_cliente = Cliente(
        id = str(uuid4()),
        nombre = cliente.nombre,
        email=cliente.email,
        telefono = cliente.telefono
    )

    documento = nuevo_cliente.model_dump(mode= "json")

    try:
        clientes_collection.insert_one(documento)

    except DuplicateKeyError:
        raise HTTPException(
            status_code = 409,
            detail = "Ya existe un cliente con ese id"
        )

    return nuevo_cliente

@router.get("/{id}", response_model = Cliente)
def consultar_Cliente(id: str):

    # ID tiene formato UUID
    try:
        UUID(id)
    except ValueError:
        raise HTTPException(
            status_code = 400,
            detail = "El ID del cliente no tiene un formato UUID válido"
        )

    # Buscar cliente
    documento = clientes_collection.find_one(
        {"id": id},
        {"_id": 0}
    )

    # Si no existe, devolver 404
    if documento is None:
        raise HTTPException(
            status_code = 404,
            detail = "Cliente no encontrado"
    )

    return documento