# ADR-001 · Estilo de integración y descomposición

**Estado:**  Aceptada

## Contexto
El sistema ArriendaPro requiere manejar múltiples dominios de negocio (gestión de equipos, clientes, etc) con la
posibilidad de escalar servicios específicos según la necesidad y permitir el despliegue independiente de estos mismos.

Arriendos necesita consultar y modificar disponibilidad mantenida por el servicio de Equipos, pero ambos dominios
tienen responsabilidades y datos propios.

## Alternativas consideradas

- **Opción A - Monolito:** integrar equipos, clientes y arriendos en una sola aplicación y base de datos. Simplifica el
despliegue y la comunicación, pero aumenta el acoplamiento entre dominios y elimina la autonomía de Equipos.
- **Opción B - Dos servicios, Equipos y Arriendos:** mantener Equipos como un servicio independiente y agrupar clientes
y contratos en Arriendos. Aumenta la complejidad de comunicación y despliegue, pero mantiene separadas las 
responsabilidades y los datos de cada dominio.

## Decisión
Mantener dos servicios independientes, Equipos y Arriendos. Se adopta una arquitectura basada en microservicios.

## Justificación
Así ganamos mayor escalabilidad horizontal, aislamiento de fallos (si un microservicio falla, los demás
siguen operando) y autonomía por servicio.

## Costo aceptado
La separación obliga a mantener una comunicación de red entre los dos servicios. Una operación de arriendo deja de
ser local, por lo que si el servicio de Equipos se cae, no será posible realizar operaciones que involucren al servicio
de Equipos.

## Consecuencias
Los dos servicios por separado pueden escalar y manejar sus datos de manera independiente. Arriendos debe manejar
los errores de comunicación con Equipos.
