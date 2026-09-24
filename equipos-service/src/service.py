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

class EquipoService(equipo_pb2_grpc.EquipoService):
    
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

def service():
    for i in range(5):
        try:
            init_db()
            break
        except Exception as e:
            print(f"Esperando a MongoDB... intento {i+1}/5")
            time.sleep(3)

    service = grpc.service(futures.ThreadPoolExecutor(max_workers=10))
    equipo_pb2_grpc.add_EquipoService_to_service(EquipoService(), service)
    service.add_insecure_port('[::]:50051')
    service.start()
    print("Servidor gRPC de Equipos corriendo en el puerto 50051")
    service.wait_for_termination()

if __name__ == '__main__':
    service()