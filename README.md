# API AEMET Microservicios

Repositorio de microservicios para la consulta de datos de municipios y, en fases posteriores, datos meteorológicos de AEMET.

El proyecto se construye paso a paso, con contratos JSON compartidos y servicios independientes en Python/FastAPI y Java/Spring Boot.

## Estado actual

- Servicio `municipio-service` implementado en Python/FastAPI con respuesta estática desde JSON local.
- Servicio `municipio-geo-service` implementado en Python/FastAPI que consulta AEMET OpenData.
- Servicio `municipio-meteo-service` implementado en Python/FastAPI que consulta AEMET OpenData.
- Servicio `municipio-demo-service` implementado en Java/Spring Boot con respuesta estática desde JSON local.
- Servicio `municipio-orquestador-service` implementado en Java/Spring Boot que compone los datos de Granada.
- `municipio-service` y `municipio-demo-service` no realizan llamadas externas.
- `municipio-geo-service` requiere la variable de entorno `AEMET_API_KEY`.
- `municipio-meteo-service` toma su `AEMET_API_KEY` de `app/config.py` (configuración provisional).
- Sin base de datos ni autenticación propia.
- Tests pendientes para una fase posterior.

## Estructura

```text
.
├── .opencode/
│   ├── agents/
│   │   ├── python-fastapi.md
│   │   └── java-spring.md
│   └── skills/
│       ├── fastapi-service/SKILL.md
│       ├── springboot-service/SKILL.md
│       ├── microservice-contract/SKILL.md
│       └── solid-best-practices/SKILL.md
├── contracts/
│   ├── json_schema_municipio.json
│   ├── json_schema_municipio_geo.json
│   ├── json_schema_municipio_meteo.json
│   ├── json_schema_municipio_demo.json
│   └── json_schema_municipio_combinado.json
├── services/
│   ├── municipio-service/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   ├── models/
│   │   │   ├── repositories/
│   │   │   ├── data/
│   │   │   └── main.py
│   │   ├── requirements.txt
│   │   └── README.md
│   ├── municipio-geo-service/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   ├── clients/
│   │   │   ├── models/
│   │   │   ├── repositories/
│   │   │   ├── config.py
│   │   │   └── main.py
│   │   ├── requirements.txt
│   │   └── README.md
│   ├── municipio-meteo-service/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   ├── clients/
│   │   │   ├── models/
│   │   │   ├── repositories/
│   │   │   ├── config.py
│   │   │   └── main.py
│   │   ├── requirements.txt
│   │   └── README.md
│   ├── municipio-demo-service/
│   │   ├── src/
│   │   │   └── main/
│   │   │       ├── java/com/example/municipiodemo/
│   │   │       │   ├── api/
│   │   │       │   ├── domain/
│   │   │       │   └── repository/
│   │   │       └── resources/
│   │   │           └── data/
│   │   ├── pom.xml
│   │   └── README.md
│   └── municipio-orquestador-service/
│       ├── src/
│       │   └── main/
│       │       ├── java/com/example/municipioorquestador/
│       │       │   ├── api/
│       │       │   ├── client/
│       │       │   ├── config/
│       │       │   ├── domain/
│       │       │   └── service/
│       │       └── resources/
│       ├── pom.xml
│       └── README.md
└── README.md
```

## Contratos

Los esquemas JSON son la fuente de verdad y se comparten entre servicios.

| Contrato | Descripción |
|---|---|
| `contracts/json_schema_municipio.json` | Datos de un municipio: `municipioid`, `gentilicio`, `sitioweb` y `provincia`. |
| `contracts/json_schema_municipio_geo.json` | Datos geográficos de un municipio: `municipioid`, `latitud`, `longitud` y `altitud`. |
| `contracts/json_schema_municipio_meteo.json` | Datos meteorológicos de un municipio: `municipioid`, `temperatura_actual`, `temperaturas`, `humedad`, `viento`, `precipitacion` y `estadocielo`. |
| `contracts/json_schema_municipio_demo.json` | Datos demográficos y políticos de un municipio: `municipioid`, `alcalde`, `partidopolitico` y `numhabitantes`. |
| `contracts/json_schema_municipio_combinado.json` | Composición de dos recursos: `municipioid` y al menos uno de `geo`, `meteo` o `demo`, cada uno con su contrato original. |

## Catálogo de servicios

| Servicio | Tecnología | Endpoint | Puerto | Estado |
|---|---|---|---|---|
| `municipio-service` | Python 3.12 + FastAPI | `GET /municipio` | 8001 | Implementado |
| `municipio-geo-service` | Python 3.12 + FastAPI | `GET /municipio/geo` | 8002 | Implementado |
| `municipio-meteo-service` | Python 3.12 + FastAPI | `GET /granada/meteo` | 8003 | Implementado |
| `municipio-demo-service` | Java 21 + Spring Boot | `GET /granada/demo` | 8004 | Implementado |
| `municipio-orquestador-service` | Java 21 + Spring Boot | `GET /granada/{tipo1}/{tipo2}` | 8005 | Implementado |

### `municipio-service`

Devuelve el municipio de Granada con id `18087` desde un JSON local:

```json
{
  "municipioid": 18087,
  "gentilicio": "granadino",
  "sitioweb": "https://www.granada.org",
  "provincia": "Granada"
}
```

No realiza llamadas a AEMET ni a ningún otro servicio.

### `municipio-geo-service`

Consulta AEMET OpenData y devuelve los datos geográficos de Granada con id `18087`:

```json
{
  "municipioid": 18087,
  "latitud": 37.176389,
  "longitud": -3.6,
  "altitud": 684.0
}
```

Requiere configurar `AEMET_API_KEY`. Sin la clave, el endpoint responde `503 Service Unavailable`.

### `municipio-meteo-service`

Consulta AEMET OpenData y devuelve los datos meteorológicos de Granada con id `18087`:

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

Usa la predicción diaria de AEMET. La clave se define en `app/config.py` como
configuración provisional. Sin clave, el endpoint responde `503 Service Unavailable`.

### `municipio-demo-service`

Devuelve los datos demográficos y políticos de Granada con id `18087` desde un
JSON local:

```json
{
  "municipioid": 18087,
  "alcalde": "Marifrán Carazo Villalonga",
  "partidopolitico": "PP",
  "numhabitantes": 233975
}
```

Los datos proceden de Wikipedia (artículo *Granada*): alcaldesa Marifrán Carazo
Villalonga (PP) y 233.975 habitantes (2025). No realiza llamadas a AEMET ni a
ningún otro servicio.

### `municipio-orquestador-service`

Orquesta los servicios anteriores mediante composición centralizada. Expone:

```text
GET /granada/{tipo1}/{tipo2}
```

Cada tipo debe ser `geo`, `meteo` o `demo`:

| Tipo | Servicio consultado |
|---|---|
| `geo` | `municipio-geo-service` (`GET /municipio/geo`) |
| `meteo` | `municipio-meteo-service` (`GET /granada/meteo`) |
| `demo` | `municipio-demo-service` (`GET /granada/demo`) |

Ejemplo de `GET /granada/geo/meteo`:

```json
{
  "municipioid": 18087,
  "geo": {
    "municipioid": 18087,
    "latitud": 37.176389,
    "longitud": -3.6,
    "altitud": 684.0
  },
  "meteo": {
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
}
```

Características:

- Los bloques no solicitados se omiten del JSON.
- Si los dos tipos coinciden, el servicio se consulta una sola vez.
- Valida que todos los servicios devuelvan el municipio `18087`.
- La composición es atómica: si un servicio falla, no se devuelve un resultado
  parcial.
- Las URLs de los servicios remotos se configuran en `application.yml`.

## Agentes

| Agente | Modo | Uso |
|---|---|---|
| `python-fastapi` | Subagente | Implementa y mantiene servicios Python/FastAPI. |
| `java-spring` | Subagente | Implementa y mantiene servicios Java/Spring Boot. |

Los agentes built-in `build` y `plan` siguen actuando como orquestadores.

## Skills

| Skill | Uso |
|---|---|
| `fastapi-service` | Estructura y convenciones de servicios FastAPI. |
| `springboot-service` | Estructura y convenciones de servicios Spring Boot. |
| `microservice-contract` | Uso del JSON Schema como fuente de verdad. |
| `solid-best-practices` | SOLID, código limpio y buenas prácticas en Python y Java. |

## Ejecución de los servicios

### `municipio-service`

```bash
cd services/municipio-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Comprobación:

```bash
curl http://localhost:8001/municipio
```

La documentación interactiva de FastAPI queda disponible en `http://localhost:8001/docs`.

### `municipio-geo-service`

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
curl http://localhost:8002/municipio/geo
```

La documentación interactiva de FastAPI queda disponible en `http://localhost:8002/docs`.

### `municipio-meteo-service`

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

La documentación interactiva de FastAPI queda disponible en `http://localhost:8003/docs`.

### `municipio-demo-service`

```bash
cd services/municipio-demo-service
mvn spring-boot:run
```

Comprobación:

```bash
curl http://localhost:8004/granada/demo
```

### `municipio-orquestador-service`

Requiere tener levantados los servicios correspondientes a los tipos
solicitados (`geo` 8002, `meteo` 8003, `demo` 8004). `geo` y `meteo` necesitan
`AEMET_API_KEY`.

```bash
cd services/municipio-orquestador-service
mvn spring-boot:run
```

Comprobación:

```bash
curl http://localhost:8005/granada/geo/meteo
curl http://localhost:8005/granada/meteo/demo
curl http://localhost:8005/granada/geo/geo
```

## Siguientes pasos

1. Añadir tests de respuesta y validación contra los contratos.
2. Configurar `AEMET_API_KEY` y validar la respuesta real de `municipio-geo-service`.
3. Mover la clave de AEMET de `app/config.py` a variables de entorno en los servicios que la consultan.
4. Añadir tests de respuesta y validación del contrato al servicio Java.
5. Añadir tests de composición, propagación de errores y validación del contrato combinado.
6. Añadir resiliencia al orquestador: reintentos, circuit breaker y paralelización de llamadas.
7. Añadir gateway y Docker Compose cuando el conjunto de servicios lo requiera.

## Principios del proyecto

- Contrato primero: ningún servicio inventa campos ni formatos.
- Servicios independientes y con una responsabilidad clara.
- Dependencias mínimas.
- Sin secretos en el repositorio.
- Cambios pequeños y verificables.
