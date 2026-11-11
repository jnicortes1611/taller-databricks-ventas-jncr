# Validación local

Ejecutar desde la raíz del repositorio:

```sh
python scripts/validar.py
```

Solo requiere Python 3.9 o posterior y su biblioteca estándar. Se comprueban los cuatro notebooks: JSON v4, celdas sin salidas persistidas, sintaxis Python y equivalencia del código con Databricks Source. Se extraen los datos originales mediante AST y se verifican 18 filas, 17 únicas y 15 válidas.

El SQL conserva su DDL de Lakeflow en `pipeline/pipeline_ventas.sql`. Para la comprobación local se adaptan únicamente las cabeceras de las dos vistas materializadas a vistas SQLite; se prueban sus SELECT, reglas y agregaciones sobre los datos del ejemplo. Los totales son 539.000 inicialmente y 589.000 después; la inserción protegida repetida mantiene una única venta 999 y 16 ventas limpias.

También se comprueba la existencia de los enlaces locales de Markdown. No se validan disponibilidad de enlaces externos, permisos de catálogo, ejecución Spark/Delta, sintaxis DDL mediante el motor Databricks, planificación del job ni estrategia incremental. Las capturas aportadas documentan la ejecución previa real del autor.

La revisión visual de privacidad excluyó la captura de dependencias por correo personal. Las otras 14 capturas se publican sin modificaciones.

## Captura final no publicada

`E4_04_resumen_despues.png` fue revisada visualmente y confirma Tecnologia 398.000, diferencia 50.000 y 16 ventas limpias. La publicación automática bloqueó su subida al no poder verificar el archivo enviado. No está incluida en GitHub; queda pendiente de carga manual por el propietario.
