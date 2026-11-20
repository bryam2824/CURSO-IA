# modelos/Alarmas/sangrado.py

from Datos.respuesta_modelo import crear_respuesta
from apis.db import obtener_sangrado


RIESGO_SANGRADO_PRESENTE = 0.95
RIESGO_SANGRADO_AUSENTE = 0.05


def clasificar_sangrado(sangrado) -> tuple:
    """
    Clasifica la presencia de sangrado.

    Regla clínica:
    - Sangrado presente: signo de alarma asociado a mayor
      riesgo de complicaciones y progresión clínica.
    - Sangrado ausente: riesgo bajo para esta variable.
    """

    if sangrado is None:
        return (
            "sin_dato",
            0.0
        )

    if bool(sangrado):
        return (
            "presente",
            RIESGO_SANGRADO_PRESENTE
        )

    return (
        "ausente",
        RIESGO_SANGRADO_AUSENTE
    )


def evaluar_sangrado(id_paciente: int) -> dict:
    """
    Contrato entrada:

    {
        "id_paciente": 12345
    }

    Contrato salida:

    {
        "id_paciente":12345,
        "variable":"sangrado",
        "valor":True,
        "categoria":"presente",
        "riesgo":0.95,
        "fuente":"dengue.db"
    }
    """

    sangrado = obtener_sangrado(id_paciente)

    categoria, riesgo = clasificar_sangrado(sangrado)

    return crear_respuesta(
        id_paciente=id_paciente,
        variable="sangrado",
        valor=sangrado,
        categoria=categoria,
        riesgo=riesgo,
        fuente="dengue.db"
    )