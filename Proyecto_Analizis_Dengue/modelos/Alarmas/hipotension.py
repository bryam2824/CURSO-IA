# modelos/Alarmas/hipotension.py

from Datos.respuesta_modelo import crear_respuesta
from apis.db import obtener_hipotension


RIESGO_HIPOTENSION_PRESENTE = 0.95
RIESGO_HIPOTENSION_AUSENTE = 0.05


def clasificar_hipotension(hipotension) -> tuple:
    """
    Clasifica la presencia de hipotensión.

    Regla clínica:
    - Hipotensión presente: signo de alarma asociado a fuga plasmática
      y posible progresión a dengue grave.
    - Hipotensión ausente: riesgo bajo por esta variable.
    """

    if hipotension is None:
        return (
            "sin_dato",
            0.0
        )

    if bool(hipotension):
        return (
            "presente",
            RIESGO_HIPOTENSION_PRESENTE
        )

    return (
        "ausente",
        RIESGO_HIPOTENSION_AUSENTE
    )


def evaluar_hipotension(id_paciente: int) -> dict:
    """
    Contrato entrada:

    {
        "id_paciente": 12345
    }

    Contrato salida:

    {
        "id_paciente":12345,
        "variable":"hipotension",
        "valor":True,
        "categoria":"presente",
        "riesgo":0.95,
        "fuente":"dengue.db"
    }
    """

    hipotension = obtener_hipotension(id_paciente)

    categoria, riesgo = clasificar_hipotension(hipotension)

    return crear_respuesta(
        id_paciente=id_paciente,
        variable="hipotension",
        valor=hipotension,
        categoria=categoria,
        riesgo=riesgo,
        fuente="dengue.db"
    )