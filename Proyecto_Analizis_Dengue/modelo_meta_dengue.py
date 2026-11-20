# modelo_meta_dengue.py

from Datos.respuesta_modelo import (
    crear_respuesta_grupal
)


def clasificar_nivel(score: float) -> str:
    """
    Escala oficial V1.0
    """

    if score >= 0.80:
        return "ALTO"

    if score >= 0.40:
        return "MODERADO"

    return "BAJO"


def calcular_riesgo_final(
    riesgo_alarmas: dict,
    riesgo_sintomas: dict,
    riesgo_laboratorio: dict,
    riesgo_entorno: dict
) -> tuple:
    """
    Consolida los riesgos principales.
    """

    riesgos_clinicos = {
        "riesgo_alarmas":
            riesgo_alarmas["riesgo"],

        "riesgo_sintomas":
            riesgo_sintomas["riesgo"],

        "riesgo_laboratorio":
            riesgo_laboratorio["riesgo"]
    }

    variable_principal = max(
        riesgos_clinicos,
        key=riesgos_clinicos.get
    )

    score = riesgos_clinicos[
        variable_principal
    ]
    riesgos = {
        **riesgos_clinicos,
        "riesgo_entorno": riesgo_entorno["riesgo"]
    }

    return (
        score,
        variable_principal,
        riesgos
    )


def riesgo_final_dengue(
    id_paciente: int,
    riesgo_alarmas: dict,
    riesgo_sintomas: dict,
    riesgo_laboratorio: dict,
    riesgo_entorno: dict
) -> dict:
    """
    Entradas:

    - riesgo_alarmas
    - riesgo_sintomas
    - riesgo_laboratorio
    - riesgo_entorno

    Salida:

    - riesgo_final_dengue
    """

    (
        score,
        variable_principal,
        riesgos
    ) = calcular_riesgo_final(
        riesgo_alarmas,
        riesgo_sintomas,
        riesgo_laboratorio,
        riesgo_entorno
    )

    return crear_respuesta_grupal(
        id_paciente=id_paciente,
        variable="riesgo_final_dengue",
        riesgo=score,
        nivel=clasificar_nivel(score),
        detalles={
            "variable_principal":
                variable_principal,

            "componentes":
                riesgos
        },
        fuente="modelo_meta_dengue.py"
    )