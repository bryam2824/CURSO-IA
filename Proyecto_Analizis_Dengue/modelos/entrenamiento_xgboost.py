"""Entrenamiento local de modelos candidatos con etiquetas verificadas."""

import argparse
import csv
import hashlib
import json
import random
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from modelos.Analizador import (
    ALARMAS,
    CARACTERISTICAS,
    SINTOMAS,
    _booleano,
    _numero,
)


ID_FIELD = "id_paciente"
LABEL_FIELD = "dengue_confirmado"


def _convertir_caracteristica(campo: str, valor: str) -> float:
    if not valor.strip():
        return float("nan")
    if campo in SINTOMAS or campo in ALARMAS:
        convertido = _booleano(valor)
        if convertido is None:
            raise ValueError(f"Valor booleano inválido para '{campo}': {valor!r}")
        return float(convertido)
    convertido = _numero(valor)
    if convertido is None:
        raise ValueError(f"Valor numérico inválido para '{campo}': {valor!r}")
    return convertido


def _leer_dataset(path: Path) -> tuple[list[list[float]], list[int], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)
        requeridas = {ID_FIELD, LABEL_FIELD, *CARACTERISTICAS}
        faltantes = requeridas - set(lector.fieldnames or ())
        if faltantes:
            raise ValueError(
                "Faltan columnas requeridas en el CSV: "
                + ", ".join(sorted(faltantes))
            )

        filas: list[list[float]] = []
        etiquetas: list[int] = []
        pacientes: list[str] = []
        etiqueta_por_paciente: dict[str, int] = {}

        for numero_fila, fila in enumerate(lector, start=2):
            paciente = (fila.get(ID_FIELD) or "").strip()
            if not paciente:
                raise ValueError(f"Falta '{ID_FIELD}' en la fila {numero_fila}.")
            etiqueta_texto = (fila.get(LABEL_FIELD) or "").strip()
            if etiqueta_texto not in ("0", "1"):
                raise ValueError(
                    f"'{LABEL_FIELD}' debe ser 0 o 1 en la fila {numero_fila}."
                )
            etiqueta = int(etiqueta_texto)
            anterior = etiqueta_por_paciente.setdefault(paciente, etiqueta)
            if anterior != etiqueta:
                raise ValueError(
                    "Se encontraron etiquetas contradictorias para un paciente "
                    f"en la fila {numero_fila}."
                )

            filas.append([
                _convertir_caracteristica(campo, fila.get(campo) or "")
                for campo in CARACTERISTICAS
            ])
            etiquetas.append(etiqueta)
            pacientes.append(paciente)

    if not filas:
        raise ValueError("El CSV no contiene casos para entrenar.")
    return filas, etiquetas, pacientes


def _separar_por_paciente(
    etiquetas: list[int],
    pacientes: list[str],
    semilla: int,
    fraccion_prueba: float,
) -> tuple[list[int], list[int]]:
    pacientes_por_etiqueta: dict[int, set[str]] = defaultdict(set)
    for etiqueta, paciente in zip(etiquetas, pacientes):
        pacientes_por_etiqueta[etiqueta].add(paciente)

    if any(len(pacientes_por_etiqueta[etiqueta]) < 2 for etiqueta in (0, 1)):
        raise ValueError(
            "Se requieren al menos dos pacientes distintos por clase para "
            "crear entrenamiento y prueba sin fuga entre pacientes."
        )

    generador = random.Random(semilla)
    pacientes_prueba: set[str] = set()
    for etiqueta in (0, 1):
        grupos = sorted(pacientes_por_etiqueta[etiqueta])
        generador.shuffle(grupos)
        cantidad = max(1, round(len(grupos) * fraccion_prueba))
        cantidad = min(cantidad, len(grupos) - 1)
        pacientes_prueba.update(grupos[:cantidad])

    indices_prueba = [
        indice for indice, paciente in enumerate(pacientes)
        if paciente in pacientes_prueba
    ]
    indices_entrenamiento = [
        indice for indice, paciente in enumerate(pacientes)
        if paciente not in pacientes_prueba
    ]
    return indices_entrenamiento, indices_prueba


def _metricas(y_real: list[int], y_predicho: list[int]) -> dict[str, float | int]:
    verdaderos_positivos = sum(
        real == 1 and predicho == 1
        for real, predicho in zip(y_real, y_predicho)
    )
    verdaderos_negativos = sum(
        real == 0 and predicho == 0
        for real, predicho in zip(y_real, y_predicho)
    )
    positivos = sum(real == 1 for real in y_real)
    negativos = sum(real == 0 for real in y_real)
    correctos = verdaderos_positivos + verdaderos_negativos
    return {
        "casos_prueba": len(y_real),
        "exactitud": correctos / len(y_real),
        "sensibilidad": verdaderos_positivos / positivos if positivos else 0.0,
        "especificidad": verdaderos_negativos / negativos if negativos else 0.0,
    }


def entrenar_candidato(
    csv_path: str | Path,
    output_path: str | Path,
    semilla: int = 42,
    fraccion_prueba: float = 0.2,
) -> dict[str, Any]:
    if not 0.0 < fraccion_prueba < 1.0:
        raise ValueError("fraccion_prueba debe ser mayor que 0 y menor que 1.")

    origen = Path(csv_path)
    destino = Path(output_path)
    filas, etiquetas, pacientes = _leer_dataset(origen)
    indices_entrenamiento, indices_prueba = _separar_por_paciente(
        etiquetas, pacientes, semilla, fraccion_prueba
    )

    try:
        import numpy as np
        import xgboost
        from xgboost import XGBClassifier
    except ModuleNotFoundError as error:
        if error.name not in ("numpy", "xgboost"):
            raise
        raise RuntimeError(
            "XGBoost y NumPy son necesarios para entrenar. Instale "
            "requirements.txt en un equipo conectado y luego ejecute el "
            "entrenamiento sin conexión."
        ) from error

    X = np.asarray(filas, dtype=float)
    y = np.asarray(etiquetas, dtype=int)

    model = XGBClassifier(
        objective="binary:logistic",
        eval_metric="logloss",
        n_estimators=100,
        max_depth=3,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=semilla,
        n_jobs=1,
        verbosity=0,
    )
    model.fit(X[indices_entrenamiento], y[indices_entrenamiento])
    predicciones = model.predict(X[indices_prueba]).astype(int).tolist()
    metricas = _metricas(
        y[indices_prueba].tolist(),
        predicciones,
    )
    destino.parent.mkdir(parents=True, exist_ok=True)
    model.save_model(str(destino))

    metadata = {
        "estado": "candidato_requiere_revision_clinica",
        "fecha_entrenamiento_utc": datetime.now(timezone.utc).isoformat(),
        "sha256_dataset": hashlib.sha256(origen.read_bytes()).hexdigest(),
        "version_python": sys.version.split()[0],
        "version_xgboost": xgboost.__version__,
        "version_numpy": np.__version__,
        "filas": len(filas),
        "pacientes": len(set(pacientes)),
        "caracteristicas_y_orden": list(CARACTERISTICAS),
        "resultado_objetivo": LABEL_FIELD,
        "particion": "por_paciente; no equivale a validacion temporal o externa",
        "metricas_holdout": metricas,
    }
    metadata_path = destino.with_suffix(destino.suffix + ".metadata.json")
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return {
        "modelo_candidato": str(destino),
        "metadata": str(metadata_path),
        **metadata,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Entrena un candidato XGBoost con casos confirmados."
    )
    parser.add_argument("csv", help="CSV local con desenlaces clínicos confirmados.")
    parser.add_argument(
        "--salida",
        default="modelos/candidatos/modelo_dengue_candidato.json",
        help="Ruta del artefacto candidato; no se publica automáticamente.",
    )
    args = parser.parse_args()
    print(json.dumps(
        entrenar_candidato(args.csv, args.salida),
        ensure_ascii=False,
        indent=2,
    ))


if __name__ == "__main__":
    main()
