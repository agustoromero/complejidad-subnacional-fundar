#!/usr/bin/env python3
import csv
import glob
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOCIO = ROOT / "datos_socioeconomicos.csv"
FICHAS_GLOB = str(ROOT / "datasets_fichas" / "Ficha_*.csv")


def resumen_socioeconomico(path: Path):
    rows = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    periodos = Counter(r["anio"] for r in rows)
    indicadores = defaultdict(set)
    for r in rows:
        indicadores[r["indicador"]].add(r["anio"])

    return rows, periodos, indicadores


def resumen_fichas(pattern: str):
    files = sorted(glob.glob(pattern))
    resumen = []
    for fp in files:
        with open(fp, encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            header = next(reader)
            nrows = sum(1 for _ in reader)
        resumen.append((Path(fp).name, nrows, len(header), header))
    return resumen


if __name__ == "__main__":
    rows, periodos, indicadores = resumen_socioeconomico(SOCIO)
    fichas = resumen_fichas(FICHAS_GLOB)

    print("=== Resumen datos_socioeconomicos.csv ===")
    print(f"Filas: {len(rows)}")
    print("Períodos presentes:")
    for p, c in sorted(periodos.items()):
        print(f"- {p}: {c} filas")

    print("\nIndicadores y períodos presentes:")
    for ind in sorted(indicadores):
        p = ", ".join(sorted(indicadores[ind]))
        print(f"- {ind}: {p}")

    print("\n=== Resumen fichas provinciales ===")
    print(f"Cantidad de fichas: {len(fichas)}")
    if fichas:
        print(f"Columnas esperadas (de la primera ficha): {fichas[0][2]}")
    for nombre, nrows, ncols, _ in fichas:
        print(f"- {nombre}: {nrows} filas, {ncols} columnas")
