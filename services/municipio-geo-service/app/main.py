"""Punto de entrada de la aplicación FastAPI."""

from fastapi import FastAPI

from app.api.municipio_geo import router as municipio_geo_router


def create_app() -> FastAPI:
    """Crea y configura la aplicación FastAPI."""
    application = FastAPI(
        title="Municipio Geo Service",
        version="0.1.0",
        description="Microservicio de datos geográficos de municipios vía AEMET.",
    )
    application.include_router(municipio_geo_router)
    return application


app = create_app()
