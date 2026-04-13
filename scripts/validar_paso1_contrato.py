#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_FILE = ROOT / 'config' / 'mapeo_fuentes_socioeconomicas.csv'
CAT_FILE = ROOT / 'config' / 'catalogo_provincias.csv'
REPORT = ROOT / 'reportes' / 'validacion_paso1_contrato_2026-04-13.md'

REQUIRED_MAP_COLS = [
    'indicador','fuente','url_referencia_dataset','url_referencia_catalogo','frecuencia','geografia',
    'unidad','nivel_agregacion_temporal','regla_ultimo_dato','transformaciones','periodo_en_repo',
    'ultimo_periodo_disponible_verificado','validaciones_minimas','estado_contrato'
]
REQUIRED_CAT_COLS = ['provincia_canonica','alias_permitidos']


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as f:
        r = csv.DictReader(f)
        rows = list(r)
        return r.fieldnames, rows


def main():
    map_cols, map_rows = read_csv(MAP_FILE)
    cat_cols, cat_rows = read_csv(CAT_FILE)

    errors = []
    if map_cols != REQUIRED_MAP_COLS:
        errors.append(f'Columnas inválidas en mapeo: {map_cols}')
    if cat_cols != REQUIRED_CAT_COLS:
        errors.append(f'Columnas inválidas en catálogo provincias: {cat_cols}')

    # complete checks
    for i, row in enumerate(map_rows, start=2):
        for col in REQUIRED_MAP_COLS:
            if not (row.get(col) or '').strip():
                errors.append(f'Fila {i} sin valor en columna {col}')

    for i, row in enumerate(cat_rows, start=2):
        for col in REQUIRED_CAT_COLS:
            if not (row.get(col) or '').strip():
                errors.append(f'Catálogo fila {i} sin valor en columna {col}')

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with REPORT.open('w', encoding='utf-8') as f:
        f.write('# Validación Paso 1 - Contrato de actualización\n\n')
        f.write(f'- Indicadores en mapeo: {len(map_rows)}\n')
        f.write(f'- Provincias/aliases en catálogo: {len(cat_rows)}\n')
        f.write(f'- Errores detectados: {len(errors)}\n\n')
        if errors:
            f.write('## Errores\n')
            for e in errors:
                f.write(f'- {e}\n')
        else:
            f.write('## Resultado\n- ✅ Paso 1 validado sin errores estructurales.\n')

    if errors:
        for e in errors:
            print(e)
        raise SystemExit(1)

    print('✅ Paso 1 validado sin errores estructurales.')
    print(f'Reporte: {REPORT}')


if __name__ == '__main__':
    main()
