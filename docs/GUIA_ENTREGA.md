# Guía de ejecución y evidencias

Este documento indica qué ejecutar y qué capturar. **No certifica que el taller ya se haya ejecutado en Databricks.** Los resultados y duraciones del informe deben corresponder a tu cuenta.

## Preparación única

1. Entra a Databricks Free Edition. No uses la antigua Community Edition.
2. Abre `Catalog` e identifica un catálogo disponible con permiso de escritura. No supongas que se llama `main`.
3. Utiliza el mismo catálogo y esquema en todos los notebooks, tareas y código del pipeline. El esquema debe seguir `ingenieria_datos_tunombre`.
4. Importa los notebooks del paquete como notebooks de Python y conserva los nombres exigidos `01_cargar_ventas` y `02_transformar_ventas`.
5. Selecciona cómputo `Serverless`. Revisa las variables o parámetros de configuración antes de ejecutar.
6. Guarda las capturas en orden. Cada imagen debe mostrar el nombre del objeto o consulta y la información relevante con texto legible.

## Ejercicio 1: catálogo, carga y lectura

1. Ejecuta `01_cargar_ventas` con la opción de fallo controlado desactivada, si está incluida.
2. Abre `Catalog > tu catálogo > tu esquema > ventas_bronze`. Captura la identificación de la tabla y sus columnas con tipos. Si no caben, usa dos imágenes.
3. Desde otro notebook ejecuta la lectura por nombre completo y muestra el conteo y las ventas de una categoría.
4. Captura el código de lectura con su resultado. Debe verse que procede de la tabla guardada, no de una variable de la sesión del notebook 01.

**Archivos sugeridos:** `E1_01_catalogo.png`, `E1_02_conteo.png`, `E1_03_categoria.png`.

## Ejercicio 2: limpieza y repetición

1. Ejecuta `02_transformar_ventas` después de la carga.
2. Registra el conteo inicial, el conteo sin duplicados y el conteo final de ventas válidas, según las salidas disponibles.
3. Muestra `ventas_silver` con `total_venta` y el resumen `ventas_por_categoria`.
4. Ejecuta otra vez el notebook completo, sin alterar la entrada.
5. Comprueba que los conteos, las filas y los valores agregados coinciden con los de la primera ejecución. Guardar solo el mismo conteo no prueba por sí solo que todos los valores sean iguales.
6. Captura las comprobaciones y el resumen.

**Archivos sugeridos:** `E2_01_limpieza.png`, `E2_02_resumen.png`, `E2_03_repeticion.png`.

## Ejercicio 3: job, fallo y corrección

La ruta verificada en la documentación es `Jobs & Pipelines > Create > Job`.

1. Crea `job_ventas_tunombre`.
2. Añade una tarea `Notebook` llamada `cargar_ventas`, con origen `Workspace` y ruta a `01_cargar_ventas`. Comprueba serverless y guarda.
3. Añade otra tarea `Notebook` llamada `transformar_ventas`, con ruta a `02_transformar_ventas`.
4. En la segunda tarea, configura `Depends on: cargar_ventas` y `Run if dependencies: All succeeded`. Guarda y captura el grafo y la condición.
5. Inicia una ejecución manual con `Run now`. Desde `Runs`, abre la ejecución y registra el estado y duración de cada tarea.
6. Introduce el fallo controlado en carga según el mecanismo del notebook: activa su parámetro de prueba o incorpora temporalmente una consulta de columna inexistente. Usa un error determinista que permanezca durante toda la ejecución.
7. Ejecuta el job de nuevo. Captura el estado fallido, la salida con la causa y el estado real de transformación. Con `All succeeded`, se espera que no corra por el fallo previo; documenta la etiqueta exacta mostrada.
8. Corrige o desactiva el error y lanza una nueva ejecución completa. Captura ambas tareas exitosas, su duración y el identificador de ejecución si es visible.

**Archivos sugeridos:** `E3_01_dependencias.png`, `E3_02_fallo.png`, `E3_03_causa.png`, `E3_04_exito.png`.

**Texto para completar tras ejecutar:** “La tarea de carga falló porque ____. El mensaje observado fue ____. La tarea de transformación quedó en estado ____ porque dependía de que carga terminara correctamente. Después de ____, ambas tareas finalizaron con estado ____.”

## Ejercicio 4: pipeline y venta adicional

Completa el ejercicio 3 antes de esta prueba. Durante la comparación **no vuelvas a ejecutar la carga ni el job**, pues la carga puede reemplazar bronze y borrar la venta agregada.

1. Abre `New > ETL pipeline`. También puede aparecer desde `Jobs & Pipelines`.
2. Configura un pipeline con el código SQL o Python preparado, cómputo serverless, catálogo y esquema correctos. Usa ejecución manual o modo `Triggered` cuando se ofrezca.
3. Comprueba que las definiciones se llaman `pipeline_ventas_limpias` y `pipeline_ventas_por_categoria`, y que la fuente es tu tabla `ventas_bronze`.
4. Ejecuta el pipeline y espera su finalización. Captura el grafo de dependencias y consulta el resumen publicado. Guarda el resumen inicial antes de insertar datos.
5. Inserta una única venta válida usando el notebook de prueba correspondiente. Revisa su identificador antes de repetir una celda: una repetición puede alterar la comparación si la inserción no está protegida.
6. Ejecuta nuevamente el pipeline, sin ejecutar la carga ni el job.
7. Consulta otra vez el resumen. La categoría de la nueva venta debe aumentar exactamente en `cantidad × precio_unitario`; las demás categorías deben conservar su total.
8. Captura la venta insertada, el resultado antes/después y la verificación de la diferencia. La actualización del resumen no demuestra por sí sola que el motor haya usado procesamiento incremental.

**Archivos sugeridos:** `E4_01_grafo.png`, `E4_02_antes.png`, `E4_03_venta.png`, `E4_04_despues.png`.

## Revisión final

| Requisito | Evidencia pendiente de verificar |
|---|---|
| Investigación | Todas las preguntas respondidas y fuentes incluidas |
| Datos | Al menos 15 registros y errores intencionales identificables |
| Catálogo | Esquema, bronze y tipos visibles |
| Lectura independiente | Nombre completo, conteo y filtro |
| Limpieza | Conteos, reglas, total y resumen |
| Repetición | Mismos resultados tras repetir transformación |
| Job | Dos tareas, dependencia, fallo explicado y éxito final |
| Pipeline | Dos vistas materializadas, grafo y destino correcto |
| Venta adicional | Resumen anterior, inserción y diferencia comprobada |

No sustituyas capturas reales por resultados calculados localmente. Los resultados esperados sirven para comprobar la ejecución; las duraciones y estados deben copiarse de Databricks.

## Referencias operativas

Consultadas el 6 de noviembre de 2026:

- Jobs e interfaz: https://docs.databricks.com/aws/en/jobs/jobs-quickstart
- Dependencias: https://docs.databricks.com/aws/en/jobs/run-if
- Historial y detalles: https://docs.databricks.com/aws/en/jobs/monitor
- Configuración de pipelines: https://docs.databricks.com/aws/en/ldp/configure-pipeline
- Cómputo serverless para pipelines: https://docs.databricks.com/aws/en/ldp/serverless
- Límites Free Edition: https://docs.databricks.com/aws/en/getting-started/free-edition-limitations
