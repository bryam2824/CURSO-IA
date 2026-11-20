"""Contratos que debe cumplir cada adaptador de fuente externa."""

from typing import Any, Protocol


class ErrorFuenteExterna(RuntimeError):
    """Error explícito al consultar o validar una fuente externa."""


class ProveedorClimatico(Protocol):
    nombre: str

    def obtener_observacion(
        self,
        *,
        latitud: float,
        longitud: float,
        fecha: str,
    ) -> dict[str, Any]:
        """Devuelve una observación diaria con fuente y unidades."""


class ProveedorEpidemiologico(Protocol):
    nombre: str

    def obtener_indicadores(
        self,
        *,
        codigo_municipio: str,
        fecha: str,
    ) -> dict[str, Any]:
        """Devuelve solo indicadores agregados para un municipio y periodo."""
