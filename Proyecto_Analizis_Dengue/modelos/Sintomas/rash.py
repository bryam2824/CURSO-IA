from Datos.respuesta_modelo import crear_respuesta
from apis.db import obtener_rash


TABLA_RIESGO_RASH = {
    "ninguno": 0.0,
    "leve": 0.3,
    "moderado": 0.6,
    "grave": 0.9
}


def clasificar_rash(severidad):

    if severidad is None:
        return ("sin_dato", 0.0)

    severidad = severidad.lower().strip()

    return (
        severidad,
        TABLA_RIESGO_RASH.get(severidad, 0.0)
    )


def evaluar_rash(id_paciente):

    severidad = obtener_rash(id_paciente)

    categoria, riesgo = clasificar_rash(severidad)

    return crear_respuesta(
        id_paciente=id_paciente,
        variable="rash",
        valor=severidad,
        categoria=categoria,
        riesgo=riesgo,
        fuente="dengue.db"
    )