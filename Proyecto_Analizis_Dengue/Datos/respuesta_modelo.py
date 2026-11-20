# Datos/respuesta_modelo.py

"""
Estandarización oficial de respuestas.

Este módulo es utilizado por:

- Alarmas
- Sintomas
- Laboratorios
- Entorno
- modelo_meta_dengue.py

Todos los módulos deben construir sus salidas
utilizando estas funciones.
"""


def crear_respuesta(
    id_paciente,
    variable,
    valor,
    categoria,
    riesgo,
    fuente
):
    """
    Respuesta estándar para variables individuales.

    Ejemplo:

    {
        "id_paciente":12345,
        "variable":"plaquetas",
        "valor":75000,
        "categoria":"bajas",
        "riesgo":0.90,
        "fuente":"dengue.db"
    }
    """

    return {
        "id_paciente": id_paciente,
        "variable": variable,
        "valor": valor,
        "categoria": categoria,
        "riesgo": riesgo,
        "fuente": fuente
    }


def crear_respuesta_grupal(
    id_paciente,
    variable,
    riesgo,
    nivel,
    detalles,
    fuente
):
    """
    Respuesta estándar para agrupadores.

    Ejemplo:

    {
        "id_paciente":12345,
        "variable":"riesgo_laboratorio",
        "riesgo":0.85,
        "nivel":"ALTO",
        "detalles":{},
        "fuente":"dengue.db"
    }
    """

    return {
        "id_paciente": id_paciente,
        "variable": variable,
        "riesgo": riesgo,
        "nivel": nivel,
        "detalles": detalles,
        "fuente": fuente
    }