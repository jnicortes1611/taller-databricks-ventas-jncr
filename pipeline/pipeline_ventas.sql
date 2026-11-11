-- Fuente de un pipeline ETL Lakeflow Spark Declarative Pipelines.
-- Agregar este archivo al pipeline; NO ejecutarlo como notebook independiente.
-- En "Default location for data assets" seleccionar exactamente el catálogo y
-- esquema que contienen ventas_bronze. Los nombres siguientes se resuelven allí.
-- No usar LIVE: los pipelines nuevos resuelven el catálogo/esquema configurado.

CREATE OR REFRESH MATERIALIZED VIEW pipeline_ventas_limpias
COMMENT 'Ventas sin duplicados idénticos, con producto y valores positivos'
AS
WITH sin_duplicados AS (
  SELECT DISTINCT
    id_venta, fecha, producto, categoria, cantidad, precio_unitario
  FROM ventas_bronze
), validas AS (
  SELECT id_venta, fecha, producto, categoria, cantidad, precio_unitario
  FROM sin_duplicados
  WHERE producto IS NOT NULL
    AND LENGTH(TRIM(producto)) > 0
    AND cantidad > 0
    AND precio_unitario > 0
)
SELECT
  id_venta, fecha, producto, categoria, cantidad, precio_unitario,
  CAST(cantidad * precio_unitario AS DECIMAL(20,2)) AS total_venta
FROM validas;

CREATE OR REFRESH MATERIALIZED VIEW pipeline_ventas_por_categoria
COMMENT 'Valor total vendido por categoría, derivado de las ventas limpias'
AS
SELECT
  categoria,
  SUM(total_venta) AS total_vendido
FROM pipeline_ventas_limpias
GROUP BY categoria;
