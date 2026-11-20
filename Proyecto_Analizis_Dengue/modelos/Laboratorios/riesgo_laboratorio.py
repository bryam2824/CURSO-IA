from Datos.respuesta_modelo import crear_respuesta


def calcular_riesgo_laboratorio(id_paciente, resultados):

    riesgos = []

    variables = [
        "hematocrito",
        "hemoglobina",
        "leucocitos",
        "neutrofilos",
        "plaquetas"
    ]

    for variable in variables:

        resultado = resultados.get(variable)

        if resultado is None:
            continue

        if "riesgo" not in resultado:
            continue

        riesgos.append(resultado["riesgo"])

    if not riesgos:

        return {
            "id_paciente": id_paciente,
            "variable": "riesgo_laboratorio",
            "error": "No existen resultados válidos"
        }

    score = round(
        sum(riesgos) / len(riesgos),
        2
    )

    if score >= 0.75:
        nivel = "CRITICO"

    elif score >= 0.50:
        nivel = "ALTO"

    elif score >= 0.25:
        nivel = "MODERADO"

    else:
        nivel = "BAJO"

    return {
        "id_paciente": id_paciente,
        "variable": "riesgo_laboratorio",
        "riesgo": score,
        "nivel": nivel,
        "detalles": resultados,
        "fuente": "dengue.db"
    }
    