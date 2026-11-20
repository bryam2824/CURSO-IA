"""Acceso local y persistencia de datos del proyecto."""

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, ContextManager, Generator, Mapping


_DB_DIR = Path(
    os.environ.get(
        "DENGUE_DB_DIR",
        str(Path(__file__).resolve().parents[1] / "db"),
    )
)

_LABORATORIOS = {
    "hematocrito",
    "hemoglobina",
    "leucocitos",
    "neutrofilos",
    "plaquetas",
}

_ALARMAS = {
    "dolor_abdominal",
    "hipotension",
    "sangrado",
    "somnolencia",
}

_SINTOMAS = {
    "artralgia",
    "cefalea",
    "fiebre",
    "mialgia",
    "nauseas",
    "rash",
    "retroocular",
    "sangrado",
    "vomitos",
}


@contextmanager
def _conectar(nombre: str) -> Generator[sqlite3.Connection, None, None]:
    path = _DB_DIR / nombre
    if not path.is_file():
        raise FileNotFoundError(f"No existe la base local requerida: {path}")

    conexion = sqlite3.connect(path, timeout=10)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    try:
        with conexion:
            yield conexion
    finally:
        conexion.close()


def conectar_dengue() -> ContextManager[sqlite3.Connection]:
    """Abre dengue.db y cierra la conexión al salir del bloque with."""
    return _conectar("dengue.db")


def conectar_historico() -> ContextManager[sqlite3.Connection]:
    """Abre historico.db y cierra la conexión al salir del bloque with."""
    return _conectar("historico.db")


def conectar_pacientes() -> ContextManager[sqlite3.Connection]:
    """Abre pacientes.db y cierra la conexión al salir del bloque with."""
    return _conectar("pacientes.db")


def _fila_a_dict(fila: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(fila) if fila is not None else None


def _obtener_valor(
    tabla: str,
    columna: str,
    id_paciente: int,
    columnas_permitidas: set[str],
) -> Any:
    if columna not in columnas_permitidas:
        raise ValueError(f"Columna no permitida: {columna}")

    with conectar_dengue() as conexion:
        fila = conexion.execute(
            f"SELECT {columna} FROM {tabla} WHERE id_paciente = ?",
            (id_paciente,),
        ).fetchone()
    return fila[0] if fila is not None else None


def _obtener_columna_laboratorios(
    id_paciente: int,
    columna: str,
) -> float | None:
    return _obtener_valor(
        "laboratorios",
        columna,
        id_paciente,
        _LABORATORIOS,
    )


def obtener_hematocrito(id_paciente: int) -> float | None:
    return _obtener_columna_laboratorios(id_paciente, "hematocrito")


def obtener_hemoglobina(id_paciente: int) -> float | None:
    return _obtener_columna_laboratorios(id_paciente, "hemoglobina")


def obtener_leucocitos(id_paciente: int) -> float | None:
    return _obtener_columna_laboratorios(id_paciente, "leucocitos")


def obtener_neutrofilos(id_paciente: int) -> float | None:
    return _obtener_columna_laboratorios(id_paciente, "neutrofilos")


def obtener_plaquetas(id_paciente: int) -> float | None:
    return _obtener_columna_laboratorios(id_paciente, "plaquetas")


def _obtener_alarma(id_paciente: int, columna: str) -> int | None:
    return _obtener_valor("alarmas", columna, id_paciente, _ALARMAS)


def obtener_dolor_abdominal(id_paciente: int) -> int | None:
    return _obtener_alarma(id_paciente, "dolor_abdominal")


def obtener_hipotension(id_paciente: int) -> int | None:
    return _obtener_alarma(id_paciente, "hipotension")


def obtener_sangrado(id_paciente: int) -> int | None:
    return _obtener_alarma(id_paciente, "sangrado")


def obtener_somnolencia(id_paciente: int) -> int | None:
    return _obtener_alarma(id_paciente, "somnolencia")


def _obtener_sintoma(id_paciente: int, columna: str) -> Any:
    return _obtener_valor("sintomas", columna, id_paciente, _SINTOMAS)


def obtener_artralgia(id_paciente: int) -> Any:
    return _obtener_sintoma(id_paciente, "artralgia")


def obtener_cefalea(id_paciente: int) -> Any:
    return _obtener_sintoma(id_paciente, "cefalea")


def obtener_fiebre(id_paciente: int) -> float | None:
    return _obtener_sintoma(id_paciente, "fiebre")


def obtener_mialgia(id_paciente: int) -> Any:
    return _obtener_sintoma(id_paciente, "mialgia")


def obtener_nauseas(id_paciente: int) -> Any:
    return _obtener_sintoma(id_paciente, "nauseas")


def obtener_rash(id_paciente: int) -> Any:
    return _obtener_sintoma(id_paciente, "rash")


def obtener_retroocular(id_paciente: int) -> Any:
    return _obtener_sintoma(id_paciente, "retroocular")


def obtener_sangrado_sintoma(id_paciente: int) -> Any:
    return _obtener_sintoma(id_paciente, "sangrado")


def obtener_vomitos(id_paciente: int) -> Any:
    return _obtener_sintoma(id_paciente, "vomitos")


def obtener_paciente(id_paciente: int) -> dict[str, Any] | None:
    with conectar_pacientes() as conexion:
        fila = conexion.execute(
            "SELECT * FROM pacientes WHERE id_paciente = ?",
            (id_paciente,),
        ).fetchone()
    return _fila_a_dict(fila)


def obtener_contexto_paciente(id_paciente: int) -> dict[str, Any] | None:
    paciente = obtener_paciente(id_paciente)
    if paciente is None:
        return None

    geografia = obtener_geografia_municipio(
        municipio=paciente.get("municipio"),
        departamento=paciente.get("departamento"),
        codigo_municipio=paciente.get("codigo_municipio"),
    )
    if geografia:
        paciente["geografia"] = geografia
        paciente.update({
            campo: geografia[campo]
            for campo in (
                "latitud",
                "longitud",
                "altitud",
                "cercania_cuerpos_agua",
                "pendiente",
                "fuente_coordenadas",
                "fecha_verificacion",
            )
            if campo in geografia
        })
    return paciente


def obtener_datos_clinicos(id_paciente: int) -> dict[str, dict[str, Any]]:
    with conectar_dengue() as conexion:
        sintomas = _fila_a_dict(
            conexion.execute(
                "SELECT * FROM sintomas WHERE id_paciente = ?",
                (id_paciente,),
            ).fetchone()
        ) or {}
        laboratorios = _fila_a_dict(
            conexion.execute(
                "SELECT * FROM laboratorios WHERE id_paciente = ?",
                (id_paciente,),
            ).fetchone()
        ) or {}
        alarmas = _fila_a_dict(
            conexion.execute(
                "SELECT * FROM alarmas WHERE id_paciente = ?",
                (id_paciente,),
            ).fetchone()
        ) or {}

    return {
        "sintomas": {
            "artralgia": sintomas.get("artralgia"),
            "cefalea": sintomas.get("cefalea"),
            "mialgia": sintomas.get("mialgia"),
            "dolor_retroocular": sintomas.get("retroocular"),
            "nauseas": sintomas.get("nauseas"),
            "vomitos": sintomas.get("vomitos"),
            "rash": sintomas.get("rash"),
            "fiebre": sintomas.get("fiebre"),
        },
        "laboratorios": {
            "plaquetas": laboratorios.get("plaquetas"),
            "leucocitos": laboratorios.get("leucocitos"),
            "hematocrito": laboratorios.get("hematocrito"),
            "hemoglobina": laboratorios.get("hemoglobina"),
            "neutrofilos": laboratorios.get("neutrofilos"),
        },
        "alarmas": {
            "dolor_abdominal": alarmas.get("dolor_abdominal"),
            "hipotension": alarmas.get("hipotension"),
            "sangrado": alarmas.get("sangrado"),
            "somnolencia": alarmas.get("somnolencia"),
        },
    }


def obtener_id_paciente_por_documento(documento: str) -> int | None:
    if not documento or not documento.strip():
        return None

    with conectar_pacientes() as conexion:
        fila = conexion.execute(
            "SELECT id_paciente FROM pacientes WHERE documento = ?",
            (documento.strip(),),
        ).fetchone()
    return int(fila[0]) if fila is not None else None


def obtener_geografia_municipio(
    municipio: str | None,
    departamento: str | None = None,
    codigo_municipio: str | None = None,
) -> dict[str, Any] | None:
    if codigo_municipio:
        consulta = "SELECT * FROM geografia WHERE codigo_municipio = ?"
        parametros: tuple[str, ...] = (codigo_municipio.strip(),)
    elif municipio and departamento:
        consulta = (
            "SELECT * FROM geografia "
            "WHERE lower(municipio) = lower(?) "
            "AND lower(departamento) = lower(?)"
        )
        parametros = (municipio.strip(), departamento.strip())
    elif municipio:
        consulta = "SELECT * FROM geografia WHERE lower(municipio) = lower(?)"
        parametros = (municipio.strip(),)
    else:
        return None

    with conectar_historico() as conexion:
        filas = conexion.execute(consulta, parametros).fetchall()
    if len(filas) > 1:
        raise ValueError(
            "La ubicación no es única; indique el código DANE del municipio."
        )
    return _fila_a_dict(filas[0]) if filas else None


def guardar_geografia_municipio(ubicacion: Mapping[str, Any]) -> None:
    obligatorios = (
        "codigo_municipio",
        "departamento",
        "municipio",
        "latitud",
        "longitud",
        "fuente_coordenadas",
        "fecha_verificacion",
    )
    faltantes = [campo for campo in obligatorios if ubicacion.get(campo) is None]
    if faltantes:
        raise ValueError(
            "Faltan campos de procedencia geográfica: " + ", ".join(faltantes)
        )

    latitud = float(ubicacion["latitud"])
    longitud = float(ubicacion["longitud"])
    if not -90 <= latitud <= 90 or not -180 <= longitud <= 180:
        raise ValueError("Las coordenadas geográficas están fuera de rango.")

    with conectar_historico() as conexion:
        conexion.execute(
            """
            INSERT INTO geografia (
                codigo_municipio, departamento, municipio, latitud, longitud,
                fuente_coordenadas, fecha_verificacion
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(codigo_municipio)
            DO UPDATE SET
                departamento = excluded.departamento,
                municipio = excluded.municipio,
                latitud = excluded.latitud,
                longitud = excluded.longitud,
                fuente_coordenadas = excluded.fuente_coordenadas,
                fecha_verificacion = excluded.fecha_verificacion
            """,
            (
                ubicacion["codigo_municipio"],
                ubicacion["departamento"],
                ubicacion["municipio"],
                latitud,
                longitud,
                ubicacion["fuente_coordenadas"],
                ubicacion["fecha_verificacion"],
            ),
        )


def obtener_clima_local(
    codigo_municipio: str,
    fecha_referencia: str,
) -> dict[str, Any] | None:
    with conectar_historico() as conexion:
        fila = conexion.execute(
            """
            SELECT * FROM clima
            WHERE codigo_municipio = ? AND fecha_referencia = ?
            ORDER BY fecha_consulta_utc DESC
            LIMIT 1
            """,
            (codigo_municipio, fecha_referencia),
        ).fetchone()
    return _fila_a_dict(fila)


def guardar_clima_local(observacion: Mapping[str, Any]) -> None:
    obligatorios = (
        "codigo_municipio",
        "departamento",
        "municipio",
        "fecha_referencia",
        "fuente",
        "fecha_consulta_utc",
    )
    faltantes = [campo for campo in obligatorios if not observacion.get(campo)]
    if faltantes:
        raise ValueError(
            "Faltan campos de procedencia climática: " + ", ".join(faltantes)
        )

    with conectar_historico() as conexion:
        conexion.execute(
            """
            INSERT INTO clima (
                codigo_municipio, departamento, municipio, fecha_referencia,
                temperatura_media, humedad, precipitacion, fuente,
                fecha_consulta_utc
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(codigo_municipio, fecha_referencia, fuente)
            DO UPDATE SET
                departamento = excluded.departamento,
                municipio = excluded.municipio,
                temperatura_media = excluded.temperatura_media,
                humedad = excluded.humedad,
                precipitacion = excluded.precipitacion,
                fecha_consulta_utc = excluded.fecha_consulta_utc
            """,
            (
                observacion["codigo_municipio"],
                observacion["departamento"],
                observacion["municipio"],
                observacion["fecha_referencia"],
                observacion.get("temperatura_media"),
                observacion.get("humedad"),
                observacion.get("precipitacion"),
                observacion["fuente"],
                observacion["fecha_consulta_utc"],
            ),
        )


def obtener_vigilancia_municipal(
    codigo_municipio: str,
    fecha_referencia: str,
) -> dict[str, Any] | None:
    with conectar_historico() as conexion:
        fila = conexion.execute(
            """
            SELECT * FROM vigilancia_dengue
            WHERE codigo_municipio = ? AND periodo_inicio <= ?
            ORDER BY periodo_fin DESC, fecha_publicacion DESC
            LIMIT 1
            """,
            (codigo_municipio, fecha_referencia),
        ).fetchone()
    return _fila_a_dict(fila)


def guardar_vigilancia_municipal(indicadores: Mapping[str, Any]) -> None:
    obligatorios = (
        "codigo_municipio",
        "departamento",
        "municipio",
        "periodo_inicio",
        "periodo_fin",
        "fuente",
        "fecha_consulta_utc",
    )
    faltantes = [campo for campo in obligatorios if not indicadores.get(campo)]
    if faltantes:
        raise ValueError(
            "Faltan campos de procedencia epidemiológica: "
            + ", ".join(faltantes)
        )

    with conectar_historico() as conexion:
        conexion.execute(
            """
            INSERT INTO vigilancia_dengue (
                codigo_municipio, departamento, municipio, periodo_inicio,
                periodo_fin, casos_probables, casos_confirmados, casos_graves,
                fuente, id_conjunto_datos, fecha_publicacion,
                fecha_consulta_utc, licencia
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(codigo_municipio, periodo_inicio, periodo_fin, fuente)
            DO UPDATE SET
                departamento = excluded.departamento,
                municipio = excluded.municipio,
                casos_probables = excluded.casos_probables,
                casos_confirmados = excluded.casos_confirmados,
                casos_graves = excluded.casos_graves,
                id_conjunto_datos = excluded.id_conjunto_datos,
                fecha_publicacion = excluded.fecha_publicacion,
                fecha_consulta_utc = excluded.fecha_consulta_utc,
                licencia = excluded.licencia
            """,
            (
                indicadores["codigo_municipio"],
                indicadores["departamento"],
                indicadores["municipio"],
                indicadores["periodo_inicio"],
                indicadores["periodo_fin"],
                indicadores.get("casos_probables"),
                indicadores.get("casos_confirmados"),
                indicadores.get("casos_graves"),
                indicadores["fuente"],
                indicadores.get("id_conjunto_datos"),
                indicadores.get("fecha_publicacion"),
                indicadores["fecha_consulta_utc"],
                indicadores.get("licencia"),
            ),
        )
