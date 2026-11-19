"""Cliente HTTP para la API OpenData de AEMET."""

from typing import Any

import httpx

from app.config import AEMET_BASE_URL, AEMET_TIMEOUT_SECONDS, AEMET_API_KEY

_MUNICIPIO_PATH = "/maestro/municipio"
_AEMET_ID_PREFIX = "id"


class AemetError(Exception):
    """Error base de la comunicación con AEMET."""


class AemetNotConfiguredError(AemetError):
    """No se ha configurado la clave de AEMET."""


class AemetNotFoundError(AemetError):
    """AEMET no tiene datos para el municipio solicitado."""


class AemetTimeoutError(AemetError):
    """La petición a AEMET ha superado el tiempo de espera."""


class AemetUpstreamError(AemetError):
    """AEMET ha devuelto una respuesta no válida o un error."""


class AemetClient:
    """Cliente de los endpoints de AEMET OpenData."""

    def __init__(
        self,
        api_key: str = AEMET_API_KEY,
        base_url: str = AEMET_BASE_URL,
        timeout: float = AEMET_TIMEOUT_SECONDS,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def get_municipio(self, municipio_id: int) -> Any:
        """Obtiene la información de un municipio siguiendo el sobre de AEMET."""
        if not self._api_key:
            raise AemetNotConfiguredError(
                "La variable de entorno AEMET_API_KEY no está configurada"
            )

        # El endpoint de detalle de AEMET espera el identificador con prefijo.
        url = (
            f"{self._base_url}{_MUNICIPIO_PATH}/"
            f"{_AEMET_ID_PREFIX}{municipio_id}"
        )
        headers = {
            "Accept": "application/json"
        }

        with httpx.Client(
            timeout=self._timeout,
            follow_redirects=True,
            headers=headers,
        ) as client:
            envelope = self._get_json(client, url, {"api_key": self._api_key})
            if not isinstance(envelope, dict):
                raise AemetUpstreamError(
                    "La respuesta inicial de AEMET no es un objeto JSON"
                )

            if envelope.get("estado") == 404:
                raise AemetNotFoundError("AEMET no devuelve datos para el municipio")

            datos_url = envelope.get("datos")
            if not isinstance(datos_url, str) or not datos_url:
                raise AemetUpstreamError(
                    "La respuesta de AEMET no contiene la URL de datos"
                )

            data = self._get_json(client, datos_url)
            if isinstance(data, dict) and data.get("estado") == 404:
                raise AemetNotFoundError("AEMET no devuelve datos para el municipio")
            return data

    def _get_json(
        self,
        client: httpx.Client,
        url: str,
        headers: dict[str, str] | None = None,
    ) -> Any:
        try:
            response = client.get(url, headers=headers)
        except httpx.TimeoutException as exc:
            raise AemetTimeoutError(
                "Tiempo de espera agotado al consultar AEMET"
            ) from exc
        except httpx.HTTPError as exc:
            raise AemetUpstreamError("Error de conexión con AEMET") from exc

        if response.status_code == 404:
            raise AemetNotFoundError("AEMET no devuelve datos para el municipio")
        if response.status_code >= 400:
            raise AemetUpstreamError(
                f"AEMET ha respondido con el código {response.status_code}"
            )

        try:
            return response.json()
        except ValueError as exc:
            raise AemetUpstreamError(
                "La respuesta de AEMET no es JSON válido"
            ) from exc
