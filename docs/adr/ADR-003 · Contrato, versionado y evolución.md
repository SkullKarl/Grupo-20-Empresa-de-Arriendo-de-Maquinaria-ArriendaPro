# ADR-003 · Contrato, versionado y evolución

**Estado:**  Aceptada

## Contexto
Los contratos definidos en los archivos actúan como la única fuente de verdad para la comunicación.
A medida que el negocio evolucione, los contratos inevitablemente deberán cambiar sin romper los sistemas existentes.

## Alternativas consideradas

- **Opción A — Modificar los contratos sin estrategia de compatibilidad:** es simple inicialmente, pero puede romper 
clientes existentes sin advertencia
- **Opción B — Mantener compatibilidad hacia atrás y versionar solo cambios incompatibles:** permite extender los 
contratos existentes mientras los cambios sean compatibles y crear una nueva versión cuando cambie su semántica o
estructura de forma incompatible.

## Decisión
Se establece una estrategia de evolución basada en las reglas de compatibilidad hacia atrás de Protocol Buffers,
reservando el versionado explícito de paquetes (v1, v2) exclusivamente para cambios estructurales mayores.
Se añade el nuevo campo al archivo .proto asignándole un nuevo número de etiqueta (tag) único (por ejemplo,
string nuevo_campo = 6;). Nunca se reutilizan números de etiquetas anteriores.

## Justificación
En Protocol Buffers, los campos nuevos se incorporarán utilizando números de campo nuevos y únicos. Los números
correspondientes a campos retirados no deberán reutilizarse.

En REST se mantendrán los endpoints actuales bajo '/v1' mientras los cambios sean compatibles, de lo contrario se
requerirá una nueva versión, por ejemplo '/v2'.

Cambios compatibles serían: añadir nuevos campos, eliminar campos antiguos, o agregar nuevos servicios/métodos.
Los consumidores antiguos simplemente ignorarán los campos nuevos que no reconozcan.

Cambios incompatibles serían: cambiar el tipo de dato de un campo existente (de int32 a string, por ejemplo),
renombrar drásticamente la semántica de un mensaje de forma que altere la lógica del cliente, o eliminar un
método completo. Ante esto, se crea un nueva versión del paquete en el contrato.


## Costo aceptado
Se exige rigurosidad al modificar tanto OpenApi como Protocol Buffers, ya que los sistemas deben manteneres compatibles
para su correcta función.

## Consecuencias
Los campos y operaciones nuevas deberán diseñarse considerando clientes anteriores.
La compatibilidad deberá revisarse cada vez que se modifique "opeanapi.yaml" o "equipo.proto"
En Protocol Buffers no deberán reutilizarse los números de campos retirados. Los cambios incompatibles deberán
introducir una versión nueva y comunicarse a los consumidores antes de retirar la versión anterior