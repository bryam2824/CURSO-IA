# modelos/Entorno/epidemiologia.py

from Datos.historico_dengue import obtener_indicadores_epidemiologicos
from Datos.respuesta_modelo import crear_respuesta


def analizar(id_paciente):
    """
    Calcula el riesgo epidemiológico de la zona donde reside
    el paciente.

    Este riesgo será utilizado posteriormente por
    xgboost_entorno.pkl.
    """

    datos = obtener_indicadores_epidemiologicos(
        id_paciente=id_paciente
    )

    casos_semana = datos.get("casos_semana", 0)
    casos_mes = datos.get("casos_mes", 0)
    brote_activo = datos.get("brote_activo", False)

    riesgo = calcular_riesgo(
        casos_semana=casos_semana,
        casos_mes=casos_mes,
        brote_activo=brote_activo
    )

    return crear_respuesta(
        id_paciente=id_paciente,
        variable="riesgo_epidemiologico",
        valor={
            "casos_semana": casos_semana,
            "casos_mes": casos_mes,
            "brote_activo": brote_activo
        },
        categoria=clasificar_riesgo(riesgo),
        riesgo=riesgo,
        fuente="historico.db"
    )


def calcular_riesgo(
    casos_semana,
    casos_mes,
    brote_activo
):
    """
    Riesgo normalizado entre 0 y 1.
    """

    riesgo = 0.0

    # Actividad semanal
    if casos_semana >= 20:
        riesgo += 0.40

    elif casos_semana >= 10:
        riesgo += 0.20

    # Actividad mensual
    if casos_mes >= 100:
        riesgo += 0.40

    elif casos_mes >= 50:
        riesgo += 0.20

    # Brote activo
    if brote_activo:
        riesgo += 0.20

    return round(min(riesgo, 1.0), 2)


def clasificar_riesgo(riesgo):

    if riesgo >= 0.70:
        return "ALTO"

    if riesgo >= 0.40:
        return "MEDIO"

    return "BAJO"