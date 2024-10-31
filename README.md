# Consultar la API de Terremotos
Esta aplicación de escritorio permite obtener información sobre los terremotos más significativos mediante consultas específicas:

- Magnitud
  - Máxima
  - Mínima
- Intervalos de Fechas
- Eventos del Día Actual

Nota: Es necesaria una conexión estable a Internet para realizar las consultas y obtener los datos en tiempo real.

Esta aplicación hace uso de la API [Earthquake Catalog](https://earthquake.usgs.gov/fdsnws/event/1/) de la USGS

Parámetros de consulta utilizados:

- `starttime`: Fecha (_*AAAA-MM-DD*_)
- `endtime`: Fecha (_*AAAA-MM-DD*_)
- `minmagnitude`: Limitar a eventos con una magnitud mayor que el mínimo especificado.
- `maxmagnitude`: Limitar a eventos con una magnitud menor que el máximo especificado.
