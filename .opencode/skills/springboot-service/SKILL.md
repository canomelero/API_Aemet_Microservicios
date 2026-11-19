---
name: Spring Boot Service
description: Convenciones para crear y mantener microservicios Java 21 con Spring Boot y contratos JSON compartidos.
---

# Spring Boot Service

Usa esta skill cuando trabajes en un servicio Java/Spring Boot del repositorio.

## Estructura recomendada

```text
services/<servicio>-service/
├── pom.xml
└── src/
    ├── main/
    │   ├── java/<paquete>/
    │   │   ├── <Servicio>Application.java
    │   │   ├── api/
    │   │   │   └── <Recurso>Controller.java
    │   │   ├── domain/
    │   │   │   └── <Recurso>.java
    │   │   └── repository/
    │   │       └── <Recurso>Repository.java
    │   └── resources/
    │       ├── application.yml
    │       └── data/
    │           └── <recurso>_<id>.json
    └── test/
        └── ...
```

## Reglas de implementación

- Java 21 y Maven salvo que el proyecto indique otra cosa.
- Usa `record` para DTOs inmutables cuando sea posible.
- Inyección por constructor, sin campos anotados con `@Autowired`.
- Controladores delgados: validan, delegan y devuelven el resultado.
- La capa de repositorio encapsula el origen de datos.
- No se realizan llamadas externas si el servicio debe devolver datos locales.
- No se devuelven campos adicionales ni envoltorios no definidos en el contrato.
- No se crean tests salvo petición expresa.
- No se ejecutan Maven, servidores ni comandos de validación salvo petición expresa.

## Contrato

El DTO debe declarar exactamente los campos del contrato JSON compartido:

```java
public record Recurso(
        int campoNumerico,
        String campoTexto
) {
}
```

Configura Jackson para rechazar propiedades desconocidas cuando el contrato lo exija.
Mantén los nombres JSON alineados con `contracts/`.

## Configuración

- Puerto propio del servicio, documentado en su README.
- Sin secretos en el repositorio.
- Configuración mediante `application.yml` y variables de entorno.
- No añadas Spring Security, bases de datos ni mensajería sin petición expresa.

## Ejecución documentada

```bash
mvn spring-boot:run
```

Documenta los comandos en el README del servicio. No los ejecutes salvo que se solicite.
