# modelos/Entorno/urbanismo.py

from Datos.respuesta_modelo import crear_respuesta
from apis.db import obtener_paciente


def analizar(id_paciente):
    """
    Analiza condiciones urbanísticas asociadas
    al riesgo de transmisión de dengue.
    """

    paciente = obtener_paciente(id_paciente)

    densidad_poblacional = paciente.get(
        "densidad_poblacional",
        0
    )

    acceso_agua = paciente.get(
        "acceso_agua_potable",
        "desconocido"
    )

    recoleccion_basuras = paciente.get(
        "recoleccion_basuras",
        "desconocido"
    )

    riesgo = calcular_riesgo_urbanistico(
        densidad_poblacional,
        acceso_agua,
        recoleccion_basuras
    )

    return crear_respuesta(
        id_paciente=id_paciente,
        variable="riesgo_urbanistico",
        valor={
            "densidad_poblacional": densidad_poblacional,
            "acceso_agua_potable": acceso_agua,
            "recoleccion_basuras": recoleccion_basuras
        },
        categoria=clasificar_riesgo(riesgo),
        riesgo=riesgo,
        fuente="pacientes.db"
    )


def calcular_riesgo_urbanistico(
    densidad_poblacional,
    acceso_agua,
    recoleccion_basuras
):

    riesgo = 0.0

    # Densidad poblacional

    if densidad_poblacional >= 5000:
        riesgo += 0.40

    elif densidad_poblacional >= 2000:
        riesgo += 0.20

    # Agua potable

    if acceso_agua == "deficiente":
        riesgo += 0.30

    elif acceso_agua == "irregular":
        riesgo += 0.15

    # Recolección de residuos

    if recoleccion_basuras == "deficiente":
        riesgo += 0.30

    elif recoleccion_basuras == "irregular":
        riesgo += 0.15

    return round(
        min(riesgo, 1.0),
        2
    )


def clasificar_riesgo(riesgo):

    if riesgo >= 0.70:
        return "ALTO"

    if riesgo >= 0.40:
        return "MEDIO"

    return "BAJO"