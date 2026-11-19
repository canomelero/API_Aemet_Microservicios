# Municipio Service

Microservicio Python/FastAPI que devuelve los datos del municipio de Granada con id `18087`.

## Endpoint

```text
GET /municipio
```

Respuesta:

```json
{
  "municipioid": 18087,
  "gentilicio": "granadino",
  "sitioweb": "https://www.granada.org",
  "provincia": "Granada"
}
```

Características:

- Respuesta estática desde un JSON local.
- Sin llamadas externas.
- Sin base de datos.
- Sin campos adicionales.
- Contrato validado con Pydantic mediante `extra="forbid"`.

## Estructura

```text
municipio-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── municipio.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── municipio.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── municipio_repository.py
│   └── data/
│       └── municipio_18087.json
├── requirements.txt
└── README.md
```

## Capas

| Capa | Responsabilidad |
|---|---|
| `app/api/municipio.py` | Expone el endpoint HTTP y gestiona errores. |
| `app/models/municipio.py` | Define el contrato Pydantic del municipio. |
| `app/repositories/municipio_repository.py` | Carga y valida el JSON local. |
| `app/main.py` | Crea y configura la aplicación FastAPI. |

La capa HTTP depende de una función factoría del repositorio mediante `Depends`. Esto permite sustituir el origen de datos sin modificar el endpoint.

## Contrato

El modelo sigue el esquema compartido:

```text
../../contracts/municipio.schema.json
```

Campos obligatorios:

| Campo | Tipo |
|---|---|
| `municipioid` | entero |
| `gentilicio` | cadena |
| `sitioweb` | cadena |
| `provincia` | cadena |

## Requisitos

- Python 3.12
- pip

## Ejecución

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Comprobación:

```bash
curl http://localhost:8001/municipio
```

Documentación interactiva:

```text
http://localhost:8001/docs
```

## Tests

No se han creado tests en esta fase por indicación expresa. Quedan pendientes:

- Respuesta `200` y `application/json`.
- Contenido exacto de los cuatro campos.
- Validación contra `contracts/municipio.schema.json`.
