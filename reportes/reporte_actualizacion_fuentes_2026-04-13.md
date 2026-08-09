# Reporte de actualización de fuentes y períodos

Fecha de corte del chequeo: **2026-04-13**.

## 1) Estado del repositorio actual (base vigente)

### 1.1 Datos socioeconómicos cargados en el repo

Archivo: `datos_socioeconomicos.csv`.

- Filas: **221**.
- Períodos presentes:
  - **2017-2019**: 47 filas.
  - **2020**: 76 filas.
  - **2021**: 98 filas.

Indicadores y período cargado en el repo:

| Indicador | Período en repo |
|---|---|
| Exportaciones totales (M USD) | 2017-2019 |
| Proporción de las exportaciones totales de Argentina | 2017-2019 |
| Empresas privadas Cada 1000 habitantes | 2020 |
| Empresas privadas industriales Cada 1000 habitantes | 2020 |
| Graduados Universitarios Total | 2020 |
| Graduados Universitarios cada 1000 habitantes | 2020 |
| Densidad Población Habitantes/Km2 | 2021 |
| Empleo privado registrado Cada 1000 habitantes | 2021 |
| Empleo privado registrado % del total de Argentina | 2021 |
| VAB per cápita (Argentina=100) | 2021 |

### 1.2 Fichas provinciales de complejidad cargadas en el repo

Carpeta: `datasets_fichas/`.

- Cantidad de fichas: **23**.
- Cantidad de filas por ficha: **4663**.
- Estructura esperada: **21 columnas**.
- Hallazgo de consistencia: `Ficha_Neuquén.csv` aparece con **18 columnas** (desvío frente al resto).

## 2) Fuentes oficiales usadas por el repositorio y disponibilidad observada hoy

Fuentes listadas en `README.md`:

- CEP XXI (Dirección Nacional de Estudios para la Producción)
- Comtrade
- INDEC
- Ministerio de Economía
- OEDE
- Ministerio de Educación (actualmente Ministerio de Capital Humano)

Chequeo de disponibilidad institucional y de datos abiertos (estado del portal a fecha 2026-04-13):

| Fuente | Estado de disponibilidad del portal | Referencia |
|---|---|---|
| CEP XXI | Activo | https://www.argentina.gob.ar/produccion/cep |
| CEP XXI datasets | Activo | https://www.argentina.gob.ar/produccion/cep/datasets-y-otros-recursos |
| Comtrade | Activo | https://comtradeplus.un.org/ |
| INDEC | Activo | https://www.indec.gob.ar/ |
| Ministerio de Economía | Activo | https://www.argentina.gob.ar/economia |
| OEDE | Activo | https://www.argentina.gob.ar/observatorio-de-empleo-y-dinamica-empresarial-oede |
| Ministerio de Capital Humano (catálogo) | Activo | https://www.argentina.gob.ar/capital-humano/catalogos-de-datos-abiertos |

> Nota metodológica: en varias de estas instituciones conviven múltiples datasets con diferentes periodicidades. Para afirmar el “último período disponible” de manera exacta por variable, se requiere identificar la URL puntual de cada dataset/API usado en la construcción original.

## 3) Resultado de actualización ejecutada en este trabajo

### 3.1 ¿Qué se actualizó efectivamente?

- **No se actualizaron valores numéricos de fichas ni de `datos_socioeconomicos.csv`**, porque el repositorio no incluye pipeline de cálculo (scripts ETL/modelado) ni mapeo de URLs exactas por variable.
- Sí se dejó implementado un script de auditoría reproducible de períodos y estructura para facilitar la actualización posterior.

### 3.2 Datos que quedan igual (con referencia temporal)

Se mantienen sin cambios los períodos actualmente cargados:

- 2017-2019: exportaciones y proporción de exportaciones.
- 2020: empresas y graduados.
- 2021: empleo, densidad y VAB per cápita.

### 3.3 Cambios observados relevantes (calidad de datos)

- Se detectó una inconsistencia estructural en `Ficha_Neuquén.csv` (18 columnas vs 21 columnas del resto).
- **Estado actual**: inconsistencia resuelta en este repositorio mediante estandarización de esquema a 21 columnas.

## 4) Próximo paso sugerido para completar actualización total

1. Definir una tabla de mapeo `variable -> fuente -> URL/API -> frecuencia -> transformaciones`.
2. Incorporar script de descarga automática por fuente.
3. Estandarizar esquema de fichas (corregir desvío de Neuquén).
4. Recalcular indicadores de complejidad con metodología original (hoy no versionada en este repo).
5. Emitir diff cuantitativo contra la versión previa por provincia e indicador.
