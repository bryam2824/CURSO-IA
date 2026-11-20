from Datos.respuesta_modelo import crear_respuesta
from apis.db import obtener_dolor_abdominal


RIESGO_DOLOR_PRESENTE = 0.90
RIESGO_DOLOR_AUSENTE = 0.05


def clasificar_dolor_abdominal(dolor) -> tuple:
    """
    Clasifica la presencia de dolor abdominal.

    Regla clínica:
    - Presente: signo de alarma OMS -> riesgo alto.
    - Ausente: riesgo bajo.
    """

    if dolor is None:
        return (
            "sin_dato",
            0.0
        )

    if bool(dolor):
        return (
            "presente",
            RIESGO_DOLOR_PRESENTE
        )

    return (
        "ausente",
        RIESGO_DOLOR_AUSENTE
    )


def evaluar_dolor_abdominal(id_paciente: int) -> dict:
    """
    Variable individual.

    Entrada:
    {
        "id_paciente": 12345
    }

    Salida:
    {
        "id_paciente":12345,
        "variable":"dolor_abdominal",
        "valor":True,
        "categoria":"presente",
        "riesgo":0.90,
        "fuente":"dengue.db"
    }
    """

    dolor = obtener_dolor_abdominal(id_paciente)

    categoria, riesgo = clasificar_dolor_abdominal(dolor)

    return crear_respuesta(
        id_paciente=id_paciente,
        variable="dolor_abdominal",
        valor=dolor,
        categoria=categoria,
        riesgo=riesgo,
        fuente="dengue.db"
    )