# modelos/Alarmas/alarmas.py

from modelos.Alarmas.dolor_abdominal import evaluar_dolor_abdominal
from modelos.Alarmas.hipotension import evaluar_hipotension
from modelos.Alarmas.sangrado_alarma import evaluar_sangrado
from modelos.Alarmas.somnolencia import evaluar_somnolencia

from Datos.respuesta_modelo import crear_respuesta_grupal


def calcular_score_alarmas(resultados: dict) -> tuple:
    """
    Estrategia:
    El riesgo de alarmas corresponde a la alarma
    de mayor gravedad encontrada.
    """

    score = 0.0
    alarma_principal = None

    for nombre, resultado in resultados.items():

        riesgo = resultado.get("riesgo", 0.0)

        if riesgo > score:
            score = riesgo
            alarma_principal = nombre

    return score, alarma_principal


def clasificar_nivel(score: float) -> str:

    if score >= 0.80:
        return "ALTO"

    if score >= 0.40:
        return "MODERADO"

    return "BAJO"


def riesgo_alarmas(payload: dict) -> dict:
    """
    Contrato oficial:

    {
        "id_paciente":12345
    }
    """

    id_paciente = payload["id_paciente"]

    resultados = {
        "dolor_abdominal": evaluar_dolor_abdominal(id_paciente),
        "hipotension": evaluar_hipotension(id_paciente),
        "sangrado": evaluar_sangrado(id_paciente),
        "somnolencia": evaluar_somnolencia(id_paciente)
    }

    score, alarma_principal = calcular_score_alarmas(
        resultados
    )

    return crear_respuesta_grupal(
        id_paciente=id_paciente,
        variable="riesgo_alarmas",
        riesgo=score,
        nivel=clasificar_nivel(score),
        detalles={
            "alarma_principal": alarma_principal,
            "variables": resultados
        },
        fuente="dengue.db"
    )
    