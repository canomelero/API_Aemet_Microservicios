# Municipio Meteo Service

Microservicio Python/FastAPI que devuelve los datos meteorológicos del municipio de Granada (id `18087`) consultando AEMET OpenData.

## Endpoint

```text
GET /granada/meteo
```

Respuesta:

```json
{
  "municipioid": 18087,
  "temperatura_actual": "14",
  "temperaturas": {
    "max": "23",
    "min": "2"
  },
  "humedad": "80",
  "viento": "O 10",
  "precipitacion": "30",
  "estadocielo": "Intervalos nubosos con lluvia escasa"
}
```

Los valores concretos los proporciona AEMET.

Características:

- Consulta en tiempo real a AEMET OpenData.
- Sin base de datos y sin datos locales de respaldo.
- Contrato validado con Pydantic mediante `extra="forbid"`.
- Sin campos adicionales ni envoltorios.
- Valores planos como cadenas, sin unidades añadidas.

## Configuración

La clave de AEMET se define en `app/config.py`:

```python
AEMET_API_KEY = "..."
```

Es una configuración provisional para desarrollo. Si `AEMET_API_KEY` está vacía, `GET /granada/meteo` responde `503 Service Unavailable`.

## Flujo con AEMET

AEMET OpenData requiere dos peticiones:

1. `GET https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/18087`
   - Cabecera: `api_key: <AEMET_API_KEY>`.
   - Devuelve un sobre con `descripcion`, `estado`, `datos` y `metadatos`.

2. `GET <URL indicada en datos>`
   - Devuelve una lista con la predicción del municipio, sus 7 días en
     `prediccion.dia` y campos como `id`, `nombre` y `fecha`.
   - La respuesta de datos puede venir codificada en latin-1; el cliente lo
     gestiona con un decodificado de respaldo.

Se toma el día cuya `fecha` coincide con la fecha actual en `Europe/Madrid`.

Mapeo al contrato:

| AEMET | Contrato | Transformación |
|---|---|---|
| `id` = `"18087"` | `municipioid` | Se elimina el posible prefijo `id` y se convierte a entero. |
| `temperatura.dato` | `temperatura_actual` | Valor de la hora más cercana a la hora actual. |
| `temperatura.maxima` | `temperaturas.max` | Se convierte a cadena. |
| `temperatura.minima` | `temperaturas.min` | Se convierte a cadena. |
| `humedadRelativa.dato` | `humedad` | Valor de la hora más cercana a la hora actual. |
| `viento` | `viento` | Intervalo más específico que contiene la hora actual; formato `"<dirección> <velocidad>"`. |
| `probPrecipitacion` | `precipitacion` | Intervalo más específico que contiene la hora actual. |
| `estadoCielo` | `estadocielo` | Descripción del intervalo más específico con descripción no vacía. |

Nota: el producto diario de AEMET no publica milímetros de precipitación, solo
probabilidad. Por eso `precipitacion` contiene el valor de
`probPrecipitacion` (porcentaje), sin unidades.

## Errores

| Situación | Código HTTP |
|---|---|
| Falta `AEMET_API_KEY` | `503 Service Unavailable` |
| AEMET devuelve `404` o `estado: 404` | `404 Not Found` |
| Timeout de AEMET | `504 Gateway Timeout` |
| `401`, `403`, `429`, JSON inválido o campos obligatorios ausentes | `502 Bad Gateway` |
| Respuesta correcta | `200 OK` |

## Estructura

```text
municipio-meteo-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── municipio_meteo.py
│   ├── clients/
│   │   ├── __init__.py
│   │   └── aemet_client.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── municipio_meteo.py
│   └── repositories/
│       ├── __init__.py
│       └── municipio_meteo_repository.py
├── requirements.txt
└── README.md
```

## Capas

| Capa | Responsabilidad |
|---|---|
| `app/api/municipio_meteo.py` | Expone el endpoint HTTP y traduce los errores a códigos de estado. |
| `app/clients/aemet_client.py` | Realiza las peticiones HTTP a AEMET y gestiona el sobre de respuesta. |
| `app/repositories/municipio_meteo_repository.py` | Normaliza la predicción de AEMET al contrato compartido. |
| `app/models/municipio_meteo.py` | Define el contrato Pydantic de los datos meteorológicos. |
| `app/config.py` | Configuración: clave, URL base, timeout e id del municipio. |
| `app/main.py` | Crea y configura la aplicación FastAPI. |

La capa HTTP depende de una función factoría del repositorio mediante `Depends`. El cliente de AEMET también se inyecta, lo que permite sustituirlo sin modificar el endpoint.

## Contrato

El modelo sigue el esquema compartido:

```text
../../contracts/json_schema_municipio_meteo.json
```

Campos obligatorios:

| Campo | Tipo |
|---|---|
| `municipioid` | entero |
| `temperatura_actual` | cadena |
| `temperaturas.max` | cadena |
| `temperaturas.min` | cadena |
| `humedad` | cadena |
| `viento` | cadena |
| `precipitacion` | cadena |
| `estadocielo` | cadena |

## Requisitos

- Python 3.12
- pip

## Ejecución

```bash
cd services/municipio-meteo-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8003
```

Comprobación:

```bash
curl http://localhost:8003/granada/meteo
```

Documentación interactiva:

```text
http://localhost:8003/docs
```

## Tests

No se han creado tests en esta fase. Quedan pendientes:

- Respuesta `200` y `application/json` con AEMET simulado.
- Validación contra `contracts/json_schema_municipio_meteo.json`.
- Respuesta `503` cuando `AEMET_API_KEY` está vacía.
- Traducción de errores de AEMET a `404`, `502` y `504`.
