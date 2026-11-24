"""Punto de entrada de la aplicación FastAPI."""

from fastapi import FastAPI

from app.api.municipio_meteo import router as municipio_meteo_router


def create_app() -> FastAPI:
    """Crea y configura la aplicación FastAPI."""
    application = FastAPI(
        title="Municipio Meteo Service",
        version="0.1.0",
        description="Microservicio de datos meteorológicos de municipios vía AEMET.",
    )
    application.include_router(municipio_meteo_router)
    return application


app = create_app()
