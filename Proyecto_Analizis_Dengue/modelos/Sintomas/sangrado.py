# modelos/Sintomas/sangrado.py

from Datos.respuesta_modelo import crear_respuesta
from apis.db import obtener_sangrado_sintoma


TABLA_RIESGO_SANGRADO = {
    "ninguno": 0.0,
    "leve": 0.4,
    "moderado": 0.7,
    "grave": 0.9
}


def clasificar_sangrado(severidad: str) -> tuple:
    """
    Analiza exclusivamente el síntoma sangrado.
    """

    if severidad is None:
        return (
            "sin_dato",
            0.0
        )

    severidad = severidad.lower().strip()

    return (
        severidad,
        TABLA_RIESGO_SANGRADO.get(
            severidad,
            0.0
        )
    )


def evaluar_sangrado(id_paciente: int) -> dict:
    """
    Variable individual.

    Entrada:
    {
        "id_paciente":12345
    }
    """

    severidad = obtener_sangrado_sintoma(
        id_paciente
    )

    categoria, riesgo = clasificar_sangrado(
        severidad
    )

    return crear_respuesta(
        id_paciente=id_paciente,
        variable="sangrado",
        valor=severidad,
        categoria=categoria,
        riesgo=riesgo,
        fuente="dengue.db"
    )