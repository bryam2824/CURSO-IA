from Datos.respuesta_modelo import crear_respuesta
from apis.db import obtener_mialgia


TABLA_RIESGO_MIALGIA = {
    "ninguna": 0.0,
    "leve": 0.3,
    "moderada": 0.6,
    "grave": 0.9
}


def clasificar_mialgia(severidad):

    if severidad is None:
        return ("sin_dato", 0.0)

    severidad = severidad.lower().strip()

    return (
        severidad,
        TABLA_RIESGO_MIALGIA.get(severidad, 0.0)
    )


def evaluar_mialgia(id_paciente):

    severidad = obtener_mialgia(id_paciente)

    categoria, riesgo = clasificar_mialgia(severidad)

    return crear_respuesta(
        id_paciente=id_paciente,
        variable="mialgia",
        valor=severidad,
        categoria=categoria,
        riesgo=riesgo,
        fuente="dengue.db"
    )