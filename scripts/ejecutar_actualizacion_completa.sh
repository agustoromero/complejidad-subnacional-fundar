#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/3] Auditoría de períodos y estructura..."
python scripts/reporte_periodos.py

echo "[2/3] Estandarización de ficha Neuquén..."
python scripts/estandarizar_ficha_neuquen.py

echo "[3/3] Actualización socioeconómica (si existe inputs/datos_socioeconomicos_nuevo.csv)..."
python scripts/actualizar_socioeconomicos.py

echo "Proceso finalizado. Revisá reportes/ y git diff."
