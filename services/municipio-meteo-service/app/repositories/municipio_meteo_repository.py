"""Acceso a la predicción diaria de municipios en AEMET."""

from datetime import date, datetime
from typing import Any
from zoneinfo import ZoneInfo

from app.clients.aemet_client import AemetClient, AemetUpstreamError
from app.models.municipio_meteo import MunicipioMeteo, Temperaturas

_TIMEZONE = ZoneInfo("Europe/Madrid")


class MunicipioMeteoRepository:
    """Repositorio que normaliza la predicción de AEMET al contrato."""

    def __init__(self, client: AemetClient) -> None:
        self._client = client

    def get_by_id(self, municipio_id: int) -> MunicipioMeteo:
        """Devuelve los datos meteorológicos del municipio indicado."""
        raw_data = self._client.get_prediccion_diaria(municipio_id)
        municipio = self._to_model(raw_data, datetime.now(_TIMEZONE))
        if municipio.municipioid != municipio_id:
            raise AemetUpstreamError(
                "AEMET ha devuelto un municipio distinto del solicitado"
            )
        return municipio

    def _to_model(self, raw_data: Any, current: datetime) -> MunicipioMeteo:
        prediccion = _first_dict(raw_data)

        try:
            dia = _select_day(prediccion["prediccion"]["dia"], current.date())
            temperatura = dia["temperatura"]

            return MunicipioMeteo(
                municipioid=_parse_municipio_id(prediccion["id"]),
                temperatura_actual=_text(
                    _closest_value(temperatura["dato"], current.hour)
                ),
                temperaturas=Temperaturas(
                    max=_text(temperatura["maxima"]),
                    min=_text(temperatura["minima"]),
                ),
                humedad=_text(
                    _closest_value(dia["humedadRelativa"]["dato"], current.hour)
                ),
                viento=_format_wind(_select_period(dia["viento"], current.hour)),
                precipitacion=_text(
                    _select_period(dia["probPrecipitacion"], current.hour)["value"]
                ),
                estadocielo=_select_sky(dia["estadoCielo"], current.hour),
            )
        except (KeyError, TypeError, ValueError, IndexError) as exc:
            raise AemetUpstreamError(
                "La respuesta de AEMET no contiene datos meteorológicos válidos"
            ) from exc


def _first_dict(raw_data: Any) -> dict[str, Any]:
    if isinstance(raw_data, list):
        if not raw_data:
            raise AemetUpstreamError("AEMET ha devuelto una lista vacía")
        raw_data = raw_data[0]
    if not isinstance(raw_data, dict):
        raise AemetUpstreamError("La respuesta de AEMET no es un objeto JSON")
    return raw_data


def _parse_municipio_id(raw_id: Any) -> int:
    value = str(raw_id).strip()
    if value.startswith("id"):
        value = value.removeprefix("id")
    return int(value)


def _select_day(dias: list[dict[str, Any]], today: date) -> dict[str, Any]:
    if not dias:
        raise ValueError("AEMET no devuelve días de predicción")

    for dia in dias:
        if _parse_date(dia.get("fecha")) == today:
            return dia
    return dias[0]


def _parse_date(value: Any) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value)).date()
    except ValueError:
        return None


def _closest_value(entries: list[dict[str, Any]], hour: int) -> Any:
    valid_entries = [
        entry for entry in entries if entry.get("value") not in (None, "")
    ]
    if not valid_entries:
        raise ValueError("AEMET no devuelve valores horarios")

    closest = min(valid_entries, key=lambda entry: abs(int(entry["hora"]) - hour))
    return closest["value"]


def _select_period(entries: list[dict[str, Any]], hour: int) -> dict[str, Any]:
    selected: dict[str, Any] | None = None
    selected_key: tuple[int, int] | None = None

    for entry in entries:
        period = _parse_period(entry.get("periodo"))
        if period is None:
            continue
        start, end = period
        if not _hour_in_period(start, end, hour):
            continue
        key = (start, -end)
        if selected_key is None or key > selected_key:
            selected = entry
            selected_key = key

    if selected is None:
        raise ValueError("AEMET no devuelve datos para la hora actual")
    return selected


def _parse_period(value: Any) -> tuple[int, int] | None:
    if not isinstance(value, str) or "-" not in value:
        return None
    start, end = value.split("-", 1)
    try:
        return int(start), int(end)
    except ValueError:
        return None


def _hour_in_period(start: int, end: int, hour: int) -> bool:
    return start <= hour < end


def _select_sky(entries: list[dict[str, Any]], hour: int) -> str:
    selected: str | None = None
    selected_key: tuple[int, int] | None = None

    for entry in entries:
        description = str(entry.get("descripcion") or "").strip()
        period = _parse_period(entry.get("periodo"))
        if not description or period is None:
            continue
        start, end = period
        if not _hour_in_period(start, end, hour):
            continue
        key = (start, -end)
        if selected_key is None or key > selected_key:
            selected = description
            selected_key = key

    if selected is not None:
        return selected

    for entry in entries:
        description = str(entry.get("descripcion") or "").strip()
        if description:
            return description

    raise ValueError("AEMET no devuelve el estado del cielo")


def _format_wind(entry: dict[str, Any]) -> str:
    direction = str(entry.get("direccion") or "").strip()
    speed = _text(entry.get("velocidad"))
    if direction:
        return f"{direction} {speed}"
    return speed


def _text(value: Any) -> str:
    if value in (None, ""):
        raise ValueError("AEMET devuelve un valor vacío")
    if isinstance(value, bool):
        raise ValueError("AEMET devuelve un valor booleano no válido")
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return str(value).strip()
