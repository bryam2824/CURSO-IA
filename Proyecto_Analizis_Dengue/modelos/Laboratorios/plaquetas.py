from apis.db import obtener_plaquetas


def analizar_plaquetas(id_paciente):

    valor = obtener_plaquetas(id_paciente)

    if valor is None:
        return {
            "id_paciente": id_paciente,
            "variable": "plaquetas",
            "error": "Resultado no encontrado"
        }       

    if valor >= 150000:
        riesgo = 0.1
        categoria = "bajo"

    elif valor >= 100000:
        riesgo = 0.5
        categoria = "normal"

    elif valor >= 50000:
        riesgo = 0.8
        categoria = "elevado"

    else:
        riesgo = 1.0
        categoria = "critico"

    return {
        "id_paciente": id_paciente,
        "variable": "plaquetas",
        "valor": valor,
        "categoria": categoria,
        "riesgo": riesgo,
        "fuente": "dengue.db"
    }