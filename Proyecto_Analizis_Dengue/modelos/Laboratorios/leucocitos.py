from apis.db import obtener_leucocitos


def analizar_leucocitos(id_paciente):

    valor = obtener_leucocitos(id_paciente)

    if valor is None:
        return {
            "id_paciente": id_paciente,
            "variable": "leucocitos",
            "error": "Resultado no encontrado"
        }

    if valor > 5000:
        riesgo = 0.2
        categoria = "bajo"

    elif valor >= 3000:
        riesgo = 0.6
        categoria = "normal"    

    else:
        riesgo = 1.0
        categoria = "critico"

    return {
        "id_paciente": id_paciente,
        "variable": "leucocitos",
        "valor": valor,
        "categoria": categoria,
        "riesgo": riesgo,
        "fuente": "dengue.db"
    }