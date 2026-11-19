---
name: FastAPI Service
description: Convenciones para crear y mantener microservicios Python con FastAPI, Pydantic y repositorios locales en este repositorio.
---

# FastAPI Service

Usa esta skill cuando trabajes en un servicio Python/FastAPI del repositorio.

## Estructura recomendada

```text
services/<servicio>-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── <recurso>.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── <recurso>.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── <recurso>_repository.py
│   └── data/
│       └── <recurso>_<id>.json
├── requirements.txt
└── README.md
```

## Reglas de implementación

- `main.py` expone `create_app()` y una instancia `app`.
- La capa `api/` solo gestiona HTTP: parámetros, códigos de estado y errores.
- Los modelos Pydantic representan el contrato y usan `extra="forbid"`.
- Los repositorios encapsulan el origen de datos.
- No se realizan llamadas externas si el servicio debe devolver datos locales.
- No se devuelven campos adicionales ni envoltorios no definidos en el contrato.
- Las dependencias se inyectan con `Depends` para facilitar la sustitución.
- Se usan type hints y funciones pequeñas.
- No se crean tests salvo petición expresa.
- No se ejecutan servidores ni comandos de validación salvo petición expresa.

## Modelo Pydantic

```python
from pydantic import BaseModel, ConfigDict


class Recurso(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    campo: str
```

## Repositorio local

```python
class RecursoRepository:
    def get_by_id(self, recurso_id: int) -> Recurso | None:
        ...
```

El repositorio puede cargar un JSON local una sola vez y validarlo con Pydantic.
La ruta del archivo se resuelve con `Path(__file__).resolve().parent`.

## Endpoint

```python
@router.get("/recurso", response_model=Recurso)
def get_recurso(
    repository: RecursoRepository = Depends(get_recurso_repository),
) -> Recurso:
    ...
```

- Usa `response_model` para documentar y validar la salida.
- Usa `status.HTTP_200_OK` y errores explícitos.
- No añadas lógica de negocio en el controlador.

## Dependencias

Mantén `requirements.txt` con rangos compatibles:

```text
fastapi>=0.115,<1.0
pydantic>=2.9,<3.0
uvicorn[standard]>=0.30,<1.0
```

## Ejecución documentada

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Documenta estos comandos en el README del servicio. No los ejecutes salvo que se solicite.
