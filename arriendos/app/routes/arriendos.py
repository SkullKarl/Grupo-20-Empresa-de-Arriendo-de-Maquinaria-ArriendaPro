from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status
from pymongo import ReturnDocument
from pymongo.errors import PyMongoError

from app.database import arriendos_collection, clientes_collection
from app.models.arriendo import Arriendo, ArriendoInput

from app.services.equipos_client import (
    EquiposNoDisponible,
    EquiposOperacionRechazada,
    reservar_equipo,
    liberar_equipo
)

router = APIRouter(
    prefix = "/v1/arriendos",
    tags = ["Arriendos"]
)

@router.get("", response_model = list[Arriendo])
def listar_arriendos():

    documentos = arriendos_collection.find(
        {},
        {"_id": 0}
    )

    return list(documentos)

@router.get("/{id}", response_model = Arriendo)
def consultar_arriendo(id: str):

    # Comprobar formato UUID para id
    try:
        UUID(id)
    except ValueError:
        raise HTTPException(
            status_code = 400,
            detail="El ID del arriendo no tiene un formato UUID válido"
        )

    # Buscar arriendo
    documento = arriendos_collection.find_one(
        {"id": id},
        {"_id": 0}
    )

    # No se encontró arriendo
    if documento is None:
        raise HTTPException(
            status_code = 404,
            detail = "Arriendo no encontrado"
        )
    return documento

@router.post("", response_model = Arriendo, status_code = status.HTTP_201_CREATED)
def registrar_arriendo(arriendo: ArriendoInput):

    # Comprobar fechas
    if arriendo.fecha_fin < arriendo.fecha_inicio:
        raise HTTPException(
            status_code = 400,
            detail = "La fecha de término no puede ser anterior a la fecha de inicio"
        )
    # Comprobar que el cliente existe
    cliente = clientes_collection.find_one(
        {"id": str(arriendo.cliente_id)},
        {"_id": 0}
    )

    if cliente is None:
        raise HTTPException(
            status_code = 400,
            detail = "El cliente indicado no existe"
        )

    # Solicitar reserva a Equipos con gRPC
    try:
        reservar_equipo(arriendo.equipo_id, arriendo.cantidad)

    except EquiposNoDisponible:
        raise HTTPException(
            status_code = 503,
            detail = "Servicio de Equipos no disponible"
        )
    except EquiposOperacionRechazada as error:
        raise HTTPException(
            status_code = 400,
            detail = str(error)
        )

    # Crear contrato de arriendo
    nuevo_arriendo = Arriendo(
        id = uuid4(),
        **arriendo.model_dump(),
        estado = "activo"
    )

    documento = nuevo_arriendo.model_dump(mode = "json")

    # Guardar en base de datos
    try:
        arriendos_collection.insert_one(documento)
    except PyMongoError:
        try:
            liberar_equipo(arriendo.equipo_id, arriendo.cantidad)
        except (EquiposNoDisponible, EquiposOperacionRechazada):
            pass

        raise HTTPException(
            status_code = 503,
            detail = "No fue posible guardar el arriendo"
        )

    return nuevo_arriendo

@router.post("/{id}/devolucion", response_model = Arriendo)
def devolver_arriendo(id: str):

    # Comprobar UUID para id
    try:
        UUID(id)
    except ValueError:
        raise HTTPException(
            status_code = 400,
            detail = "El ID del arriendo no tiene un formato UUID válido"
        )
    # Buscar arriendo
    documento = arriendos_collection.find_one(
        {"id": id},
        {"_id": 0}
    )

    # No se encontró arriendo
    if documento is None:
        raise HTTPException(
            status_code = 404,
            detail = "Arriendo no encontrado"
        )

    # Comprobar si arriendo ya fue devuelto
    if documento["estado"] == "devuelto":
        raise HTTPException(
            status_code = 400,
            detail = "El arriendo ya fue devuelto"
        )

    # Solicitar liberación de unidades a Equipos
    try:
        liberar_equipo(
            documento["equipo_id"],
            documento["cantidad"]
        )
    except EquiposNoDisponible:
        raise HTTPException(
            status_code = 503,
            detail = "Servicio de Equipos no disponible"
        )

    except EquiposOperacionRechazada as error:
        raise HTTPException(
            status_code = 400,
            detail = str(error)
        )

    # Actualizar estado en base de datos
    try:
        documento_actualizado = arriendos_collection.find_one_and_update(
            {"id": id, "estado": "activo"},
            {"$set": {"estado": "devuelto"}},
            projection = {"_id": 0},
            return_document = ReturnDocument.AFTER
        )

    except PyMongoError:
        raise HTTPException(
            status_code = 503,
            detail = "Se liberó el equipo, pero no se pudo actualizar el arriendo"
        )

    if documento_actualizado is None:
        raise HTTPException(
            status_code = 503,
            detail = "No fue posible confirmar la devolución"
        )

    return documento_actualizado