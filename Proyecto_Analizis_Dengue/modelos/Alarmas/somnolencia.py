# modelos/Alarmas/somnolencia.py

from Datos.respuesta_modelo import crear_respuesta
from apis.db import obtener_somnolencia


RIESGO_SOMNOLENCIA_PRESENTE = 0.95
RIESGO_SOMNOLENCIA_AUSENTE = 0.05


def clasificar_somnolencia(somnolencia) -> tuple:
    """
    Clasifica la presencia de somnolencia.

    Regla clínica:
    - Somnolencia presente: signo de alarma asociado
      a posible compromiso clínico y deterioro del estado general.
    - Somnolencia ausente: riesgo bajo para esta variable.
    """

    if somnolencia is None:
        return (
            "sin_dato",
            0.0
        )

    if bool(somnolencia):
        return (
            "presente",
            RIESGO_SOMNOLENCIA_PRESENTE
        )

    return (
        "ausente",
        RIESGO_SOMNOLENCIA_AUSENTE
    )


def evaluar_somnolencia(id_paciente: int) -> dict:
    """
    Contrato entrada:

    {
        "id_paciente": 12345
    }

    Contrato salida:

    {
        "id_paciente":12345,
        "variable":"somnolencia",
        "valor":True,
        "categoria":"presente",
        "riesgo":0.95,
        "fuente":"dengue.db"
    }
    """

    somnolencia = obtener_somnolencia(id_paciente)

    categoria, riesgo = clasificar_somnolencia(somnolencia)

    return crear_respuesta(
        id_paciente=id_paciente,
        variable="somnolencia",
        valor=somnolencia,
        categoria=categoria,
        riesgo=riesgo,
        fuente="dengue.db"
    )