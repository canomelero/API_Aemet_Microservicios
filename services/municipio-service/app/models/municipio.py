"""Contrato de datos de un municipio."""

from pydantic import BaseModel, ConfigDict


class Municipio(BaseModel):
    """Municipio conforme a ``contracts/municipio.schema.json``."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    municipioid: int
    gentilicio: str
    sitioweb: str
    provincia: str
