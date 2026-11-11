"""Validación local sin Spark; no reemplaza una ejecución en Databricks."""
import ast
import json
import re
import sqlite3
from datetime import date
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def source_cells(text):
    text = text.removeprefix('# Databricks notebook source\n')
    return [part.strip() for part in text.split('# COMMAND ----------')
            if part.strip() and not part.strip().startswith('# MAGIC %md')]


def main():
    for path in sorted((ROOT / 'notebooks').glob('*.ipynb')):
        notebook = json.loads(path.read_text(encoding='utf-8'))
        assert notebook['nbformat'] == 4
        cells = notebook['cells']
        codes = []
        for cell in cells:
            assert cell['cell_type'] in ('code', 'markdown')
            source = ''.join(cell['source'])
            if cell['cell_type'] == 'code':
                ast.parse(source, filename=path.name)
                assert cell['execution_count'] is None and cell['outputs'] == []
                codes.append(source.strip())
        py = (ROOT / 'databricks-source' / (path.stem + '.py')).read_text(encoding='utf-8')
        ast.parse(py)
        assert codes == source_cells(py), f'Versiones distintas: {path.name}'
        print(f'OK sintaxis, estructura y equivalencia: {path.name}')

    source = (ROOT / 'databricks-source/01_cargar_ventas.py').read_text(encoding='utf-8')
    tree = ast.parse(source)
    assignments = [n for n in tree.body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id in ('filas_validas', 'filas') for t in n.targets)]
    scope = {'date': date, 'Decimal': Decimal}
    for node in assignments:
        exec(compile(ast.Module(body=[node], type_ignores=[]), '<datos>', 'exec'), scope)
    rows = scope['filas']
    unique = set(rows)
    clean = {r for r in unique if r[2] and r[2].strip() and r[4] > 0 and r[5] > 0}
    assert (len(rows), len(unique), len(clean)) == (18, 17, 15)
    expected = {}
    for row in clean:
        expected[row[3]] = expected.get(row[3], Decimal(0)) + row[4] * row[5]
    assert expected == {'Papeleria': 90000, 'Alimentos': 101000, 'Tecnologia': 348000}

    sql = (ROOT / 'pipeline/pipeline_ventas.sql').read_text(encoding='utf-8')
    sql = re.sub(r'--[^\n]*', '', sql)
    # SQLite solo valida los SELECT y resultados de ejemplo; no soporta el DDL de Lakeflow.
    adapted = re.sub(r"CREATE OR REFRESH MATERIALIZED VIEW (\w+)\s+COMMENT '[^']*'\s+AS", r'CREATE VIEW \1 AS', sql, flags=re.I)
    assert adapted.count('CREATE VIEW') == 2
    db = sqlite3.connect(':memory:')
    db.execute('CREATE TABLE ventas_bronze (id_venta INTEGER, fecha TEXT, producto TEXT, categoria TEXT, cantidad INTEGER, precio_unitario NUMERIC)')
    db.executemany('INSERT INTO ventas_bronze VALUES (?, ?, ?, ?, ?, ?)',
                   [(r[0], r[1].isoformat(), r[2], r[3], r[4], str(r[5])) for r in rows])
    db.executescript(adapted)
    def totals():
        return dict(db.execute('SELECT categoria, total_vendido FROM pipeline_ventas_por_categoria'))
    assert totals() == expected
    assert db.execute('SELECT COUNT(*) FROM pipeline_ventas_limpias').fetchone()[0] == 15
    # Inserción protegida por ID: equivalente lógico al MERGE del notebook.
    for _ in range(2):
        db.execute("INSERT INTO ventas_bronze SELECT 999, '2026-11-06', 'Mouse especial', 'Tecnologia', 2, 25000 WHERE NOT EXISTS (SELECT 1 FROM ventas_bronze WHERE id_venta=999)")
    assert db.execute('SELECT COUNT(*) FROM ventas_bronze WHERE id_venta=999').fetchone()[0] == 1
    assert totals() == {'Papeleria': 90000, 'Alimentos': 101000, 'Tecnologia': 398000}
    assert sum(totals().values()) == 589000
    assert db.execute('SELECT COUNT(*) FROM pipeline_ventas_limpias').fetchone()[0] == 16
    print('OK limpieza 18/17/15, SQL adaptado, resumen 539000/589000 y venta única 999')

    # Verifica destinos locales explícitos de Markdown; no consulta enlaces externos.
    for path in ROOT.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if '://' not in target and not target.startswith('#'):
                assert (path.parent / target.split('#')[0]).exists(), (path, target)
    print('OK enlaces locales Markdown')


if __name__ == '__main__':
    main()
