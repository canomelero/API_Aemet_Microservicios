---
name: SOLID and Best Practices
description: Principios SOLID, código limpio y buenas prácticas aplicadas a servicios Python/FastAPI y Java/Spring Boot, con criterio pragmático.
---

# SOLID and Best Practices

Usa esta skill al diseñar, implementar o revisar cualquier servicio del repositorio.

## Principios SOLID

### S — Single Responsibility

Cada módulo, clase o función debe tener una sola razón para cambiar.

- Un modelo describe el contrato.
- Un repositorio accede a datos.
- Un controlador gestiona HTTP.
- La configuración de la aplicación se concentra en `main.py` o en la clase de arranque.

Evita clases que mezclen validación, acceso a datos, lógica de negocio y presentación.

### O — Open/Closed

El código debe poder extenderse sin modificar lo que ya funciona.

- Añade nuevas implementaciones de repositorio en lugar de llenar el controlador de condicionales.
- Usa composición antes que cadenas de `if/else` sobre tipos.
- No introduzcas abstracciones hasta que exista una variación real.

### L — Liskov Substitution

Cualquier implementación de una abstracción debe poder sustituir a otra sin romper el contrato.

- Respeta los tipos de entrada y salida.
- No lances excepciones nuevas e incompatibles en una implementación.
- No devuelvas `None` donde el contrato promete un valor.

### I — Interface Segregation

Es mejor varias interfaces pequeñas que una interfaz genérica.

- Los repositorios exponen solo las operaciones que el servicio necesita.
- Los DTOs representan un caso de uso concreto.
- No obligues a implementar métodos que no se usan.

### D — Dependency Inversion

Los módulos de alto nivel dependen de abstracciones, no de detalles.

- El controlador depende de una interfaz o contrato de repositorio.
- La implementación concreta (JSON local, base de datos, API) se inyecta.
- En Python usa `Depends` y funciones factoría.
- En Java usa inyección por constructor.

## Buenas prácticas generales

- Nombres descriptivos y en el idioma del dominio.
- Funciones pequeñas con una responsabilidad clara.
- Type hints en Python y tipos explícitos en Java.
- Sin estado global mutable.
- Sin números o cadenas mágicas; usa constantes con nombre.
- Errores explícitos y códigos HTTP coherentes.
- Dependencias mínimas y con rangos de versión.
- Sin secretos en el repositorio.
- Sin duplicación de contratos ni de lógica.
- Documentación breve junto al código y en el README.
- No añadas patrones, capas o interfaces solo por apariencia.

## Criterio pragmático

SOLID no significa crear una interfaz para cada clase. Aplica abstracciones cuando:

1. Existe o se espera una segunda implementación real.
2. Hay un límite claro del sistema (HTTP, persistencia, API externa).
3. La abstracción mejora la sustitución en pruebas o la claridad.

En este repositorio, el repositorio de municipios es un límite válido porque el origen de datos puede pasar de JSON local a AEMET o a una base de datos.

## Python/FastAPI

- PEP 8 y nombres en `snake_case`.
- Modelos Pydantic inmutables con `extra="forbid"` cuando representen contratos.
- Repositorios con una única responsabilidad.
- Dependencias inyectadas con `Depends`.
- `create_app()` como factoría de la aplicación.
- Sin lógica de negocio en los endpoints.
- No usar `requests` o `httpx` en servicios que deben devolver datos locales.

## Java/Spring Boot

- Paquetes por funcionalidad cuando el servicio crezca.
- DTOs inmutables con `record`.
- Inyección por constructor.
- Controladores delgados.
- Servicios y repositorios con responsabilidades separadas.
- Excepciones claras y mapeadas a códigos HTTP.
- Sin `@Autowired` en campos.
- Sin lógica de negocio en el controlador.

## Lista de comprobación antes de terminar

- [ ] Cada clase y función tiene una responsabilidad clara.
- [ ] El contrato JSON se respeta exactamente.
- [ ] No hay campos ni envoltorios adicionales.
- [ ] Las dependencias se inyectan, no se construyen dentro del controlador.
- [ ] No hay estado global mutable innecesario.
- [ ] Los nombres son descriptivos.
- [ ] No hay duplicación de contrato ni de lógica.
- [ ] No se han añadido dependencias, tests, ejecuciones ni infraestructura no solicitados.
- [ ] El README documenta lo necesario para ejecutar el servicio.
