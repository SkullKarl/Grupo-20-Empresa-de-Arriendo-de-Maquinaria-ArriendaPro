import os

import grpc

from app.generated import equipo_pb2, equipo_pb2_grpc

EQUIPOS_GRPC_ADDRESS = os.getenv(
    "EQUIPOS_GRPC_ADDRESS",
    "equipos:50051"
)

GRPC_TIMEOUT = 3.0

class EquiposNoDisponible(Exception):
    pass

class EquiposOperacionRechazada(Exception):
    pass

def _ejecutar_rpc(operacion):
    try:
        with grpc.insecure_channel(EQUIPOS_GRPC_ADDRESS) as channel:
            stub = equipo_pb2_grpc.EquipoServiceStub(channel)
            return operacion(stub)
    except grpc.RpcError as exc:
        raise EquiposNoDisponible(
            "No fue posible comunicarse con el servicio de Equipos"
        ) from exc

def obtener_equipo(equipo_id: str):
    respuesta = _ejecutar_rpc(
        lambda stub: stub.GetEquipo(
            equipo_pb2.GetEquipoRequest(id = equipo_id),
            timeout = GRPC_TIMEOUT
        )
    )

    if not respuesta.HasField("equipo"):
        raise EquiposOperacionRechazada(
            "El equipo solicitado no existe"
        )

    return respuesta.equipo

def modificar_reserva(
        equipo_id: str,
        cantidad: int,
        operacion: int
):
    respuesta = _ejecutar_rpc(
        lambda stub: stub.SetReserva(
            equipo_pb2.SetReservaRequest(
                equipo_id = equipo_id,
                quantity = cantidad,
                operation = operacion
            ),
            timeout = GRPC_TIMEOUT
        )
    )

    if not respuesta.success:
        raise EquiposOperacionRechazada(
            respuesta.message or "Equipos rechazó la operación"
        )
    return respuesta

def reservar_equipo(equipo_id: str, cantidad: int):
    return modificar_reserva(
        equipo_id,
        cantidad,
        equipo_pb2.RESERVE
    )

def liberar_equipo(equipo_id: str, cantidad: int):
    return modificar_reserva(
        equipo_id,
        cantidad,
        equipo_pb2.RELEASE
    )