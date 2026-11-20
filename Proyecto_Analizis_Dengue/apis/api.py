from typing import Any

from fastapi import FastAPI, HTTPException

from apis.db import obtener_contexto_paciente, obtener_datos_clinicos
from Datos.contexto_territorial import obtener_contexto_territorial
from modelos.Analizador import analizar_paciente


app = FastAPI(
    title="Sistema experimental de apoyo para dengue",
    version="2.0",
    description=(
        "Hallazgos y contexto territorial. No es una herramienta diagnóstica."
    ),
)


@app.get("/")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "sistema": "Analizis Dengue",
        "modo": "local_con_enriquecimiento_externo_opcional",
    }


@app.post("/evaluar")
def evaluar(datos: dict[str, Any]) -> dict[str, Any]:
    try:
        id_paciente = datos.get("id_paciente")
        ubicacion = datos.get("ubicacion")
        tiene_datos_clinicos = any(
            campo in datos
            for campo in ("sintomas", "laboratorios", "alarmas")
        )

        if id_paciente is not None:
            if isinstance(id_paciente, bool) or not isinstance(id_paciente, int):
                raise ValueError("id_paciente debe ser un entero.")
            if tiene_datos_clinicos:
                raise ValueError(
                    "Envíe id_paciente para leer datos locales o datos clínicos "
                    "en el JSON, pero no ambos."
                )
            paciente = obtener_contexto_paciente(id_paciente)
            if paciente is None:
                raise HTTPException(
                    status_code=404,
                    detail="El paciente no existe en la base local.",
                )
            resultado = analizar_paciente(
                obtener_datos_clinicos(id_paciente)
            )
            resultado["origen_datos_clinicos"] = "base_local"
            resultado["contexto_zona"] = obtener_contexto_territorial(
                id_paciente=id_paciente,
                fecha_referencia=datos.get("fecha_referencia"),
            )
            return resultado

        if ubicacion is not None and not isinstance(ubicacion, dict):
            raise ValueError("ubicacion debe ser un objeto JSON.")

        resultado = analizar_paciente(datos)
        if ubicacion is not None:
            resultado["contexto_zona"] = obtener_contexto_territorial(
                ubicacion=ubicacion,
                fecha_referencia=datos.get("fecha_referencia"),
            )
        return resultado
    except HTTPException:
        raise
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error