from apis.db import obtener_hemoglobina


def analizar_hemoglobina(id_paciente):

    valor = obtener_hemoglobina(id_paciente)

    if valor is None:
        return {
            "id_paciente": id_paciente,
            "variable": "hemoglobina",
            "error": "Resultado no encontrado"
        }

    if valor < 10:
        riesgo = 0.8
        categoria = "bajo"

    elif valor < 12:
        riesgo = 0.5
        categoria = "normal"

    elif valor <= 16:
        riesgo = 0.2
        categoria = "elevado"

    else:
        riesgo = 0.6
        categoria = "critico"

    return {
        "id_paciente": id_paciente,
        "variable": "hemoglobina",
        "valor": valor,
        "categoria": categoria,
        "riesgo": riesgo,
        "fuente": "dengue.db"
    }
