# modelos/Sintomas/artralgia.py

from Datos.respuesta_modelo import crear_respuesta
from apis.db import obtener_artralgia


TABLA_RIESGO_ARTRALGIA = {
    "ninguna": 0.0,
    "leve": 0.3,
    "moderada": 0.6,
    "grave": 0.9
}


def clasificar_artralgia(severidad: str) -> tuple:
    """
    Analiza únicamente la variable artralgia.
    """

    if severidad is None:
        return (
            "sin_dato",
            0.0
        )

    severidad = severidad.lower().strip()

    riesgo = TABLA_RIESGO_ARTRALGIA.get(
        severidad,
        0.0
    )

    return (
        severidad,
        riesgo
    )


def evaluar_artralgia(id_paciente: int) -> dict:
    """
    Contrato entrada:

    {
        "id_paciente": 12345
    }

    Contrato salida:

    {
        "id_paciente": 12345,
        "variable": "artralgia",
        "valor": "moderada",
        "categoria": "moderada",
        "riesgo": 0.6,
        "fuente": "dengue.db"
    }
    """

    severidad = obtener_artralgia(
        id_paciente=id_paciente
    )

    categoria, riesgo = clasificar_artralgia(
        severidad
    )

    return crear_respuesta(
        id_paciente=id_paciente,
        variable="artralgia",
        valor=severidad,
        categoria=categoria,
        riesgo=riesgo,
        fuente="dengue.db"
    )