# Evidencias reales de Databricks

Capturas suministradas por el autor y revisadas visualmente antes de publicarse. Se conservan sin modificar; solo se normalizaron nombres y extensiones.

| Captura | Sección |
|---|---|
| [E1_01_carga_18_registros.png](E1_01_carga_18_registros.png) | Ejercicio 1 |
| [E1_02_catalogo_columnas.png](E1_02_catalogo_columnas.png) | Ejercicio 1 |
| [E1_03_consultas.png](E1_03_consultas.png) | Ejercicio 1 |
| [E2_01_limpieza.jpeg](E2_01_limpieza.jpeg) | Ejercicio 2 |
| [E2_02_resumen.jpeg](E2_02_resumen.jpeg) | Ejercicio 2 |
| [E2_03_repeticion.png](E2_03_repeticion.png) | Ejercicio 2 |
| [E2_03_repeticion2.png](E2_03_repeticion2.png) | Ejercicio 2 |
| [E3_02_primera_ejecucion_exitosa.jpeg](E3_02_primera_ejecucion_exitosa.jpeg) | Ejercicio 3 |
| [E3_03_ejecucion_fallida.png](E3_03_ejecucion_fallida.png) | Ejercicio 3 |
| [E3_04_causa_del_error.png](E3_04_causa_del_error.png) | Ejercicio 3 |
| [E3_05_ejecucion_final_exitosa.png](E3_05_ejecucion_final_exitosa.png) | Ejercicio 3 |
| [E4_01_grafo_pipeline.png](E4_01_grafo_pipeline.png) | Ejercicio 4 |
| [E4_02_resumen_antes.png](E4_02_resumen_antes.png) | Ejercicio 4 |
| [E4_03_venta_agregada.jpeg](E4_03_venta_agregada.jpeg) | Ejercicio 4 |

## Privacidad y alcance

Se excluyó `E3_01_dependencias.png..jpeg` porque muestra un correo personal en las rutas de los notebooks. No se publica el ZIP original. En las otras 14 capturas no se observaron contraseñas, tokens, códigos de verificación ni datos de clientes reales. Los datos de ventas son el conjunto didáctico incluido en el código.

La dependencia configurada es `cargar_ventas` → `transformar_ventas`, con `All succeeded`; la captura específica queda pendiente de una versión sin correo. Las capturas de ejecuciones muestran ambas tareas, el fallo y la recuperación, pero no permiten leer la etiqueta exacta del estado de la tarea omitida ni sus duraciones individuales. El job completo registra 1 min 5 s inicialmente, 19 s en el fallo y 44 s en la recuperación.

El grafo del pipeline muestra `Full recompute`: estas evidencias prueban la actualización del resultado, no procesamiento incremental.

## Captura final no publicada

`E4_04_resumen_despues.png` fue revisada visualmente y confirma Tecnologia 398.000, diferencia 50.000 y 16 ventas limpias. La publicación automática bloqueó su subida al no poder verificar el archivo enviado. No está incluida en GitHub; queda pendiente de carga manual por el propietario.
