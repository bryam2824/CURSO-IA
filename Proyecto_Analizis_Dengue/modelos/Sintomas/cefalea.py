from Datos.respuesta_modelo import crear_respuesta
from apis.db import obtener_cefalea


TABLA_RIESGO_CEFALEA = {
    "ninguna": 0.0,
    "leve": 0.3,
    "moderada": 0.6,
    "grave": 0.9
}


def clasificar_cefalea(severidad):

    if severidad is None:
        return ("sin_dato", 0.0)

    severidad = severidad.lower().strip()

    return (
        severidad,
        TABLA_RIESGO_CEFALEA.get(severidad, 0.0)
    )


def evaluar_cefalea(id_paciente):

    severidad = obtener_cefalea(id_paciente)

    categoria, riesgo = clasificar_cefalea(severidad)

    return crear_respuesta(
        id_paciente=id_paciente,
        variable="cefalea",
        valor=severidad,
        categoria=categoria,
        riesgo=riesgo,
        fuente="dengue.db"
    )