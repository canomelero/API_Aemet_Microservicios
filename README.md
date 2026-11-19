# API AEMET Microservicios

Repositorio de microservicios para la consulta de datos de municipios y, en fases posteriores, datos meteorológicos de AEMET.

El proyecto se construye paso a paso, con contratos JSON compartidos y servicios independientes en Python/FastAPI y Java/Spring Boot.

## Estado actual

- Servicio `municipio-service` implementado en Python/FastAPI.
- Respuesta estática desde JSON local.
- Sin llamadas externas, base de datos ni autenticación.
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
│   └── municipio.schema.json
├── services/
│   └── municipio-service/
│       ├── app/
│       │   ├── api/
│       │   ├── models/
│       │   ├── repositories/
│       │   ├── data/
│       │   └── main.py
│       ├── requirements.txt
│       └── README.md
└── README.md
```

## Contratos

Los esquemas JSON son la fuente de verdad y se comparten entre servicios.

| Contrato | Descripción |
|---|---|
| `contracts/municipio.schema.json` | Datos de un municipio: `municipioid`, `gentilicio`, `sitioweb` y `provincia`. |

## Catálogo de servicios

| Servicio | Tecnología | Endpoint | Puerto | Estado |
|---|---|---|---|---|
| `municipio-service` | Python 3.12 + FastAPI | `GET /municipio` | 8001 | Implementado |

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

## Agentes

| Agente | Modo | Uso |
|---|---|---|
| `python-fastapi` | Subagente | Implementa y mantiene servicios Python/FastAPI. |
| `java-spring` | Subagente | Reservado para los futuros servicios Java/Spring Boot. |

Los agentes built-in `build` y `plan` siguen actuando como orquestadores.

## Skills

| Skill | Uso |
|---|---|
| `fastapi-service` | Estructura y convenciones de servicios FastAPI. |
| `springboot-service` | Estructura y convenciones de servicios Spring Boot. |
| `microservice-contract` | Uso del JSON Schema como fuente de verdad. |
| `solid-best-practices` | SOLID, código limpio y buenas prácticas en Python y Java. |

## Ejecución del servicio

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

## Siguientes pasos

1. Añadir tests de respuesta y validación contra el contrato.
2. Incorporar el servicio meteorológico de AEMET.
3. Crear el primer servicio Java/Spring Boot reutilizando los contratos.
4. Añadir gateway y Docker Compose cuando el conjunto de servicios lo requiera.

## Principios del proyecto

- Contrato primero: ningún servicio inventa campos ni formatos.
- Servicios independientes y con una responsabilidad clara.
- Dependencias mínimas.
- Sin secretos en el repositorio.
- Cambios pequeños y verificables.
