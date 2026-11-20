from Datos.respuesta_modelo import crear_respuesta
from apis.db import obtener_retroocular


TABLA_RIESGO_RETROOCULAR = {
    "ninguna": 0.0,
    "leve": 0.3,
    "moderada": 0.6,
    "grave": 0.9
}


def clasificar_retroocular(severidad):

    if severidad is None:
        return ("sin_dato", 0.0)

    severidad = severidad.lower().strip()

    return (
        severidad,
        TABLA_RIESGO_RETROOCULAR.get(severidad, 0.0)
    )


def evaluar_retroocular(id_paciente):

    severidad = obtener_retroocular(id_paciente)

    categoria, riesgo = clasificar_retroocular(severidad)

    return crear_respuesta(
        id_paciente=id_paciente,
        variable="retroocular",
        valor=severidad,
        categoria=categoria,
        riesgo=riesgo,
        fuente="dengue.db"
    )