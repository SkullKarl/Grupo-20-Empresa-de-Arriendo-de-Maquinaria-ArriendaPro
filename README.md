# Grupo-20-Empresa-de-Arriendo-de-Maquinaria-ArriendaPro

# ArriendaPro

Proyecto desarrollado para el curso **Integración de Sistemas** de la Universidad de Concepción.

ArriendaPro implementa la integración entre dos sistemas independientes de una empresa de arriendo de maquinaria:

- **Arriendos:** gestiona clientes y contratos de arriendo mediante una API REST.
- **Equipos:** administra el catálogo de maquinaria y sus unidades disponibles mediante un servicio gRPC.

La integración permite verificar y modificar la disponibilidad de los equipos al momento de registrar o devolver un arriendo.

---

## Arquitectura

El sistema se divide en dos servicios principales:

- Servicio de Arriendos
- Servicio de Equipos

Cada servicio posee su propia base de datos. Arriendos no accede directamente a los datos de Equipos; toda interacción entre ambos servicios se realiza mediante gRPC.

### Tecnologías principales

- Python
- FastAPI
- gRPC
- Protocol Buffers
- MongoDB
- Docker
- Docker Compose
- OpenAPI

---

## Estructura del proyecto

```text
.
├── arriendos/
│   ├── app/
│   │   ├── generated/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── database.py
│   │   ├── errors.py
│   │   ├── main.py
│   │   └── security.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── equipos-service/
│   ├── src/
│   ├── Dockerfile
│   └── equipo.proto
│
├── contracts/
│   └── openapi.yaml
│
├── docs/
│   └── adr/
│       ├── ADR-001-descomposicion-servicios.md
│       ├── ADR-002-rest-grpc.md
│       ├── ADR-003-evolucion-contratos.md
│       └── ADR-004-resiliencia.md
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Requisitos

Para ejecutar el proyecto se necesita:

- Docker
- Docker Compose

---

## Configuración

Antes de levantar el sistema, crear un archivo `.env` en la raíz del proyecto.

Puede utilizarse `.env.example` como referencia:

```env
ARRIENDOS_API_KEY=clave-local-de-prueba
```

La API Key se utiliza para autenticar las solicitudes realizadas a la API REST de Arriendos.

> El archivo `.env` contiene configuración local y no debe subirse al repositorio.

---

## Ejecución

Desde la raíz del proyecto ejecutar:

```bash
docker compose up --build
```

Docker Compose construirá y levantará los cuatro componentes principales:

```text
arriendos
equipos-service
mongo_arriendos
mongo-equipos
```

Para comprobar su estado:

```bash
docker compose ps
```

---

## API REST

Una vez iniciado el sistema, la documentación interactiva de la API puede consultarse mediante Swagger en:

```text
http://localhost:8080/docs
```

La API está versionada bajo:

```text
/v1
```

### Autenticación

Los endpoints requieren una API Key mediante el encabezado:

```text
X-API-Key
```

Desde Swagger puede configurarse utilizando el botón **Authorize** e ingresando el mismo valor definido en `ARRIENDOS_API_KEY`.

### Clientes

La API permite:

```text
GET  /v1/clientes
POST /v1/clientes
GET  /v1/clientes/{id}
```

### Arriendos

La API permite:

```text
GET  /v1/arriendos
POST /v1/arriendos
GET  /v1/arriendos/{id}
POST /v1/arriendos/{id}/devolucion
```

Al registrar un arriendo, el servicio consulta mediante gRPC a Equipos para reservar las unidades solicitadas.

Al realizar una devolución, Arriendos solicita a Equipos liberar nuevamente las unidades correspondientes.

---

## Servicio gRPC de Equipos

Equipos expone internamente el servicio definido mediante Protocol Buffers.

Las operaciones principales son:

```text
GetEquipo
ListCatalog
SetReserva
```

`SetReserva` permite realizar las operaciones:

```text
RESERVE
RELEASE
```

La comunicación se realiza dentro de la red de Docker mediante:

```text
equipos-service:50051
```

El servicio no necesita ser consumido directamente por los clientes externos de ArriendaPro.

---

## Contratos

El proyecto utiliza contratos explícitos para ambas interfaces.

### REST

El contrato de la API REST está definido en:

```text
contracts/openapi.yaml
```

### gRPC

El contrato del servicio de Equipos está definido en:

```text
equipos-service/equipo.proto
```

A partir del archivo `.proto` se generan las clases necesarias para la comunicación gRPC.

---

## Manejo de fallas

Las llamadas desde Arriendos hacia Equipos utilizan un timeout para evitar esperas indefinidas.

Si Equipos no se encuentra disponible y una operación necesita comunicarse con él, Arriendos responde con:

```text
503 Service Unavailable
```

De esta manera no se registra un arriendo cuando no es posible confirmar la disponibilidad del equipo.

---

## Persistencia

Cada servicio posee su propia instancia lógica de MongoDB:

```text
Arriendos → mongo_arriendos
Equipos   → mongo-equipos
```

Los datos se almacenan mediante volúmenes de Docker, por lo que permanecen disponibles después de ejecutar:

```bash
docker compose down
```

Para eliminar también los volúmenes y sus datos:

```bash
docker compose down -v
```

> Este último comando elimina los datos almacenados por ambos servicios.

---

## Detener el sistema

Para detener todos los contenedores:

```bash
docker compose down
```

Para volver a construir y ejecutar el proyecto después de realizar cambios:

```bash
docker compose up --build
```

---

## ADR

Las principales decisiones arquitectónicas del proyecto están documentadas en:

```text
docs/adr/
```

Se incluyen los siguientes ADR:

1. **ADR-001:** Separación de Arriendos y Equipos en dos servicios.
2. **ADR-002:** REST para la interfaz pública y gRPC para la comunicación interna.
3. **ADR-003:** Evolución y versionado de los contratos.
4. **ADR-004:** Manejo de indisponibilidad del servicio de Equipos.

---

## Uso de asistentes de IA

Durante el desarrollo del proyecto se utilizaron asistentes de inteligencia artificial como herramienta de apoyo.

Su uso estuvo orientado principalmente a:

- Consultas sobre conceptos de REST, gRPC, Protocol Buffers y Docker.
- Apoyo en la revisión y depuración de errores de integración.

Las propuestas generadas mediante estas herramientas fueron revisadas, adaptadas y verificadas por los integrantes antes de incorporarlas al proyecto. Los integrantes son responsables del código y de las decisiones arquitectónicas utilizadas en la solución.

---

## Autores

**Grupo 20 — Empresa de Arriendo de Maquinaria ArriendaPro**

- Gustavo González Anabalón
- Joaquín Sandoval Reyes

Universidad de Concepción  
Facultad de Ingeniería  
Integración de Sistemas — 2026