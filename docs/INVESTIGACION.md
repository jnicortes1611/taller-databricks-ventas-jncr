# Taller de Ingeniería de Datos: investigación

Fecha de consulta de todas las fuentes: **6 de noviembre de 2026**.

Estas respuestas están redactadas como apoyo para comprender y desarrollar el taller. Las evidencias de ejecución deben añadirse después de trabajar en la cuenta real de Databricks.

## 1. Almacenar y consultar datos en el catálogo

### ¿Qué es Unity Catalog en Databricks?

Unity Catalog es el sistema con el que Databricks organiza y gobierna los datos y otros recursos. Permite encontrar tablas, controlar quién puede utilizarlas y conocer su origen y sus relaciones. Una tabla se identifica mediante tres niveles: `catalogo.esquema.tabla`. En este taller, el esquema reúne las tablas de ventas y permite consultarlas desde distintos notebooks sin depender de una variable creada en una sesión anterior. [1]

### ¿Qué diferencia hay entre un DataFrame de Spark y una tabla Delta?

Un DataFrame es una representación de datos con filas y columnas que se utiliza para seleccionar, filtrar, transformar o agrupar información mediante Spark. Definirlo no equivale a guardar una tabla persistente. [2]

Una tabla Delta conserva los datos en almacenamiento con el formato Delta Lake, que incorpora un registro de transacciones para mantener operaciones consistentes y permitir versiones de los datos. Si se registra en el catálogo, puede recuperarse por su nombre completo desde otro notebook. En el taller, el DataFrame sirve para construir las ventas; la tabla Delta `ventas_bronze` sirve para conservarlas y compartir su lectura. [3]

| Aspecto | DataFrame de Spark | Tabla Delta registrada |
|---|---|---|
| Uso en el taller | Construir y transformar datos | Conservar resultados consultables |
| Referencia habitual | Variable, por ejemplo `ventas` | Nombre `catalogo.esquema.tabla` |
| Persistencia | No guarda por sí solo una tabla permanente | Datos guardados y metadatos registrados |
| Relación entre ambos | Puede leer una tabla o escribirse como tabla | Puede consultarse como DataFrame |

## 2. Transformar datos y aplicar reglas de calidad

El enunciado no incluye preguntas de investigación en este ejercicio. La implementación debe eliminar filas idénticas, excluir producto ausente y cantidades o precios no positivos, calcular `total_venta` y generar el resumen por categoría. Repetir la transformación debe conservar el mismo resultado mientras la entrada no cambie.

## 3. Automatizar el proceso mediante un job

### ¿Qué es un job en Databricks y para qué sirve?

Un job es un recurso que coordina la ejecución de una o varias actividades. Permite repetir un proceso, iniciarlo manualmente o programarlo, y consultar cómo terminó cada ejecución. Aquí automatiza la carga y la transformación de ventas para evitar abrir ambos notebooks cada vez. [4]

### ¿Qué es una tarea y cómo se diferencia de un job?

Una tarea es una unidad de trabajo dentro del job; por ejemplo, ejecutar un notebook. El job contiene la organización general y las tareas realizan los pasos concretos. En este caso hay un job con dos tareas: cargar ventas y transformarlas. [4]

### ¿Qué significa establecer dependencias entre tareas?

Significa indicar qué tarea debe terminar y con qué resultado antes de iniciar otra. Para este taller, transformación depende de carga con la condición `All succeeded`. Si carga falla, transformación no debe ejecutarse; la documentación indica el estado `Upstream failed` cuando esa condición no se cumple. Esto evita procesar una carga que no terminó correctamente. [5]

### ¿Qué información del historial de ejecuciones permite identificar un fallo?

Se revisan el estado general de la ejecución, la tarea fallida, su hora de inicio y duración, y especialmente su salida, código o mensaje de error y registros disponibles. El detalle permite relacionar el error con el código ejecutado. Una referencia a una columna inexistente debe investigarse abriendo la salida de carga y comprobando el nombre mencionado en el error. La duración ayuda a ubicar el problema, pero por sí sola no explica la causa. [6]

## 4. Construir un pipeline declarativo

### ¿Qué es un pipeline de datos y cuáles son sus etapas habituales?

Un pipeline es un proceso que lleva datos desde una fuente hasta resultados utilizables. En este caso, las etapas son entrada de ventas, limpieza y validación, cálculo del valor de cada venta, resumen por categoría y publicación. Esta organización es una aplicación del taller: las etapas concretas dependen del problema. Lakeflow admite procesos por lotes y en streaming, con conjuntos de datos y transformaciones conectados. [7]

### ¿Qué significa que un pipeline sea declarativo?

Significa describir los resultados que se necesitan y las consultas que los producen. El motor identifica las dependencias y organiza el procesamiento. Aquí se declara una vista materializada de ventas limpias y otra que suma esas ventas por categoría; la referencia de la segunda a la primera establece su relación. Una vista materializada conserva el resultado calculado y lo actualiza cuando se refresca. [7, 8]

### ¿En qué se diferencian un job que ejecuta notebooks y un pipeline declarativo que define conjuntos de datos?

| Aspecto | Job con notebooks | Pipeline declarativo |
|---|---|---|
| Qué se define | Tareas que ejecutan código | Conjuntos de datos y consultas |
| Dependencias del taller | Se configura carga antes de transformación | Se deducen de las referencias entre resultados |
| Resultado observado | Ejecuciones y estados de tareas | Datos publicados y grafo del proceso |
| Uso aquí | Ejecutar los notebooks 01 y 02 | Mantener las dos vistas materializadas |

Ambos pueden integrarse: un job también puede tener una tarea que ejecute un pipeline. Al refrescar vistas materializadas, el motor puede procesar cambios incrementalmente cuando es posible o volver a calcular resultados. Por tanto, observar el aumento correcto de ventas demuestra actualización del resultado, pero no demuestra por sí solo que la ejecución haya sido incremental. [4, 7]

## Notas para Databricks Free Edition

Free Edition utiliza únicamente cómputo serverless y está sujeta a cuotas. La documentación consultada permite hasta cinco tareas de job concurrentes y un pipeline activo por tipo; el taller solo requiere dos tareas secuenciales y un pipeline ETL. Si se agota la cuota, debe esperarse a su restablecimiento. [9]

La documentación actual sitúa los jobs en `Jobs & Pipelines > Create > Job`. Los pipelines ETL pueden crearse desde `New > ETL pipeline`; se debe comprobar el catálogo y esquema de destino, mantener serverless y ejecutar de forma manual. Los nombres de controles pueden variar según la actualización del workspace. [10, 11]

## Fuentes oficiales

1. Databricks. *What is Unity Catalog?* https://docs.databricks.com/aws/en/data-governance/unity-catalog
2. Databricks. *Tutorial: Load and transform data using Apache Spark DataFrames*. https://docs.databricks.com/aws/en/getting-started/dataframes
3. Databricks. *What is Delta Lake?* https://docs.databricks.com/aws/en/delta/
4. Databricks. *Lakeflow Jobs*. https://docs.databricks.com/aws/en/jobs/
5. Databricks. *Configure task dependencies*. https://docs.databricks.com/aws/en/jobs/run-if
6. Databricks. *Monitor Lakeflow Jobs*. https://docs.databricks.com/aws/en/jobs/monitor
7. Databricks. *Pipeline concepts*. https://docs.databricks.com/aws/en/ldp/concepts
8. Databricks. *Materialized views*. https://docs.databricks.com/aws/en/ldp/materialized-views
9. Databricks. *Databricks Free Edition limitations*. https://docs.databricks.com/aws/en/getting-started/free-edition-limitations
10. Databricks. *Create your first workflow with Lakeflow Jobs*. https://docs.databricks.com/aws/en/jobs/jobs-quickstart
11. Databricks. *Configure pipelines*. https://docs.databricks.com/aws/en/ldp/configure-pipeline

Todas las fuentes fueron consultadas el 6 de noviembre de 2026. Son documentación de Databricks para AWS; la interfaz efectiva de la cuenta es la referencia al realizar las capturas.
