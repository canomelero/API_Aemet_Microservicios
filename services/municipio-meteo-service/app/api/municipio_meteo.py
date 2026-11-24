"""Endpoints de datos meteorológicos de municipios."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.clients.aemet_client import (
    AemetClient,
    AemetNotConfiguredError,
    AemetNotFoundError,
    AemetTimeoutError,
    AemetUpstreamError,
)
from app.config import AEMET_API_KEY, MUNICIPIO_ID
from app.models.municipio_meteo import MunicipioMeteo
from app.repositories.municipio_meteo_repository import MunicipioMeteoRepository

router = APIRouter(tags=["municipios"])


def get_aemet_client() -> AemetClient:
    """Proporciona un cliente de AEMET con la clave del archivo config."""
    return AemetClient(api_key=AEMET_API_KEY)


def get_municipio_meteo_repository(
    client: AemetClient = Depends(get_aemet_client),
) -> MunicipioMeteoRepository:
    """Proporciona el repositorio de datos meteorológicos."""
    return MunicipioMeteoRepository(client)


@router.get(
    "/granada/meteo",
    response_model=MunicipioMeteo,
    status_code=status.HTTP_200_OK,
    summary="Devuelve los datos meteorológicos del municipio de Granada",
    description=(
        "Consulta AEMET OpenData y devuelve la temperatura, humedad, viento, "
        "precipitación y estado del cielo del municipio con id 18087."
    ),
)
def get_municipio_meteo(
    repository: MunicipioMeteoRepository = Depends(get_municipio_meteo_repository),
) -> MunicipioMeteo:
    """Devuelve los datos meteorológicos de Granada desde AEMET."""
    try:
        return repository.get_by_id(MUNICIPIO_ID)
    except AemetNotConfiguredError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AEMET_API_KEY no configurada",
        ) from exc
    except AemetNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Municipio no encontrado en AEMET",
        ) from exc
    except AemetTimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Tiempo de espera agotado al consultar AEMET",
        ) from exc
    except AemetUpstreamError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AEMET ha devuelto una respuesta no válida",
        ) from exc
