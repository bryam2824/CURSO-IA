"""Evaluación local y transparente de hallazgos relacionados con dengue."""

import json
import math
from pathlib import Path
from typing import Any, Mapping


SINTOMAS = (
    "fiebre",
    "cefalea",
    "mialgia",
    "artralgia",
    "dolor_retroocular",
    "nauseas",
    "vomitos",
    "rash",
)

LABORATORIOS = (
    "plaquetas",
    "leucocitos",
    "hematocrito",
    "hemoglobina",
    "neutrofilos",
)

ALARMAS = (
    "dolor_abdominal",
    "hipotension",
    "sangrado",
    "somnolencia",
)

CARACTERISTICAS = SINTOMAS + LABORATORIOS + ALARMAS
MODELO_PUBLICADO = Path(__file__).with_name("modelo_dengue_publicado.json")


def _seccion(datos: Mapping[str, Any], nombre: str) -> Mapping[str, Any]:
    valor = datos.get(nombre, {})
    if valor is None:
        return {}
    if not isinstance(valor, Mapping):
        raise ValueError(f"El campo '{nombre}' debe ser un objeto JSON.")
    return valor


def _booleano(valor: Any) -> bool | None:
    if valor is None:
        return None
    if isinstance(valor, bool):
        return valor
    if isinstance(valor, int) and valor in (0, 1):
        return bool(valor)
    if isinstance(valor, str):
        normalizado = valor.strip().lower()
        if normalizado in ("si", "sí", "true", "1", "presente"):
            return True
        if normalizado in ("no", "false", "0", "ausente"):
            return False
    return None


def _numero(valor: Any) -> float | None:
    if valor is None or isinstance(valor, bool):
        return None
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        return None
    return numero if math.isfinite(numero) else None


def analizar_paciente(
    datos: Mapping[str, Any],
    model_path: str | Path | None = None,
) -> dict[str, Any]:
    """Analiza datos proporcionados sin consultar servicios externos ni inventar valores."""
    if not isinstance(datos, Mapping):
        raise ValueError("Los datos del paciente deben ser un objeto JSON.")

    sintomas = _seccion(datos, "sintomas")
    laboratorios = _seccion(datos, "laboratorios")
    alarmas = _seccion(datos, "alarmas")
    valores: dict[str, bool | float | None] = {}
    faltantes: list[str] = []
    datos_invalidos: list[str] = []

    for campo in SINTOMAS:
        original = sintomas.get(campo)
        valor = _booleano(original)
        valores[campo] = valor
        if valor is None:
            faltantes.append(f"sintomas.{campo}")
            if original is not None:
                datos_invalidos.append(f"sintomas.{campo}")

    for campo in LABORATORIOS:
        original = laboratorios.get(campo)
        valor = _numero(original)
        valores[campo] = valor
        if valor is None:
            faltantes.append(f"laboratorios.{campo}")
            if original is not None:
                datos_invalidos.append(f"laboratorios.{campo}")

    for campo in ALARMAS:
        original = alarmas.get(campo)
        valor = _booleano(original)
        valores[campo] = valor
        if valor is None:
            faltantes.append(f"alarmas.{campo}")
            if original is not None:
                datos_invalidos.append(f"alarmas.{campo}")

    sintomas_informados = [
        valores[campo] for campo in SINTOMAS
        if valores[campo] is not None
    ]
    sintomas_presentes = sum(valor is True for valor in sintomas_informados)
    alarmas_presentes = [
        campo for campo in ALARMAS if valores[campo] is True
    ]
    laboratorios_informados = {
        campo: valores[campo]
        for campo in LABORATORIOS
        if valores[campo] is not None
    }
    campos_esperados = len(CARACTERISTICAS)
    campos_informados = campos_esperados - len(faltantes)

    estimate: dict[str, Any] = {
        "metodo": "indice_descriptivo_no_validado",
        "indice_sintomas_reportados": (
            round(sintomas_presentes / len(sintomas_informados), 4)
            if sintomas_informados
            else None
        ),
        "interpretacion": (
            "Proporción de síntomas compatibles marcados como presentes "
            "entre los síntomas informados; no es una probabilidad de dengue."
            if sintomas_informados
            else "No se puede calcular el índice: no se informaron síntomas."
        ),
    }
    modelo_estado = "no_hay_modelo_xgboost_publicado"

    published_path = Path(model_path) if model_path else MODELO_PUBLICADO
    if published_path.is_file():
        metadata_path = published_path.with_suffix(
            published_path.suffix + ".metadata.json"
        )
        if not metadata_path.is_file():
            raise ValueError(
                "El modelo local no tiene metadatos de entrenamiento; "
                "no se puede verificar su esquema ni su aprobación."
            )
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if not isinstance(metadata, dict):
            raise ValueError("Los metadatos del modelo deben ser un objeto JSON.")
        if metadata.get("estado") != "aprobado_para_uso_experimental":
            raise ValueError(
                "El artefacto XGBoost es un candidato. Requiere revisión "
                "humana antes de habilitarse."
            )
        if metadata.get("caracteristicas_y_orden") != list(CARACTERISTICAS):
            raise ValueError(
                "El esquema de características del modelo no coincide con "
                "el analizador actual."
            )

        try:
            from xgboost import XGBClassifier
        except ModuleNotFoundError as error:
            if error.name != "xgboost":
                raise
            modelo_estado = "xgboost_no_instalado"
        else:
            model = XGBClassifier()
            model.load_model(str(published_path))
            matriz = [[
                float(valores[campo])
                if valores[campo] is not None
                else float("nan")
                for campo in CARACTERISTICAS
            ]]
            probabilidad = float(model.predict_proba(matriz)[0][1])
            estimate = {
                "metodo": "xgboost_experimental",
                "probabilidad_modelo_no_validada": round(probabilidad, 4),
                "interpretacion": (
                    "Salida del modelo local. No está validada para uso "
                    "clínico y no sustituye la evaluación profesional."
                ),
            }
            modelo_estado = f"modelo_local:{published_path.name}"

    return {
        "estado": (
            "estimacion_orientativa"
            if sintomas_informados
            else "datos_insuficientes"
        ),
        "estimacion": estimate,
        "modelo": {
            "estado": modelo_estado,
            "caracteristicas": list(CARACTERISTICAS),
        },
        "hallazgos": {
            "sintomas_presentes": [
                campo for campo in SINTOMAS if valores[campo] is True
            ],
            "sintomas_informados": len(sintomas_informados),
            "sintomas_esperados": len(SINTOMAS),
            "laboratorios_recibidos": laboratorios_informados,
            "alarmas_presentes": alarmas_presentes,
        },
        "calidad_datos": {
            "campos_informados": campos_informados,
            "campos_esperados": campos_esperados,
            "completitud_porcentaje": round(
                campos_informados / campos_esperados * 100, 1
            ),
            "campos_faltantes": faltantes,
            "campos_invalidos": datos_invalidos,
        },
        "advertencias": [
            "Este resultado es apoyo experimental, no un diagnóstico ni una "
            "recomendación terapéutica.",
            "Los datos ausentes no se imputaron ni se interpretaron como "
            "resultados normales.",
            "Las unidades de laboratorio se muestran tal como se recibieron; "
            "no se convierten ni se validan.",
            "Las alarmas se muestran por separado y no se compensan con el "
            "índice de síntomas; aplique los protocolos clínicos locales.",
        ],
    }
