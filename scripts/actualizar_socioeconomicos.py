import csv, os

required = ["provincia","valor","indicador","anio"]
src = "inputs/datos_socioeconomicos_nuevo.csv"
dst = "datos_socioeconomicos.csv"

if not os.path.exists(src):
    print("No existe inputs/datos_socioeconomicos_nuevo.csv -> no se aplicó actualización.")
    raise SystemExit(0)

with open(src, encoding="utf-8", newline="") as f:
    r = csv.DictReader(f)
    rows = list(r)
    if r.fieldnames != required:
        raise ValueError(f"Columnas inválidas. Esperado {required}, recibido {r.fieldnames}")

with open(dst, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=required, quoting=csv.QUOTE_ALL)
    w.writeheader()
    w.writerows(rows)

print(f"Actualización aplicada en {dst}. Filas: {len(rows)}")
