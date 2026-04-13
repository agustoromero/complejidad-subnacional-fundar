import csv, glob
from collections import Counter, defaultdict

# socioeconomicos
with open("datos_socioeconomicos.csv", encoding="utf-8", newline="") as f:
    r = csv.DictReader(f)
    rows = list(r)

periodos = Counter(x["anio"] for x in rows)
inds = defaultdict(set)
for x in rows:
    inds[x["indicador"]].add(x["anio"])

print("=== datos_socioeconomicos.csv ===")
print("Filas:", len(rows))
for p,c in sorted(periodos.items()):
    print(f"- {p}: {c} filas")

print("\n=== indicadores ===")
for k in sorted(inds):
    print(f"- {k}: {', '.join(sorted(inds[k]))}")

# fichas
print("\n=== fichas ===")
files = sorted(glob.glob("datasets_fichas/Ficha_*.csv"))
print("Cantidad fichas:", len(files))
for fp in files:
    with open(fp, encoding="utf-8", newline="") as f:
        rr = csv.reader(f)
        h = next(rr)
        n = sum(1 for _ in rr)
    print(f"- {fp}: {n} filas, {len(h)} columnas")
