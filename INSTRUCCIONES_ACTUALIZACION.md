# Instrucciones claras para completar la actualización

## Lo que ya ejecuté en el repositorio

- Auditoría estructural y temporal (`scripts/reporte_periodos.py`).
- Estandarización de la ficha de Neuquén (`scripts/estandarizar_ficha_neuquen.py`).
- Ejecución del actualizador socioeconómico (`scripts/actualizar_socioeconomicos.py`) en modo reporte (sin archivo de insumo nuevo).

## Resultado actual

- El sistema está listo para aplicar actualización automática.
- Falta tu parte: proveer `inputs/datos_socioeconomicos_nuevo.csv` con datos nuevos completos.

## Tu parte (paso a paso)

1. **Descargar y consolidar** los nuevos datos desde las fuentes oficiales (INDEC, OEDE, CEP XXI/Comtrade, Capital Humano, Economía), en un único archivo con esquema:
   - `provincia,valor,indicador,anio`
2. Guardarlo como:
   - `inputs/datos_socioeconomicos_nuevo.csv`
3. Ejecutar:
   - `bash scripts/ejecutar_actualizacion_completa.sh`
4. Verificar cambios:
   - `git diff -- datos_socioeconomicos.csv`
   - `python scripts/reporte_periodos.py`
5. Si está correcto, versionar:
   - `git add datos_socioeconomicos.csv reportes/*.md`
   - `git commit -m "Actualiza datos socioeconómicos a <periodo>"`

## Checklist de validación rápida

- [ ] El archivo de input tiene las 4 columnas en el orden correcto.
- [ ] No hay indicadores fuera del catálogo esperado.
- [ ] Todas las provincias están presentes.
- [ ] Los periodos nuevos aparecen en el reporte generado.
- [ ] `git diff` muestra cambios esperados (sin roturas de formato).
