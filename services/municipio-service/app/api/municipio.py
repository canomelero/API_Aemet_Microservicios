"""Endpoints del recurso municipio."""

from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.municipio import Municipio
from app.repositories.municipio_repository import MunicipioRepository

MUNICIPIO_ID = 18087

router = APIRouter(tags=["municipios"])


@lru_cache
def get_municipio_repository() -> MunicipioRepository:
    """Proporciona una única instancia del repositorio para la aplicación."""
    return MunicipioRepository()


@router.get(
    "/granada",
    response_model=Municipio,
    status_code=status.HTTP_200_OK,
    summary="Devuelve el municipio de Granada",
    description="Devuelve los datos locales del municipio con id 18087.",
)
def get_municipio(
    repository: MunicipioRepository = Depends(get_municipio_repository),
) -> Municipio:
    """Devuelve el municipio de Granada sin realizar llamadas externas."""
    municipio = repository.get_by_id(MUNICIPIO_ID)
    if municipio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Municipio no encontrado",
        )
    return municipio
