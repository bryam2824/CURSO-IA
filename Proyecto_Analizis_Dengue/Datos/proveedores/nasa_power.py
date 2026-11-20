"""Adaptador diario de NASA POWER; no envía datos del paciente."""

import json
import math
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from typing import Any

from Datos.proveedores.contratos import ErrorFuenteExterna


NOMBRE_FUENTE = "NASA POWER"
_ENDPOINT = "https://power.larc.nasa.gov/api/temporal/daily/point"
_PARAMETROS = {
    "T2M": "temperatura_media",
    "RH2M": "humedad",
    "PRECTOTCORR": "precipitacion",
}
_UNIDADES = {
    "temperatura_media": "C",
    "humedad": "%",
    "precipitacion": "mm/day",
}


def obtener_observacion(
    *,
    latitud: float,
    longitud: float,
    fecha: str,
) -> dict[str, Any]:
    try:
        fecha_objeto = date.fromisoformat(fecha)
    except ValueError as error:
        raise ValueError("fecha debe tener formato YYYY-MM-DD.") from error

    if not math.isfinite(latitud) or not -90 <= latitud <= 90:
        raise ValueError("latitud debe estar entre -90 y 90.")
    if not math.isfinite(longitud) or not -180 <= longitud <= 180:
        raise ValueError("longitud debe estar entre -180 y 180.")

    fecha_api = fecha_objeto.strftime("%Y%m%d")
    query = urlencode({
        "parameters": ",".join(_PARAMETROS),
        "community": "RE",
        "longitude": longitud,
        "latitude": latitud,
        "start": fecha_api,
        "end": fecha_api,
        "format": "JSON",
    })
    url = f"{_ENDPOINT}?{query}"
    solicitud = Request(
        url,
        headers={"User-Agent": "CURSO-IA-Dengue/1.0 (public-health research)"},
    )

    try:
        with urlopen(solicitud, timeout=20) as respuesta:
            contenido = json.loads(respuesta.read().decode("utf-8"))
    except HTTPError as error:
        raise ErrorFuenteExterna(
            f"{NOMBRE_FUENTE} respondió HTTP {error.code}."
        ) from error
    except (URLError, TimeoutError) as error:
        raise ErrorFuenteExterna(
            f"No fue posible consultar {NOMBRE_FUENTE}: {error}."
        ) from error
    except json.JSONDecodeError as error:
        raise ErrorFuenteExterna(
            f"{NOMBRE_FUENTE} devolvió una respuesta JSON inválida."
        ) from error

    try:
        propiedades = contenido["properties"]
        parametros = propiedades["parameter"]
        cabecera = contenido["header"]
        valores = {
            destino: float(parametros[codigo][fecha_api])
            for codigo, destino in _PARAMETROS.items()
        }
        valores_unidades = {
            destino: contenido["parameters"][codigo]["units"]
            for codigo, destino in _PARAMETROS.items()
        }
    except (KeyError, TypeError, ValueError) as error:
        raise ErrorFuenteExterna(
            f"La respuesta de {NOMBRE_FUENTE} no contiene los campos esperados."
        ) from error

    fill_value = float(cabecera.get("fill_value", -999.0))
    if any(not math.isfinite(valor) or valor == fill_value for valor in valores.values()):
        raise ErrorFuenteExterna(
            f"{NOMBRE_FUENTE} no tiene observaciones completas para {fecha}."
        )
    if valores_unidades != _UNIDADES:
        raise ErrorFuenteExterna(
            f"Las unidades devueltas por {NOMBRE_FUENTE} cambiaron: "
            f"{valores_unidades}."
        )

    return {
        **valores,
        "fecha_referencia": fecha,
        "latitud": latitud,
        "longitud": longitud,
        "fuente": NOMBRE_FUENTE,
        "unidades": valores_unidades,
        "tiempo_fuente": cabecera.get("time_standard"),
    }
