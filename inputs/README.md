# Insumo para actualización socioeconómica

Para que el proceso automático aplique la actualización, crear:

- `inputs/datos_socioeconomicos_nuevo.csv`

Con **columnas exactas** y en este orden:

```csv
provincia,valor,indicador,anio
```

## Plantilla mínima

```csv
"provincia","valor","indicador","anio"
"Buenos Aires","0.00000","Densidad Población Habitantes/Km2","2025"
```

## Reglas

- Codificación: UTF-8
- Separador: coma
- Comillas dobles para campos de texto
- Mantener nomenclatura de `indicador` consistente con `datos_socioeconomicos.csv`
- Incluir todas las provincias y todos los indicadores para una actualización completa
