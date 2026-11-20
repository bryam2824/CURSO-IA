from apis.db import obtener_neutrofilos


def analizar_neutrofilos(id_paciente):

    valor = obtener_neutrofilos(id_paciente)

    if valor is None:
        return {
            "id_paciente": id_paciente,
            "variable": "neutrofilos",
            "error": "Resultado no encontrado"
        }

    if valor > 2500:
        riesgo = 0.2
        categoria = "bajo"

    elif valor >= 1500:
        riesgo = 0.5
        categoria = "normal"

    elif valor >= 1000:
        riesgo = 0.8
        categoria = "elevado"

    else:
        riesgo = 1.0
        categoria = "critico"
    
    return {
        "id_paciente": id_paciente,
        "variable": "neutrofilos",
        "valor": valor,
        "categoria": categoria,
        "riesgo": riesgo,
        "fuente": "dengue.db"   
    }