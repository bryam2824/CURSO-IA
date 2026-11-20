
from Datos.respuesta_modelo import crear_respuesta
from apis.db import obtener_paciente


def analizar(id_paciente):
    """
    Calcula el riesgo geográfico asociado a la ubicación
    del paciente.
    """

    paciente = obtener_paciente(id_paciente)

    altitud = paciente.get("altitud", 0)

    distancia_agua = paciente.get(
        "distancia_cuerpo_agua",
        999
    )

    riesgo = calcular_riesgo_geografico(
        altitud,
        distancia_agua
    )

    return crear_respuesta(
        id_paciente=id_paciente,
        variable="riesgo_geografico",
        valor={
            "altitud": altitud,
            "distancia_cuerpo_agua": distancia_agua
        },
        categoria=clasificar_riesgo(riesgo),
        riesgo=riesgo,
        fuente="pacientes.db"
    )


def calcular_riesgo_geografico(
    altitud,
    distancia_agua
):

    riesgo = 0.0

    # Altitud

    if altitud < 1000:
        riesgo += 0.60

    elif altitud < 1800:
        riesgo += 0.30

    # Cercanía a cuerpos de agua

    if distancia_agua < 1:
        riesgo += 0.40

    elif distancia_agua < 3:
        riesgo += 0.20

    return round(
        min(riesgo, 1.0),
        2
    )


def clasificar_riesgo(riesgo):

    if riesgo >= 0.70:
        return "ALTO"

    if riesgo >= 0.40:
        return "MEDIO"

    return "BAJO"