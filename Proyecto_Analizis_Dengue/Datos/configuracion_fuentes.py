"""Selección de fuentes por código DANE, sin acoplarla a las rutas de la API."""

import json
from pathlib import Path
from typing import Any


_CONFIG_PATH = Path(__file__).with_name("configuracion_fuentes.json")


def fuentes_para_municipio(codigo_municipio: str) -> dict[str, str | None]:
    configuracion: Any = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(configuracion, dict) or configuracion.get("version") != 1:
        raise ValueError("La configuración de fuentes debe usar version 1.")

    por_defecto = configuracion.get("default")
    por_municipio = configuracion.get("municipios")
    if not isinstance(por_defecto, dict) or not isinstance(por_municipio, dict):
        raise ValueError("La configuración de fuentes tiene una estructura inválida.")

    seleccion = por_municipio.get(codigo_municipio, {})
    if not isinstance(seleccion, dict):
        raise ValueError(
            f"La configuración para el municipio {codigo_municipio} no es válida."
        )

    resultado = {
        "clima": seleccion.get("clima", por_defecto.get("clima")),
        "epidemiologia": seleccion.get(
            "epidemiologia",
            por_defecto.get("epidemiologia"),
        ),
    }
    if any(value is not None and not isinstance(value, str) for value in resultado.values()):
        raise ValueError(
            f"Los proveedores del municipio {codigo_municipio} deben ser nombres o null."
        )
    return resultado
