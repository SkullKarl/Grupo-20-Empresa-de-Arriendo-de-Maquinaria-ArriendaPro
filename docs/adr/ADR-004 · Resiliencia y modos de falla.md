# ADR-003 · Resiliencia y modos de falla

**Estado:**  Aceptada

## Contexto
 El microservicio de equipos se comunica mediante gRPC y persiste datos en MongoDB, todo ello ejecutándose dentro de
 contenedores Docker aislados. Para esta implementación, se requiere un manejo de errores claro y directo,
 aprovechando los mecanismos nativos del framework gRPC y del motor de contenedores sin recurrir a patrones complejos.

## Alternativas consideradas
- **Opción A — Esperar sin timeout:** permite esperar respuestas lentas, pero puede mantener bloqueadas las
solicitudes de Arriendos indefinidamente cuando Equipos presenta problemas.
- **Opción B — Continuar el arriendo aunque Equipos no responda:** mantiene disponible la operación REST, pero puede
registrar contratos sin confirmar disponibilidad, reproduciendo el problema de inconsistencia que la integración 
busca solucionar.
- **Opción C — Aplicar timeout y rechazar temporalmente la operación:** limita el tiempo de espera y evita registrar
operaciones cuya disponibilidad no pudo confirmarse, a costa de rechazar solicitudes mientras Equipos está indisponible.

## Decisión
Manejo de errores mediante Códigos gRPC Estándar, utilizar las excepciones nativas de la librería de Python y PyMongo
para capturar fallos en la base de datos o lógica de negocio, devolviendo códigos de estado estándar y aprovechando los
contenedores, delegar la recuperación ante fallos del proceso del servidor o de la base de datos al entorno de
ejecución de Docker Compose, asegurando que los servicios mantengan su aislamiento y puedan reiniciarse limpiamente
en el entorno local.


## Justificación
La disponibilidad de Equipos es necesaria para confirmar una reserva o liberación. Si Arriendos continuara sin esa
confirmación, podría generar contratos inconsistentes con el inventario.

El cliente gRPC establece un timeout de 3 segundos, los errores de comunicación gRPC se capturan por Arriendos y se
transforman en una respuesta HTTP 503. Este timeout además evita que una llamada lenta mantenga ocupado el servicio
de REST.

## Costo aceptado
Mientras Equipos esté caído o supere el timeout, no será posible registrar ni devolver arriendos que requieran modificar
su disponibilidad.

La implementación actual tampoco incorpora mecanismos más avanzados como
reintentos con backoff, circuit breaker o caché de disponibilidad.

## Consecuencias
La falla de Equipos queda aislada y se comunica explícitamente al consumidor mediante HTTP 503.

Las operaciones de Arriendos que no necesitan modificar Equipos pueden seguir funcionando mientras sus propias dependencias estén disponibles.

