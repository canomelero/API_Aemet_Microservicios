---
name: Microservice Contract
description: Reglas para usar los JSON Schema de contracts/ como fuente de verdad y evitar divergencias entre servicios Python y Java.
---

# Microservice Contract

Usa esta skill cuando implementes, revises o evoluciones un contrato de microservicio.

## Fuente de verdad

- Los contratos están en `contracts/`.
- Cada servicio consume el mismo esquema; no se copia ni se renombra.
- El contrato actual es `contracts/municipio.schema.json`.
- Los nombres de los campos son exactos y sensibles a mayúsculas.

## Reglas

1. No inventes campos que no estén en el esquema.
2. No omitas campos obligatorios.
3. No cambies tipos sin actualizar el esquema y todos los servicios.
4. No añadas envoltorios como `data`, `result` o `payload` si el esquema no los define.
5. No devuelvas campos adicionales; usa validación estricta.
6. Mantén los mismos nombres en Python, Java y JSON.
7. Documenta cualquier cambio de contrato antes de aplicarlo.
8. Si el cambio es incompatible, versiona el contrato o el endpoint.

## Validación por lenguaje

### Python

```python
class Municipio(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    municipioid: int
    gentilicio: str
    sitioweb: str
    provincia: str
```

- `extra="forbid"` impide campos adicionales.
- `model_validate` valida el JSON local al cargarlo.
- `response_model` valida la respuesta del endpoint.

### Java

- Usa un DTO con exactamente los campos del contrato.
- Configura Jackson para fallar ante propiedades desconocidas cuando corresponda.
- No uses `Map<String, Object>` como contrato público.
- Mantén los nombres de propiedades alineados con el JSON.

## Evolución

- Campo opcional nuevo: actualizar esquema, DTOs y documentación.
- Campo obligatorio nuevo: cambio incompatible; valorar nueva versión.
- Renombrado o cambio de tipo: cambio incompatible; no hacerlo sin migración.
- Eliminación de campo: cambio incompatible; no hacerlo sin migración.

## Comprobación manual

Cuando se soliciten tests, la respuesta debe validarse contra el esquema con `jsonschema`.
En la fase actual no se crean tests ni se ejecutan validaciones.
