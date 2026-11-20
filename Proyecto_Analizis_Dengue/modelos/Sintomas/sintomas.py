# modelos/Sintomas/sintomas.py

from modelos.Sintomas.artralgia import evaluar_artralgia
from modelos.Sintomas.cefalea import evaluar_cefalea
from modelos.Sintomas.fiebre import evaluar_fiebre
from modelos.Sintomas.mialgia import evaluar_mialgia
from modelos.Sintomas.nauseas import evaluar_nauseas
from modelos.Sintomas.rash import evaluar_rash
from modelos.Sintomas.retroocular import evaluar_retroocular
from modelos.Sintomas.sangrado import evaluar_sangrado
from modelos.Sintomas.vomitos import evaluar_vomitos

from Datos.respuesta_modelo import crear_respuesta_grupal


def calcular_score_sintomas(resultados: dict) -> tuple:
    """
    Utiliza como score final
    el síntoma con mayor riesgo.
    """

    score = 0.0
    sintoma_principal = None

    for nombre, resultado in resultados.items():

        riesgo = resultado.get(
            "riesgo",
            0.0
        )

        if riesgo > score:
            score = riesgo
            sintoma_principal = nombre

    return score, sintoma_principal


def clasificar_nivel(score: float) -> str:

    if score >= 0.80:
        return "ALTO"

    if score >= 0.40:
        return "MODERADO"

    return "BAJO"


def riesgo_sintomas(payload: dict) -> dict:
    """
    Contrato oficial:

    {
        "id_paciente":12345
    }
    """

    id_paciente = payload["id_paciente"]

    resultados = {

        "artralgia":
            evaluar_artralgia(
                id_paciente
            ),

        "cefalea":
            evaluar_cefalea(
                id_paciente
            ),

        "fiebre":
            evaluar_fiebre(
                id_paciente
            ),

        "mialgia":
            evaluar_mialgia(
                id_paciente
            ),

        "nauseas":
            evaluar_nauseas(
                id_paciente
            ),

        "rash":
            evaluar_rash(
                id_paciente
            ),

        "retroocular":
            evaluar_retroocular(
                id_paciente
            ),

        "sangrado":
            evaluar_sangrado(
                id_paciente
            ),

        "vomitos":
            evaluar_vomitos(
                id_paciente
            )
    }

    score, sintoma_principal = (
        calcular_score_sintomas(
            resultados
        )
    )

    return crear_respuesta_grupal(
        id_paciente=id_paciente,
        variable="riesgo_sintomas",
        riesgo=score,
        nivel=clasificar_nivel(
            score
        ),
        detalles={
            "sintoma_principal":
                sintoma_principal,
            "variables":
                resultados
        },
        fuente="dengue.db"
    )