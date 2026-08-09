#!/usr/bin/env python3
import csv
from pathlib import Path
from collections import Counter, defaultdict
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / 'config' / 'mapeo_fuentes_socioeconomicas.csv'
CURRENT = ROOT / 'datos_socioeconomicos.csv'
CANDIDATE = ROOT / 'inputs' / 'datos_socioeconomicos_nuevo.csv'
REPORT = ROOT / 'reportes' / f'estado_actualizacion_socioeconomica_{date.today().isoformat()}.md'

REQUIRED_COLS = ['provincia', 'valor', 'indicador', 'anio']


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        header = reader.fieldnames
    return header, rows


def validate_schema(header):
    if header != REQUIRED_COLS:
        raise ValueError(f'Esquema inválido. Esperado {REQUIRED_COLS}, recibido {header}')


def summarize(rows):
    by_indicator = defaultdict(set)
    by_period = Counter()
    for r in rows:
        by_indicator[r['indicador']].add(r['anio'])
        by_period[r['anio']] += 1
    return by_indicator, by_period


def load_mapping(path):
    _, rows = read_csv(path)
    return rows


def write_report(mapping_rows, old_summary, new_summary=None, applied=False):
    old_ind, old_period = old_summary
    new_ind, new_period = (new_summary if new_summary else ({}, {}))

    lines = []
    lines.append('# Estado de actualización socioeconómica')
    lines.append('')
    lines.append(f'Fecha: {date.today().isoformat()}')
    lines.append('')
    lines.append('## Resumen')
    lines.append(f'- Actualización aplicada: **{"sí" if applied else "no"}**.')
    lines.append('')
    lines.append('## Períodos en dataset actual')
    for p, c in sorted(old_period.items()):
        lines.append(f'- {p}: {c} filas')
    lines.append('')

    if applied:
        lines.append('## Períodos en dataset nuevo')
        for p, c in sorted(new_period.items()):
            lines.append(f'- {p}: {c} filas')
        lines.append('')

    lines.append('## Estado por indicador')
    lines.append('| Indicador | Período en repo | Último período disponible verificado | Estado |')
    lines.append('|---|---|---|---|')

    for row in mapping_rows:
        ind = row['indicador']
        periodos = ', '.join(sorted(old_ind.get(ind, []))) or 'no_encontrado'
        ultimo = row['ultimo_periodo_disponible_verificado']
        estado = 'sin_actualizar' if (ultimo == 'pendiente_verificacion_dataset' or ultimo in periodos) else 'pendiente_actualizacion'
        if applied and ind in new_ind:
            new_periodos = ', '.join(sorted(new_ind[ind]))
            if new_periodos != periodos:
                estado = f'actualizado ({periodos} -> {new_periodos})'
        lines.append(f"| {ind} | {periodos} | {ultimo} | {estado} |")

    lines.append('')
    if not applied:
        lines.append('> Para aplicar actualización automática, guardar un archivo candidato en `inputs/datos_socioeconomicos_nuevo.csv` con columnas exactas: `provincia,valor,indicador,anio`.')

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Reporte generado: {REPORT}')


def main():
    cur_header, cur_rows = read_csv(CURRENT)
    validate_schema(cur_header)
    mapping_rows = load_mapping(MAPPING)

    old_summary = summarize(cur_rows)

    if CANDIDATE.exists():
        new_header, new_rows = read_csv(CANDIDATE)
        validate_schema(new_header)
        # replace dataset
        with CURRENT.open('w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=REQUIRED_COLS, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(new_rows)
        write_report(mapping_rows, old_summary, summarize(new_rows), applied=True)
    else:
        write_report(mapping_rows, old_summary, applied=False)


if __name__ == '__main__':
    main()
