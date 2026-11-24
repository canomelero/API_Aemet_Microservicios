# Municipio Orquestador Service

Microservicio Java 21 + Spring Boot que orquesta los servicios de datos de
Granada y devuelve un recurso compuesto.

## Patrón

Orquestación centralizada (*API Composition*): este servicio es el único que
conoce a los demás. Los servicios `geo`, `meteo` y `demo` no se llaman entre
sí y no saben que existe un orquestador.

```text
Cliente
  │  GET /granada/geo/meteo
  ▼
municipio-orquestador-service :8005
  ├── HTTP GET /municipio/geo   → municipio-geo-service   :8002
  └── HTTP GET /granada/meteo   → municipio-meteo-service :8003
  │
  └── compone { municipioid, geo, meteo }
```

## Endpoint

```text
GET /granada/{tipo1}/{tipo2}
```

`tipo1` y `tipo2` deben ser exactamente uno de:

| Tipo | Servicio consultado | Endpoint remoto |
|---|---|---|
| `geo` | `municipio-geo-service` | `GET http://localhost:8002/municipio/geo` |
| `meteo` | `municipio-meteo-service` | `GET http://localhost:8003/granada/meteo` |
| `demo` | `municipio-demo-service` | `GET http://localhost:8004/granada/demo` |

Reglas:

- Los tipos distinguen mayúsculas: solo se aceptan `geo`, `meteo` y `demo` en
  minúsculas.
- Si `tipo1` y `tipo2` coinciden, el servicio se consulta y se devuelve una
  sola vez (`/granada/geo/geo`).
- La composición es atómica: si uno de los servicios falla, no se devuelve un
  resultado parcial.
- Se valida que todos los servicios devuelvan el municipio `18087`; si no, la
  composición falla con `502`.

### Ejemplos

`GET /granada/geo/meteo`:

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

`GET /granada/meteo/demo`:

```json
{
  "municipioid": 18087,
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
  },
  "demo": {
    "municipioid": 18087,
    "alcalde": "Marifrán Carazo Villalonga",
    "partidopolitico": "PP",
    "numhabitantes": 233975
  }
}
```

`GET /granada/geo/geo` consulta una sola vez el servicio geográfico y devuelve
un único bloque `geo`.

Los bloques no solicitados se omiten del JSON; no se serializan como `null` ni
se añaden envoltorios.

## Configuración

`src/main/resources/application.yml`:

```yaml
spring:
  application:
    name: municipio-orquestador-service
  http:
    client:
      connect-timeout: 2s
      read-timeout: 10s

server:
  port: 8005

servicios:
  geo:
    base-url: http://localhost:8002
  meteo:
    base-url: http://localhost:8003
  demo:
    base-url: http://localhost:8004
```

Las URLs base son configurables; en Docker Compose o Kubernetes se sustituyen
por los nombres de servicio correspondientes sin cambiar el código.

## Errores

Las respuestas de error siguen el formato:

```json
{
  "detail": "Descripción del error"
}
```

| Situación | Código HTTP |
|---|---|
| Tipo de path no válido | `400 Bad Request` |
| El servicio remoto responde con error | Se propaga su código (por ejemplo `503` si falta `AEMET_API_KEY`, `404` o `502`) |
| Timeout al consultar un servicio remoto | `504 Gateway Timeout` |
| Conexión rechazada, JSON inválido o respuesta vacía | `502 Bad Gateway` |
| Municipios distintos o distintos de `18087` | `502 Bad Gateway` |

`geo` y `meteo` dependen de `AEMET_API_KEY`. Si falta, el orquestador devuelve
el `503` que produce el servicio remoto.

## Estructura

```text
municipio-orquestador-service/
├── pom.xml
├── .gitignore
├── README.md
└── src/main/
    ├── java/com/example/municipioorquestador/
    │   ├── MunicipioOrquestadorApplication.java
    │   ├── api/
    │   │   ├── MunicipioOrquestadorController.java
    │   │   ├── ApiExceptionHandler.java
    │   │   └── ErrorResponse.java
    │   ├── config/
    │   │   └── ServiciosProperties.java
    │   ├── client/
    │   │   ├── ClienteUpstream.java
    │   │   ├── MunicipioGeoClient.java
    │   │   ├── MunicipioMeteoClient.java
    │   │   ├── MunicipioDemoClient.java
    │   │   ├── ServicioUpstreamException.java
    │   │   └── UpstreamTimeoutException.java
    │   ├── domain/
    │   │   ├── TipoRecurso.java
    │   │   ├── TipoRecursoInvalidoException.java
    │   │   ├── MunicipioGeo.java
    │   │   ├── MunicipioMeteo.java
    │   │   ├── Temperaturas.java
    │   │   ├── MunicipioDemo.java
    │   │   ├── MunicipioCombinado.java
    │   │   └── MunicipioInconsistenteException.java
    │   └── service/
    │       └── MunicipioComposicionService.java
    └── resources/
        └── application.yml
```

## Capas

| Capa | Responsabilidad |
|---|---|
| `api/MunicipioOrquestadorController.java` | Expone `GET /granada/{tipo1}/{tipo2}` y delega en el servicio de composición. |
| `api/ApiExceptionHandler.java` | Traduce los errores de dominio y de los servicios remotos a códigos HTTP. |
| `service/MunicipioComposicionService.java` | Deduplica tipos, invoca los clientes necesarios, valida el municipio y compone la respuesta. |
| `client/ClienteUpstream.java` | Base común de los clientes: petición GET, deserialización y traducción de errores. |
| `client/Municipio*Client.java` | Adaptadores de cada servicio remoto. |
| `domain/*.java` | DTOs inmutables y excepciones del dominio. |
| `config/ServiciosProperties.java` | URLs base de los servicios remotos. |

## Contrato

El modelo sigue el esquema compartido:

```text
../../contracts/json_schema_municipio_combinado.json
```

El esquema reutiliza mediante `$ref` los contratos originales:

- `contracts/json_schema_municipio_geo.json`
- `contracts/json_schema_municipio_meteo.json`
- `contracts/json_schema_municipio_demo.json`

Campos del recurso compuesto:

| Campo | Tipo | Obligatorio |
|---|---|---|
| `municipioid` | entero | Sí |
| `geo` | objeto del contrato geográfico | Al menos uno de los tres bloques |
| `meteo` | objeto del contrato meteorológico | Al menos uno de los tres bloques |
| `demo` | objeto del contrato demográfico y político | Al menos uno de los tres bloques |

## Requisitos

- Java 21
- Maven 3.6.3 o superior
- Servicios correspondientes a los tipos solicitados levantados (`geo` 8002, `meteo` 8003, `demo` 8004)
- `AEMET_API_KEY` configurada en `geo` y `meteo` para obtener datos reales

## Ejecución

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

## Tests

No se han creado tests en esta fase. Quedan pendientes:

- Composición de dos tipos y de un tipo repetido.
- Respuesta `400` con tipos inválidos.
- Propagación de errores `502`, `503` y `504` de los servicios remotos.
- Validación de la respuesta contra `contracts/json_schema_municipio_combinado.json`.
- Resiliencia: timeouts, reintentos y circuit breaker.
