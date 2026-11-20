from Datos.respuesta_modelo import crear_respuesta
from apis.db import obtener_vomitos


def clasificar_vomitos(presente):

    if presente is None:
        return ("sin_dato", 0.0)

    if bool(presente):
        return ("presente", 0.80)

    return ("ausente", 0.05)


def evaluar_vomitos(id_paciente):

    presente = obtener_vomitos(id_paciente)

    categoria, riesgo = clasificar_vomitos(presente)

    return crear_respuesta(
        id_paciente=id_paciente,
        variable="vomitos",
        valor=presente,
        categoria=categoria,
        riesgo=riesgo,
        fuente="dengue.db"
    )