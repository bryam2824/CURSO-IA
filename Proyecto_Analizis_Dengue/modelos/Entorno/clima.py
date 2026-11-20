
from datetime import datetime, timedelta

from Datos.respuesta_modelo import crear_respuesta
from Datos.variables_climaticas import obtener_clima_historico
from apis.db import obtener_contexto_paciente


def analizar_clima(id_paciente):

    contexto = obtener_contexto_paciente(
        id_paciente
    )

    if not contexto:

        return {
            "id_paciente": id_paciente,
            "variable": "clima",
            "error": "Paciente no encontrado"
        }

    municipio = contexto.get("municipio")

    fecha_inicio_sintomas = contexto.get(
        "fecha_inicio_sintomas"
    )

    if not municipio or not fecha_inicio_sintomas:

        return {
            "id_paciente": id_paciente,
            "variable": "clima",
            "error": "Información insuficiente"
        }

    # Se estima la fecha probable de infección

    if isinstance(fecha_inicio_sintomas, str):

        fecha_inicio_sintomas = datetime.strptime(
            fecha_inicio_sintomas,
            "%Y-%m-%d"
        )

    fecha_probable_infeccion = (
        fecha_inicio_sintomas - timedelta(days=7)
    )

    # Consulta clima histórico desde API

    clima = obtener_clima_historico(
        municipio=municipio,
        fecha=fecha_probable_infeccion.strftime(
            "%Y-%m-%d"
        )
    )

    if not clima:

        return {
            "id_paciente": id_paciente,
            "variable": "clima",
            "error": "No existe información climática"
        }

    temperatura = clima.get(
        "temperatura_media",
        0
    )

    humedad = clima.get(
        "humedad",
        0
    )

    precipitacion = clima.get(
        "precipitacion",
        0
    )

    riesgo = 0.0

    # Temperatura favorable para Aedes aegypti

    if 24 <= temperatura <= 32:
        riesgo += 0.4

    # Humedad alta favorece supervivencia

    if humedad >= 70:
        riesgo += 0.3

    # Lluvias favorecen criaderos

    if precipitacion >= 100:
        riesgo += 0.3

    riesgo = round(
        min(riesgo, 1.0),
        2
    )

    if riesgo >= 0.75:
        categoria = "alto"

    elif riesgo >= 0.50:
        categoria = "moderado"

    else:
        categoria = "bajo"

    return crear_respuesta(
        id_paciente=id_paciente,

        variable="clima",

        valor={
            "municipio": municipio,
            "fecha_probable_infeccion":
                fecha_probable_infeccion.strftime(
                    "%Y-%m-%d"
                ),
            "temperatura_media": temperatura,
            "humedad": humedad,
            "precipitacion": precipitacion
        },

        riesgo=riesgo,

        categoria=categoria,

        fuente="api_clima_historico"
    )