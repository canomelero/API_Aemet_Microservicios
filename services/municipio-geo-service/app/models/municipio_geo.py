"""Contrato de datos geográficos de un municipio."""

from pydantic import BaseModel, ConfigDict


class MunicipioGeo(BaseModel):
    """Datos geográficos conforme a ``contracts/json_schema_municipio_geo.json``."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    municipioid: int
    latitud: float
    longitud: float
    altitud: float
