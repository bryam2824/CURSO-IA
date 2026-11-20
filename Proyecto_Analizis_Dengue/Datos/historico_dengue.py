# Datos/historico_dengue.py

from apis.db import conectar_historico


def obtener_epidemiologia_municipio(
    municipio: str
) -> dict:
    """
    Obtiene información epidemiológica
    histórica del municipio.
    """

    with conectar_historico() as conn:

        conn.row_factory = dict_factory

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM epidemiologia
            WHERE municipio = ?
            ORDER BY fecha_referencia DESC
            LIMIT 1
            """,
            (municipio,)
        )

        return cursor.fetchone()


def obtener_geografia_municipio(
    municipio: str
) -> dict:
    """
    Obtiene información geográfica.
    """

    with conectar_historico() as conn:

        conn.row_factory = dict_factory

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM geografia
            WHERE municipio = ?
            LIMIT 1
            """,
            (municipio,)
        )

        return cursor.fetchone()


def obtener_urbanismo_municipio(
    municipio: str
) -> dict:
    """
    Obtiene información urbanística.
    """

    with conectar_historico() as conn:

        conn.row_factory = dict_factory

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM urbanismo
            WHERE municipio = ?
            LIMIT 1
            """,
            (municipio,)
        )

        return cursor.fetchone()


def obtener_zona_municipio(
    municipio: str,
    zona: str
) -> dict:
    """
    Obtiene información histórica
    específica de la zona.
    """

    with conectar_historico() as conn:

        conn.row_factory = dict_factory

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM zona
            WHERE municipio = ?
            AND zona = ?
            LIMIT 1
            """,
            (
                municipio,
                zona
            )
        )

        return cursor.fetchone()


def dict_factory(cursor, row):

    return {
        col[0]: row[idx]
        for idx, col in enumerate(
            cursor.description
        )
    }