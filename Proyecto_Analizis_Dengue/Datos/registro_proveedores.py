"""Registro de adaptadores externos disponibles en esta instalación."""

from Datos.proveedores import nasa_power
from Datos.proveedores.contratos import (
    ProveedorClimatico,
    ProveedorEpidemiologico,
)


PROVEEDORES_CLIMATICOS: dict[str, ProveedorClimatico] = {
    "nasa_power": nasa_power,
}

PROVEEDORES_EPIDEMIOLOGICOS: dict[str, ProveedorEpidemiologico] = {}


def obtener_proveedor_climatico(nombre: str) -> ProveedorClimatico:
    try:
        return PROVEEDORES_CLIMATICOS[nombre]
    except KeyError as error:
        raise ValueError(
            f"No está registrado el proveedor climático '{nombre}'."
        ) from error


def obtener_proveedor_epidemiologico(nombre: str) -> ProveedorEpidemiologico:
    try:
        return PROVEEDORES_EPIDEMIOLOGICOS[nombre]
    except KeyError as error:
        raise ValueError(
            f"No está registrado el proveedor epidemiológico '{nombre}'."
        ) from error
