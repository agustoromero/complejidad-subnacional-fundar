# Paso 1 completado: Contrato de actualización socioeconómica

Fecha: 2026-04-13

Este documento formaliza el **contrato de actualización** para que la automatización produzca resultados reproducibles.

## Entregables implementados

1. Tabla maestra de indicadores con contrato expandido:
   - `config/mapeo_fuentes_socioeconomicas.csv`
2. Catálogo geográfico único (provincias + aliases):
   - `config/catalogo_provincias.csv`
3. Criterios de aceptación del paso 1:
   - Campos completos por indicador.
   - Diccionario canónico de nombres.
   - Reglas de último dato y transformaciones explícitas.
   - Validaciones mínimas definidas.

## Definition of Done del Paso 1

- [x] Todo indicador tiene fuente y referencia de dataset/catálogo.
- [x] Todo indicador tiene frecuencia, geografía, unidad y nivel temporal.
- [x] Todo indicador tiene regla de último dato definida.
- [x] Todo indicador tiene transformación matemática explícita.
- [x] Todo indicador tiene validaciones mínimas documentadas.
- [x] Existe catálogo único de provincias y aliases.
- [x] Se mantiene el esquema de salida final esperado (`provincia,valor,indicador,anio`).

## Intervención humana obligatoria (seguridad del proceso)

1. Confirmar endpoint oficial exacto por indicador antes de automatizar descarga.
2. Confirmar criterio institucional del “último dato” para cada fuente.
3. Aprobar cambios atípicos en valores antes de merge.
4. Aprobar commit final de actualización.
