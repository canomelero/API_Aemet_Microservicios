"""Contrato de datos meteorológicos de un municipio."""

from pydantic import BaseModel, ConfigDict


class Temperaturas(BaseModel):
    """Temperaturas máxima y mínima del día."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    max: str
    min: str


class MunicipioMeteo(BaseModel):
    """Datos meteorológicos conforme a ``contracts/json_schema_municipio_meteo.json``."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    municipioid: int
    temperatura_actual: str
    temperaturas: Temperaturas
    humedad: str
    viento: str
    precipitacion: str
    estadocielo: str
