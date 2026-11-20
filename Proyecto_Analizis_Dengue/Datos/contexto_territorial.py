"""Reúne observaciones territoriales, sin calcular riesgo o diagnóstico."""

from datetime import date, datetime, timezone
from typing import Any, Mapping

from apis.db import (
    guardar_clima_local,
    guardar_vigilancia_municipal,
    obtener_clima_local,
    obtener_contexto_paciente,
    obtener_geografia_municipio,
    obtener_vigilancia_municipal,
)
from Datos.configuracion_fuentes import fuentes_para_municipio
from Datos.proveedores.contratos import ErrorFuenteExterna
from Datos.registro_proveedores import (
    obtener_proveedor_climatico,
    obtener_proveedor_epidemiologico,
)


def _contexto_no_disponible(estado: str, detalle: str) -> dict[str, Any]:
    return {"estado": estado, "detalle": detalle, "datos": None}


def obtener_contexto_territorial(
    *,
    ubicacion: Mapping[str, Any] | None = None,
    id_paciente: int | None = None,
    fecha_referencia: str | None = None,
) -> dict[str, Any]:
    if id_paciente is not None:
        paciente = obtener_contexto_paciente(id_paciente)
        if paciente is None:
            raise LookupError(f"No existe el paciente local {id_paciente}.")
        ubicacion_paciente = {
            "codigo_municipio": paciente.get("codigo_municipio"),
            "municipio": paciente.get("municipio"),
            "departamento": paciente.get("departamento"),
        }
        fecha_referencia = (
            fecha_referencia
            or paciente.get("fecha_consulta")
            or date.today().isoformat()
        )
    else:
        ubicacion_paciente = dict(ubicacion or {})
        fecha_referencia = fecha_referencia or date.today().isoformat()

    try:
        fecha_referencia = date.fromisoformat(fecha_referencia).isoformat()
    except ValueError as error:
        raise ValueError(
            "fecha_referencia debe tener formato YYYY-MM-DD."
        ) from error

    codigo_municipio = ubicacion_paciente.get("codigo_municipio")
    municipio = ubicacion_paciente.get("municipio")
    departamento = ubicacion_paciente.get("departamento")
    geografia = obtener_geografia_municipio(
        municipio=municipio,
        departamento=departamento,
        codigo_municipio=codigo_municipio,
    )
    if geografia is None:
        return {
            "fecha_referencia": fecha_referencia,
            "clima": _contexto_no_disponible(
                "sin_coordenadas_locales",
                "Registre en historico.db el código DANE y coordenadas "
                "verificadas del municipio.",
            ),
            "vigilancia_dengue": _contexto_no_disponible(
                "sin_fuente_configurada",
                "No se configuró una fuente agregada de vigilancia para "
                "este municipio.",
            ),
        }

    codigo_municipio = geografia.get("codigo_municipio")
    if not codigo_municipio:
        return {
            "fecha_referencia": fecha_referencia,
            "clima": _contexto_no_disponible(
                "sin_codigo_municipal",
                "La ubicación local no tiene código DANE para seleccionar "
                "fuentes regionales.",
            ),
            "vigilancia_dengue": _contexto_no_disponible(
                "sin_codigo_municipal",
                "La ubicación local no tiene código DANE para seleccionar "
                "fuentes regionales.",
            ),
        }

    fuentes = fuentes_para_municipio(str(codigo_municipio))
    clima = obtener_observacion_climatica(
        fuente=fuentes["clima"],
        geografia=geografia,
        fecha_referencia=fecha_referencia,
    )
    vigilancia = _obtener_contexto_vigilancia(
        fuente=fuentes["epidemiologia"],
        codigo_municipio=str(codigo_municipio),
        fecha_referencia=fecha_referencia,
    )

    return {
        "municipio": geografia.get("municipio"),
        "departamento": geografia.get("departamento"),
        "codigo_municipio": codigo_municipio,
        "fecha_referencia": fecha_referencia,
        "clima": clima,
        "vigilancia_dengue": vigilancia,
        "interpretacion": (
            "Datos contextuales territoriales; no determinan infección, "
            "gravedad ni un caso activo en la persona."
        ),
    }


def obtener_observacion_climatica(
    *,
    fuente: str | None,
    geografia: Mapping[str, Any],
    fecha_referencia: str,
) -> dict[str, Any]:
    latitud = geografia.get("latitud")
    longitud = geografia.get("longitud")
    codigo_municipio = str(geografia["codigo_municipio"])
    if latitud is None or longitud is None:
        return _contexto_no_disponible(
            "sin_coordenadas",
            "El municipio no tiene coordenadas locales verificadas.",
        )
    if fuente is None:
        return _contexto_no_disponible(
            "sin_fuente_configurada",
            "No se configuró una fuente climática para el municipio.",
        )

    observacion = obtener_clima_local(codigo_municipio, fecha_referencia)
    if observacion is not None:
        return {"estado": "observacion_local", "datos": observacion}

    proveedor = obtener_proveedor_climatico(fuente)
    try:
        datos = proveedor.obtener_observacion(
            latitud=float(latitud),
            longitud=float(longitud),
            fecha=fecha_referencia,
        )
    except ErrorFuenteExterna as error:
        return _contexto_no_disponible("fuente_externa_no_disponible", str(error))

    registro = {
        "codigo_municipio": codigo_municipio,
        "departamento": geografia.get("departamento") or "",
        "municipio": geografia.get("municipio") or "",
        "fecha_referencia": fecha_referencia,
        "temperatura_media": datos["temperatura_media"],
        "humedad": datos["humedad"],
        "precipitacion": datos["precipitacion"],
        "fuente": datos["fuente"],
        "fecha_consulta_utc": datetime.now(timezone.utc).isoformat(),
    }
    guardar_clima_local(registro)
    return {
        "estado": "observacion_externa",
        "datos": {
            **registro,
            "unidades": datos["unidades"],
            "tiempo_fuente": datos["tiempo_fuente"],
            "latitud": datos["latitud"],
            "longitud": datos["longitud"],
            "fuente_coordenadas": geografia.get("fuente_coordenadas"),
            "fecha_verificacion_coordenadas": geografia.get(
                "fecha_verificacion"
            ),
        },
    }


def _obtener_contexto_vigilancia(
    *,
    fuente: str | None,
    codigo_municipio: str,
    fecha_referencia: str,
) -> dict[str, Any]:
    observacion = obtener_vigilancia_municipal(
        codigo_municipio,
        fecha_referencia,
    )
    if observacion is not None:
        return {"estado": "indicador_agregado_local", "datos": observacion}
    if fuente is None:
        return _contexto_no_disponible(
            "sin_fuente_configurada",
            "No hay una fuente vigente de vigilancia configurada para "
            "este municipio; no se puede afirmar si existe un caso activo.",
        )

    try:
        proveedor = obtener_proveedor_epidemiologico(fuente)
        datos = proveedor.obtener_indicadores(
            codigo_municipio=codigo_municipio,
            fecha=fecha_referencia,
        )
    except (ErrorFuenteExterna, ValueError) as error:
        return _contexto_no_disponible(
            "fuente_epidemiologica_no_disponible",
            str(error),
        )

    datos["fecha_consulta_utc"] = datetime.now(timezone.utc).isoformat()
    guardar_vigilancia_municipal(datos)
    return {"estado": "indicador_agregado_externo", "datos": datos}
