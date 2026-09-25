# ArriendaPro — Servicio de Arriendos

Servicio REST desarrollado con **FastAPI** para gestionar clientes y contratos de arriendo. Utiliza **MongoDB** para almacenar los datos y un cliente **gRPC** para comunicarse con el servicio de Equipos.

## Requisitos

* Docker y Docker Compose.
* El archivo `contracts/equipo.proto`, utilizado para generar el cliente gRPC durante la construcción.

No es necesario instalar Python ni MongoDB localmente.

## 1. Configurar variables de entorno

En la raíz del repositorio, crear un archivo `.env`:

```dotenv
ARRIENDOS_API_KEY=clave-local-de-prueba
```

La clave puede cambiarse, pero debe coincidir con la utilizada al realizar las solicitudes HTTP. **No subir `.env` a GitHub.**

## 2. Levantar Arriendos

Abrir una terminal en la raíz del repositorio y ejecutar:

```powershell
docker compose up -d --build arriendos
```

Este comando construye la imagen de Arriendos y levanta MongoDB como dependencia.

Para comprobar el estado de los contenedores:

```powershell
docker compose ps
```

## 3. Acceder a la API

Con los contenedores funcionando, abrir:

**http://localhost:8080/docs**

Swagger permite consultar y probar los endpoints de clientes y arriendos.

Para realizar solicitudes protegidas, pulsar **Authorize** e ingresar la API Key configurada en `.env`. La API utiliza el encabezado `X-API-Key`.

## 4. Integración con Equipos

Arriendos se comunica con Equipos mediante gRPC. La dirección se configura en `docker-compose.yml` mediante:

```yaml
EQUIPOS_GRPC_ADDRESS: equipos:50051
```

El nombre del servicio y el puerto deben coincidir con la configuración del servidor gRPC de Equipos.

Mientras Equipos no esté disponible, las operaciones de clientes y las consultas de arriendos pueden funcionar, pero el registro y la devolución de arriendos no podrán completar su comunicación gRPC.

## 5. Comandos útiles

Ver los logs de Arriendos:

```powershell
docker compose logs --tail=50 arriendos
```

Detener los contenedores:

```powershell
docker compose down
```

Volver a levantarlos:

```powershell
docker compose up -d --build arriendos
```

MongoDB utiliza un volumen de Docker, por lo que los datos persisten al detener y volver a iniciar los contenedores. **No utilizar `docker compose down -v` si se desea conservar la información almacenada.**

## Estado del proyecto

El servicio de Arriendos implementa las siete operaciones definidas en `contracts/openapi.yaml`. La validación completa del registro y devolución de arriendos requiere ejecutar e integrar el servicio gRPC de Equipos.
