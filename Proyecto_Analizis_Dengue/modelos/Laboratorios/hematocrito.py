from apis.db import obtener_hematocrito


def analizar_hematocrito(id_paciente):

    valor = obtener_hematocrito(id_paciente)

    if valor is None:
        return {
            "id_paciente": id_paciente,
            "variable": "hematocrito",
            "error": "Resultado no encontrado"
        }

    if valor < 35:
        riesgo = 0.2
        categoria = "bajo"

    elif valor <= 45:
        riesgo = 0.4
        categoria = "normal"

    elif valor <= 50:
        riesgo = 0.7
        categoria = "elevado"

    else:
        riesgo = 1.0
        categoria = "critico"

    return {
        "id_paciente": id_paciente,
        "variable": "hematocrito",
        "valor": valor,
        "categoria": categoria,
        "riesgo": riesgo,
        "fuente": "dengue.db"
    }

