# ADR-002 · REST frente a gRPC: por qué cada uno donde está

**Estado:**  Aceptada

## Contexto
Los microservicios de ArriendaPro necesitan comunicarse entre sí de forma rápida, eficiente.
Mediante Arriendos, el cliente se comunica con el sistema, mientras que Arriendos es el que se comunica frecuentemente
con Equipos, para consultar disponibilidad.

## Alternativas consideradas

- **Opción A - REST para toda la comunicación:** utiliza HTTP/JSON tanto hacia consumidores externos como entre
servicios. Es sencillo de inspeccionar, ampliamente interoperable y fácil de probar, pero utiliza mensajes JSON más
verbosos y carece del contrato binario fuertemente tipado de Protocol Buffers.
- **Opción B - gRPC para otda la comunicación:** mantener Equipos como un servicio independiente y agrupar clientes
y contratos en Arriendos. Aumenta la complejidad de comunicación y despliegue, pero mantiene separadas las 
responsabilidades y los datos de cada dominio.
- **Opción C — REST público y gRPC interno:** utiliza REST/JSON para la interfaz pública de Arriendos y 
gRPC/Protocol Buffers para la comunicación frecuente entre Arriendos y Equipos.

## Decisión
Utilizar REST para la API de Arriendos y gRPC impulsado por Protocol Buffers (Protobuf) como protocolo principal de
comunicación interna entre microservicios.

## Justificación
REST proporciona una interfaz facil de consumir y depurar.
Para la comunicación interna, gRPC proporciona una alta velocidad de transferencia, serialización binaria ultracompacta
y tipado estricto mediante archivos .proto

En el experimento realizado para este proyecto, los tres mensajes evaluados resultaron más pequeños utilizando
Protocol Buffers que sus equivalentes JSON: 56 frente a 22 bytes, 77 frente a 27 bytes y 93 frente a 32 bytes. Esto
representó reducciones aproximadas de 60,7 %, 64,9 % y 65,5 % respectivamente para los casos medidos.

## Costo aceptado
Formato binario de gRPC no legible de forma nativa (dificulta la depuración visual sin herramientas especiales) y
curva de aprendizaje inicial para la compilación de contratos.

## Consecuencias
Los consumidores sólo pueden conocer la API REST de Arriendos y no el servicio interno de Equipos.

Los cambios de la interfaz pública deberá reflejarse en "openapi.yaml", mientras que los cambios de comunicación con
Equipos deben mantenerse compatibles con "equipo.proto".