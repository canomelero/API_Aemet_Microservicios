"""Acceso a los datos geográficos de municipios en AEMET."""

import re
from typing import Any

from app.clients.aemet_client import AemetClient, AemetUpstreamError
from app.models.municipio_geo import MunicipioGeo

_DMS_PATTERN = re.compile(
    r"^(?P<sign>[+-])?(?P<degrees>\d+)[º°]"
    r"(?P<minutes>\d+)['′]"
    r'(?P<seconds>\d+(?:\.\d+)?)["″]$'
)


class MunicipioGeoRepository:
    """Repositorio que normaliza la información de AEMET al contrato."""

    def __init__(self, client: AemetClient) -> None:
        self._client = client

    def get_by_id(self, municipio_id: int) -> MunicipioGeo:
        """Devuelve los datos geográficos del municipio indicado."""
        raw_data = self._client.get_municipio(municipio_id)
        municipio = self._to_model(raw_data)
        if municipio.municipioid != municipio_id:
            raise AemetUpstreamError(
                "AEMET ha devuelto un municipio distinto del solicitado"
            )
        return municipio

    def _to_model(self, raw_data: Any) -> MunicipioGeo:
        if isinstance(raw_data, list):
            if not raw_data:
                raise AemetUpstreamError("AEMET ha devuelto una lista vacía")
            raw_data = raw_data[0]
        if not isinstance(raw_data, dict):
            raise AemetUpstreamError("La respuesta de AEMET no es un objeto JSON")

        try:
            return MunicipioGeo(
                municipioid=_parse_municipio_id(raw_data["id"]),
                latitud=_parse_coordinate(raw_data, "latitud_dec", "latitud"),
                longitud=_parse_coordinate(raw_data, "longitud_dec", "longitud"),
                altitud=float(raw_data["altitud"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise AemetUpstreamError(
                "La respuesta de AEMET no contiene datos geográficos válidos"
            ) from exc


def _parse_municipio_id(raw_id: Any) -> int:
    value = str(raw_id).strip()
    if value.startswith("id"):
        value = value.removeprefix("id")
    return int(value)


def _parse_coordinate(
    raw_data: dict[str, Any],
    decimal_key: str,
    dms_key: str,
) -> float:
    decimal_value = raw_data.get(decimal_key)
    if decimal_value not in (None, ""):
        return float(decimal_value)
    return _parse_dms(str(raw_data[dms_key]))


def _parse_dms(value: str) -> float:
    match = _DMS_PATTERN.match(value.strip())
    if match is None:
        raise ValueError(f"Coordenada DMS inválida: {value}")

    degrees = float(match.group("degrees"))
    minutes = float(match.group("minutes"))
    seconds = float(match.group("seconds"))
    sign = -1.0 if match.group("sign") == "-" else 1.0
    return sign * (degrees + minutes / 60 + seconds / 3600)
