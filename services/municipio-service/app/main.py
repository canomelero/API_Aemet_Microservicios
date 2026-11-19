"""Punto de entrada de la aplicación FastAPI."""

from fastapi import FastAPI

from app.api.municipio import router as municipio_router


def create_app() -> FastAPI:
    """Crea y configura la aplicación FastAPI."""
    application = FastAPI(
        title="Municipio Service",
        version="0.1.0",
        description="Microservicio de consulta de municipios.",
    )
    application.include_router(municipio_router)
    return application


app = create_app()
