#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'datasets_fichas' / 'Ficha_Neuquén.csv'

OUTPUT_COLUMNS = [
    'codigo_hs','product_name_en','nombre_producto_es','seccion_atlas','seccion_2_digitos',
    'indice_de_complejidad_de_producto_icp','ranking_de_complejidad_producto','tendencia_mercado','potencial_exportador',
    'fob_neuquen','vcr_neuquen','compatibilidad_con_neuquen','valor_estrategico_para_neuquen',
    'indice_recuperacion_de_posiciones_neuquen','indice_oportunidades_cercanas_neuquen',
    'indice_objetivos_factibles_neuquen','indice_apuestas_ambiciosas_neuquen','top_20_criterios_neuquen',
    'empleo','empresas','tasa_fem'
]

RENAME = {
    'seccion_harvard': 'seccion_atlas',
    'complejidad_producto': 'indice_de_complejidad_de_producto_icp',
}


def main():
    with TARGET.open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    transformed = []
    for row in rows:
        new_row = {}
        # base values
        for k, v in row.items():
            if k == 'unnamed_0':
                continue
            new_key = RENAME.get(k, k)
            new_row[new_key] = v

        # columns absent in original Neuquén
        new_row.setdefault('nombre_producto_es', '')
        new_row.setdefault('empleo', '')
        new_row.setdefault('empresas', '')
        new_row.setdefault('tasa_fem', '')

        transformed.append({col: new_row.get(col, '') for col in OUTPUT_COLUMNS})

    with TARGET.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(transformed)

    print(f'Estandarizada {TARGET} con {len(transformed)} filas y {len(OUTPUT_COLUMNS)} columnas')


if __name__ == '__main__':
    main()
