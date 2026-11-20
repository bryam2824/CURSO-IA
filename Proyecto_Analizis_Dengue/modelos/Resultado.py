def clasificar_riesgo(probabilidad):

    if probabilidad < 0.30:
        return "BAJO"

    elif probabilidad < 0.60:
        return "MODERADO"

    elif probabilidad < 0.80:
        return "ALTO"

    return "CRITICO"


def generar_explicacion(
    score_sintomas,
    score_laboratorio,
    score_alarmas,
    score_entorno
):
    componentes = {
        "síntomas": score_sintomas,
        "laboratorio": score_laboratorio,
        "signos de alarma": score_alarmas,
        "entorno": score_entorno
    }
    componente_principal = max(componentes, key=componentes.get)
    return f"El principal factor contribuyente es {componente_principal}."


def generar_resultado(
    probabilidad,
    score_sintomas,
    score_laboratorio,
    score_alarmas,
    score_entorno
):

    return {

        "clasificacion":
            clasificar_riesgo(probabilidad),

        "probabilidad_dengue":
            round(probabilidad, 4),

        "explicacion":
            generar_explicacion(
                score_sintomas,
                score_laboratorio,
                score_alarmas,
                score_entorno
            ),

        "componentes": {

            "sintomas":
                round(score_sintomas, 4),

            "laboratorio":
                round(score_laboratorio, 4),

            "alarmas":
                round(score_alarmas, 4),

            "entorno":
                round(score_entorno, 4)

        }

    }
    

    