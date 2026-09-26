FROM python:3.12-slim

WORKDIR /code

COPY arriendos/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY arriendos/app/ ./app/
COPY equipos-service/equipo.proto ./proto/equipo.proto

RUN mkdir -p app/generated && \
    touch app/generated/__init__.py && \
    python -m grpc_tools.protoc \
        -I./proto \
        --python_out=./app/generated \
        --grpc_python_out=./app/generated \
        ./proto/equipo.proto && \
    sed -i 's/^import equipo_pb2 as equipo__pb2$/from . import equipo_pb2 as equipo__pb2/' \
        app/generated/equipo_pb2_grpc.py

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]