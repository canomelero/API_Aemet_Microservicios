# Municipio Demo Service

Microservicio Java/Spring Boot que devuelve datos demográficos y políticos del municipio de Granada (id `18087`) desde un JSON local.

## Endpoint

```text
GET /granada/demo
```

Respuesta:

```json
{
  "municipioid": 18087,
  "alcalde": "Marifrán Carazo Villalonga",
  "partidopolitico": "PP",
  "numhabitantes": 233975
}
```

Características:

- Datos servidos desde `src/main/resources/data/municipio_demo_18087.json`.
- Sin llamadas a AEMET, sin base de datos y sin autenticación.
- Contrato validado con Jackson: se rechazan propiedades desconocidas y campos obligatorios ausentes.
- Sin campos adicionales ni envoltorios.

## Origen de los datos

Los valores se han tomado de Wikipedia, artículo [Granada](https://es.wikipedia.org/wiki/Granada), consultado el 24 de noviembre de 2026:

- Alcaldesa: Marifrán Carazo Villalonga (PP).
- Población: 233.975 habitantes (2025).
- Identificador municipal: `18087`.

## Estructura

```text
municipio-demo-service/
├── pom.xml
├── .gitignore
├── README.md
└── src/
    └── main/
        ├── java/com/example/municipiodemo/
        │   ├── MunicipioDemoApplication.java
        │   ├── api/
        │   │   └── MunicipioDemoController.java
        │   ├── domain/
        │   │   └── MunicipioDemo.java
        │   └── repository/
        │       └── MunicipioDemoRepository.java
        └── resources/
            ├── application.yml
            └── data/
                └── municipio_demo_18087.json
```

## Capas

| Capa | Responsabilidad |
|---|---|
| `api/MunicipioDemoController.java` | Expone `GET /granada/demo` y delega en el repositorio. |
| `repository/MunicipioDemoRepository.java` | Carga y valida el JSON local una sola vez. |
| `domain/MunicipioDemo.java` | Define el contrato inmutable de los datos demográficos y políticos. |
| `application.yml` | Configura el nombre del servicio y el puerto `8004`. |

## Contrato

El modelo sigue el esquema compartido:

```text
../../contracts/json_schema_municipio_demo.json
```

Campos obligatorios:

| Campo | Tipo |
|---|---|
| `municipioid` | entero |
| `alcalde` | cadena |
| `partidopolitico` | cadena |
| `numhabitantes` | entero |

## Requisitos

- Java 21
- Maven 3.6.3 o superior

## Ejecución

```bash
cd services/municipio-demo-service
mvn spring-boot:run
```

Comprobación:

```bash
curl http://localhost:8004/granada/demo
```

## Tests

No se han creado tests en esta fase. Quedan pendientes:

- Respuesta `200` y `application/json` con el JSON local.
- Validación contra `contracts/json_schema_municipio_demo.json`.
- Fallo de arranque si el JSON local no existe o no cumple el contrato.
