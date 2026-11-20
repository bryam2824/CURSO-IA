from Datos.respuesta_modelo import crear_respuesta
from apis.db import obtener_fiebre


def clasificar_fiebre(temperatura):

    if temperatura is None:
        return (
            "sin_dato",
            0.0
        )

    if temperatura >= 39:
        return (
            "alta",
            0.9
        )

    if temperatura >= 38:
        return (
            "moderada",
            0.6
        )

    if temperatura >= 37.5:
        return (
            "leve",
            0.3
        )

    return (
        "ausente",
        0.0
    )


def evaluar_fiebre(id_paciente):

    temperatura = obtener_fiebre(id_paciente)

    categoria, riesgo = clasificar_fiebre(
        temperatura
    )

    return crear_respuesta(
        id_paciente=id_paciente,
        variable="fiebre",
        valor=temperatura,
        categoria=categoria,
        riesgo=riesgo,
        fuente="dengue.db"
    )