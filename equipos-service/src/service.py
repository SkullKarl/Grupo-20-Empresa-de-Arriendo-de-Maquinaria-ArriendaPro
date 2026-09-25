import os
import sys
import time
import grpc
import equipo_pb2
import equipo_pb2_grpc
from concurrent import futures
from database import db, init_db

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
equipos_collection = db["equipos"]

class EquipoService(equipo_pb2_grpc.EquipoServiceServicer):

    def GetEquipo(self, request, context):
            eq = equipos_collection.find_one({"id": request.id})
            if not eq:
                context.abort(grpc.StatusCode.NOT_FOUND, f"El equipo con ID {request.id} no existe")
            
            equipo_msg = equipo_pb2.Equipo(
                id=eq["id"],
                name=eq["name"],
                type=eq["type"],
                total_units=eq["total_units"],
                available_units=eq["available_units"]
            )
            return equipo_pb2.GetEquipoResponse(equipo=equipo_msg)
    
    def ListCatalog(self, request, context):
        equipos_list = []
        for eq in equipos_collection.find():
            equipos_list.append(equipo_pb2.Equipo(
                id=eq["id"],
                name=eq["name"],
                type=eq["type"],
                total_units=eq["total_units"],
                available_units=eq["available_units"]
            ))
        return equipo_pb2.ListCatalogResponse(equipos=equipos_list)
    
    def ModifyReservation(self, request, context):
        eq = equipos_collection.find_one({"id": request.equipment_id})
        if not eq:
            context.abort(grpc.StatusCode.NOT_FOUND, "Equipo no encontrado")

        if request.operation == equipo_pb2.RESERVE:
            if eq["available_units"] >= request.quantity:
                new_units = eq["available_units"] - request.quantity
                equipos_collection.update_one(
                    {"id": request.equipment_id},
                    {"$set": {"available_units": new_units}}
                )
                return equipo_pb2.ModifyReservationResponse(
                    success=True,
                    message="Reserva realizada con éxito",
                    current_available_units=new_units
                )
            else:
                return equipo_pb2.ModifyReservationResponse(
                    success=False,
                    message="Stock insuficiente",
                    current_available_units=eq["available_units"]
                )

        elif request.operation == equipo_pb2.RELEASE:
            new_units = eq["available_units"] + request.quantity
            if new_units > eq["total_units"]:
                new_units = eq["total_units"]
                
            equipos_collection.update_one(
                {"id": request.equipment_id},
                {"$set": {"available_units": new_units}}
            )
            return equipo_pb2.ModifyReservationResponse(
                success=True,
                message="Equipo liberado correctamente",
                current_available_units=new_units
            )

        return equipo_pb2.ModifyReservationResponse(
            success=False,
            message="Operación desconocida",
            current_available_units=eq["available_units"]
        )

def server():
    for i in range(5):
        try:
            init_db()
            break
        except Exception as e:
            print(f"Esperando a MongoDB... intento {i+1}/5")
            time.sleep(3)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    equipo_pb2_grpc.add_EquipoServiceServicer_to_server(EquipoService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC de Equipos corriendo en el puerto 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    server()