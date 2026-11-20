from Datos.respuesta_modelo import (
    crear_respuesta_grupal
)

from modelos.Entorno.clima import analizar as analizar_clima
from modelos.Entorno.epidemiologia import analizar as analizar_epidemiologia
from modelos.Entorno.geografia import analizar as analizar_geografia
from modelos.Entorno.urbanismo import analizar as analizar_urbanismo


PESO_CLIMA = 0.35
PESO_EPIDEMIOLOGIA = 0.35
PESO_GEOGRAFIA = 0.15
PESO_URBANISMO = 0.15


def analizar(id_paciente):
    """
    Consolida todos los factores de entorno y genera
    el riesgo_entorno oficial.
    """

    clima = analizar_clima(id_paciente)

    epidemiologia = analizar_epidemiologia(
        id_paciente
    )

    geografia = analizar_geografia(
        id_paciente
    )

    urbanismo = analizar_urbanismo(
        id_paciente
    )

    riesgo = calcular_riesgo_entorno(
        riesgo_clima=clima["riesgo"],
        riesgo_epidemiologico=epidemiologia["riesgo"],
        riesgo_geografico=geografia["riesgo"],
        riesgo_urbanistico=urbanismo["riesgo"]
    )

    return crear_respuesta_grupal(
        id_paciente=id_paciente,
        variable="riesgo_entorno",
        riesgo=riesgo,
        nivel=clasificar_riesgo(riesgo),
        detalles={
            "riesgo_clima": clima["riesgo"],
            "riesgo_epidemiologico":
                epidemiologia["riesgo"],
            "riesgo_geografico":
                geografia["riesgo"],
            "riesgo_urbanistico":
                urbanismo["riesgo"]
        },
        fuente="riesgo_entorno.py"
    )


def calcular_riesgo_entorno(
    riesgo_clima,
    riesgo_epidemiologico,
    riesgo_geografico,
    riesgo_urbanistico
):

    riesgo = (

        riesgo_clima
        * PESO_CLIMA

        +

        riesgo_epidemiologico
        * PESO_EPIDEMIOLOGIA

        +

        riesgo_geografico
        * PESO_GEOGRAFIA

        +

        riesgo_urbanistico
        * PESO_URBANISMO

    )

    return round(
        min(riesgo, 1.0),
        4
    )


def clasificar_riesgo(riesgo):

    if riesgo >= 0.70:
        return "ALTO"

    if riesgo >= 0.40:
        return "MEDIO"

    return "BAJO"