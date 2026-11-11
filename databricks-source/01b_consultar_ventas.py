# Databricks notebook source
# MAGIC %md
# MAGIC Configura el catálogo si tu workspace lo requiere. Vacío usa el catálogo actual.
# COMMAND ----------
import re
from pyspark.sql import functions as F

dbutils.widgets.text("catalogo", "")
dbutils.widgets.text("esquema", "ingenieria_datos_juan_nicolas")
catalogo = dbutils.widgets.get("catalogo").strip() or spark.sql("SELECT current_catalog()").first()[0]
esquema = dbutils.widgets.get("esquema").strip()
for etiqueta, identificador in [("catálogo", catalogo), ("esquema", esquema)]:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", identificador):
        raise ValueError(f"El {etiqueta} debe contener letras, números o guion bajo y no comenzar por número: {identificador!r}")
def tabla(nombre):
    return f"`{catalogo}`.`{esquema}`.`{nombre}`"
print(f"Catálogo: {catalogo}; esquema: {esquema}")
# COMMAND ----------
# Este notebook es independiente: lee la tabla usando catálogo.esquema.tabla.
ventas = spark.table(tabla("ventas_bronze"))
print("Nombre completo:", tabla("ventas_bronze"))
print("Cantidad de registros:", ventas.count())
ventas.printSchema()
display(ventas.filter(F.col("categoria") == "Tecnologia").orderBy("id_venta"))
