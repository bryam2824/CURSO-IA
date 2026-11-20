from Datos.respuesta_modelo import crear_respuesta
from apis.db import obtener_nauseas


def clasificar_nauseas(presente):

    if presente is None:
        return ("sin_dato", 0.0)

    if bool(presente):
        return ("presente", 0.70)

    return ("ausente", 0.05)


def evaluar_nauseas(id_paciente):

    presente = obtener_nauseas(id_paciente)

    categoria, riesgo = clasificar_nauseas(presente)

    return crear_respuesta(
        id_paciente=id_paciente,
        variable="nauseas",
        valor=presente,
        categoria=categoria,
        riesgo=riesgo,
        fuente="dengue.db"
    )