# Datos/variables_climaticas.py

"""Obtiene clima de NASA POWER usando coordenadas locales verificadas."""

from typing import Any

from apis.db import obtener_geografia_municipio
from Datos.configuracion_fuentes import fuentes_para_municipio
from Datos.contexto_territorial import obtener_observacion_climatica
from Datos.proveedores.contratos import ErrorFuenteExterna


def obtener_clima_historico(
    municipio: str,
    fecha: str,
    *,
    departamento: str | None = None,
    codigo_municipio: str | None = None,
) -> dict[str, Any]:
    """Obtiene el registro local o consulta el proveedor elegido para el DANE."""
    geografia = obtener_geografia_municipio(
        municipio=municipio,
        departamento=departamento,
        codigo_municipio=codigo_municipio,
    )
    if geografia is None:
        raise ErrorFuenteExterna(
            "No existe una coordenada local verificada para el municipio."
        )

    codigo = geografia.get("codigo_municipio")
    if not codigo:
        raise ErrorFuenteExterna(
            "La ubicación no tiene código DANE para seleccionar el proveedor."
        )

    fuentes = fuentes_para_municipio(str(codigo))
    resultado = obtener_observacion_climatica(
        fuente=fuentes["clima"],
        geografia=geografia,
        fecha_referencia=fecha,
    )
    if resultado.get("datos") is None:
        raise ErrorFuenteExterna(str(resultado.get("detalle")))

    return resultado["datos"]
