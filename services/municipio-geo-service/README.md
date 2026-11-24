# Municipio Geo Service

Microservicio Python/FastAPI que devuelve los datos geográficos del municipio de Granada (id `18087`) consultando AEMET OpenData.

## Endpoint

```text
GET /municipio/geo
```

Respuesta:

```json
{
  "municipioid": 18087,
  "latitud": 37.176389,
  "longitud": -3.6,
  "altitud": 684.0
}
```

Los valores concretos de latitud, longitud y altitud los proporciona AEMET.

Características:

- Consulta en tiempo real a AEMET OpenData.
- Sin base de datos.
- Sin datos locales de respaldo.
- Contrato validado con Pydantic mediante `extra="forbid"`.
- Sin campos adicionales ni envoltorios.

## Configuración

Variable de entorno obligatoria:

```bash
export AEMET_API_KEY="tu_api_key"
```

Sin ella, `GET /municipio/geo` responde `503 Service Unavailable` y no devuelve datos.

No se guarda ninguna clave en el repositorio.

## Flujo con AEMET

AEMET OpenData requiere dos peticiones:

1. `GET https://opendata.aemet.es/opendata/api/maestro/municipio/id18087`
   - Cabecera: `api_key: <AEMET_API_KEY>`.
   - Devuelve un sobre con `descripcion`, `estado`, `datos` y `metadatos`.

2. `GET <URL indicada en datos>`
   - Devuelve el objeto del municipio con campos como `id`, `nombre`,
     `latitud`, `latitud_dec`, `longitud`, `longitud_dec` y `altitud`.

Mapeo al contrato:

| AEMET | Contrato | Transformación |
|---|---|---|
| `id` = `"id18087"` | `municipioid` | Se elimina el prefijo `id` y se convierte a entero. |
| `latitud_dec` | `latitud` | Se convierte a número. Si no existe, se parsea `latitud` en formato DMS. |
| `longitud_dec` | `longitud` | Se convierte a número. Si no existe, se parsea `longitud` en formato DMS. |
| `altitud` = `"684"` | `altitud` | Se convierte a número. |

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
municipio-geo-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── municipio_geo.py
│   ├── clients/
│   │   ├── __init__.py
│   │   └── aemet_client.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── municipio_geo.py
│   └── repositories/
│       ├── __init__.py
│       └── municipio_geo_repository.py
├── requirements.txt
└── README.md
```

## Capas

| Capa | Responsabilidad |
|---|---|
| `app/api/municipio_geo.py` | Expone el endpoint HTTP y traduce los errores a códigos de estado. |
| `app/clients/aemet_client.py` | Realiza las peticiones HTTP a AEMET y gestiona el sobre de respuesta. |
| `app/repositories/municipio_geo_repository.py` | Normaliza los datos de AEMET al contrato compartido. |
| `app/models/municipio_geo.py` | Define el contrato Pydantic del municipio geográfico. |
| `app/config.py` | Configuración: clave, URL base, timeout e id del municipio. |
| `app/main.py` | Crea y configura la aplicación FastAPI. |

La capa HTTP depende de una función factoría del repositorio mediante `Depends`. El cliente de AEMET también se inyecta, lo que permite sustituirlo sin modificar el endpoint.

## Contrato

El modelo sigue el esquema compartido:

```text
../../contracts/json_schema_municipio_geo.json
```

Campos obligatorios:

| Campo | Tipo |
|---|---|
| `municipioid` | entero |
| `latitud` | número |
| `longitud` | número |
| `altitud` | número |

## Requisitos

- Python 3.12
- pip

## Ejecución

```bash
cd services/municipio-geo-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export AEMET_API_KEY="tu_api_key"
uvicorn app.main:app --reload --port 8002
```

Comprobación:

```bash
curl http://localhost:8002/<municipio>/geo
```

Documentación interactiva:

```text
http://localhost:8002/docs
```

## Tests

No se han creado tests en esta fase por indicación expresa. Quedan pendientes:

- Respuesta `200` y `application/json` con AEMET simulado.
- Validación contra `contracts/json_schema_municipio_geo.json`.
- Respuesta `503` cuando falta `AEMET_API_KEY`.
- Traducción de errores de AEMET a `404`, `502` y `504`.
