"""Acceso a los datos locales de municipios."""

import json
from pathlib import Path

from app.models.municipio import Municipio

_DEFAULT_DATA_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "municipio_18087.json"
)


class MunicipioRepository:
    """Repositorio de municipios respaldado por un JSON local.

    La capa HTTP no conoce el origen de los datos. Si en el futuro se
    sustituye el JSON por una base de datos o una API externa, basta con
    proporcionar otra implementación de este repositorio.
    """

    def __init__(self, data_path: Path | None = None) -> None:
        self._data_path = data_path or _DEFAULT_DATA_PATH
        self._municipio: Municipio | None = None

    def get_by_id(self, municipio_id: int) -> Municipio | None:
        """Devuelve el municipio con el identificador indicado, si existe."""
        municipio = self._get_municipio()
        if municipio.municipioid != municipio_id:
            return None
        return municipio

    def _get_municipio(self) -> Municipio:
        if self._municipio is None:
            self._municipio = self._load()
        return self._municipio

    def _load(self) -> Municipio:
        with self._data_path.open(encoding="utf-8") as data_file:
            raw_data = json.load(data_file)
        return Municipio.model_validate(raw_data)
