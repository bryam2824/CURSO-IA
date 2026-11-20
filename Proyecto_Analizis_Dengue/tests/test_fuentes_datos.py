import json
import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

from apis import api, db
from Datos import contexto_territorial
from Datos.proveedores import nasa_power


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    "dengue.db": "schema_dengue.sql",
    "historico.db": "schema_historico.sql",
    "pacientes.db": "schema_pacientes.sql",
}


class CapaDatosTests(unittest.TestCase):
    def setUp(self):
        self.directorio = TemporaryDirectory()
        self.addCleanup(self.directorio.cleanup)
        self.patch_db = patch.object(db, "_DB_DIR", Path(self.directorio.name))
        self.patch_db.start()
        self.addCleanup(self.patch_db.stop)

        schema_dir = PROJECT_ROOT / "db"
        for database_name, schema_name in SCHEMAS.items():
            conexion = sqlite3.connect(Path(self.directorio.name) / database_name)
            try:
                conexion.executescript(
                    (schema_dir / schema_name).read_text(encoding="utf-8")
                )
            finally:
                conexion.close()

    def test_missing_values_stay_missing_and_identifiers_are_parameterized(self):
        with db.conectar_dengue() as conexion:
            conexion.execute(
                "INSERT INTO laboratorios (id_paciente, plaquetas) VALUES (1, 42)"
            )
        with db.conectar_pacientes() as conexion:
            conexion.execute(
                "INSERT INTO pacientes (id_paciente, documento) VALUES (1, '123')"
            )
        self.assertIsNone(db.obtener_hipotension(1))
        self.assertEqual(db.obtener_plaquetas(1), 42.0)
        self.assertIsNone(db.obtener_fiebre(1))
        self.assertIsNone(db.obtener_id_paciente_por_documento("' OR 1=1 --"))
        with self.assertRaises(ValueError):
            db._obtener_valor(
                "laboratorios",
                "plaquetas; DROP TABLE pacientes",
                1,
                {"plaquetas"},
            )

    def test_local_geography_is_auditable_and_joins_patient_by_dane_code(self):
        db.guardar_geografia_municipio({
            "codigo_municipio": "05001",
            "departamento": "Antioquia",
            "municipio": "Medellín",
            "latitud": 6.24,
            "longitud": -75.57,
            "fuente_coordenadas": "Coordenadas oficiales del municipio",
            "fecha_verificacion": "2026-11-20",
        })
        with db.conectar_pacientes() as conexion:
            conexion.execute(
                """
                INSERT INTO pacientes (
                    id_paciente, municipio, departamento, codigo_municipio,
                    fecha_consulta
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (1, "Medellín", "Antioquia", "05001", "2026-11-20"),
            )

        paciente = db.obtener_contexto_paciente(1)

        self.assertEqual(paciente["latitud"], 6.24)
        self.assertEqual(paciente["longitud"], -75.57)
        self.assertEqual(
            paciente["geografia"]["fuente_coordenadas"],
            "Coordenadas oficiales del municipio",
        )

    def test_context_uses_nasa_and_caches_only_aggregated_weather(self):
        db.guardar_geografia_municipio({
            "codigo_municipio": "05001",
            "departamento": "Antioquia",
            "municipio": "Medellín",
            "latitud": 6.24,
            "longitud": -75.57,
            "fuente_coordenadas": "Fuente oficial",
            "fecha_verificacion": "2026-11-20",
        })
        with db.conectar_pacientes() as conexion:
            conexion.execute(
                """
                INSERT INTO pacientes (
                    id_paciente, municipio, departamento, codigo_municipio
                ) VALUES (1, 'Medellín', 'Antioquia', '05001')
                """
            )
        observacion = {
            "temperatura_media": 16.96,
            "humedad": 94.05,
            "precipitacion": 7.34,
            "fecha_referencia": "2026-01-01",
            "latitud": 6.24,
            "longitud": -75.57,
            "fuente": "NASA POWER",
            "unidades": {
                "temperatura_media": "C",
                "humedad": "%",
                "precipitacion": "mm/day",
            },
            "tiempo_fuente": "LST",
        }

        with patch.object(
            nasa_power,
            "obtener_observacion",
            return_value=observacion,
        ) as consulta:
            primero = contexto_territorial.obtener_contexto_territorial(
                id_paciente=1,
                fecha_referencia="2026-01-01",
            )
            segundo = contexto_territorial.obtener_contexto_territorial(
                id_paciente=1,
                fecha_referencia="2026-01-01",
            )

        self.assertEqual(consulta.call_count, 1)
        self.assertEqual(primero["clima"]["estado"], "observacion_externa")
        self.assertEqual(segundo["clima"]["estado"], "observacion_local")
        self.assertEqual(
            segundo["vigilancia_dengue"]["estado"],
            "sin_fuente_configurada",
        )
        self.assertIn("no determinan infección", primero["interpretacion"])

    def test_nasa_adapter_parses_documented_units_without_network_access(self):
        response_body = {
            "properties": {
                "parameter": {
                    "T2M": {"20260101": 16.96},
                    "RH2M": {"20260101": 94.05},
                    "PRECTOTCORR": {"20260101": 7.34},
                }
            },
            "header": {"fill_value": -999.0, "time_standard": "LST"},
            "parameters": {
                "T2M": {"units": "C"},
                "RH2M": {"units": "%"},
                "PRECTOTCORR": {"units": "mm/day"},
            },
        }
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps(
            response_body
        ).encode("utf-8")

        with patch(
            "Datos.proveedores.nasa_power.urlopen",
            return_value=response,
        ) as urlopen:
            datos = nasa_power.obtener_observacion(
                latitud=6.24,
                longitud=-75.57,
                fecha="2026-01-01",
            )

        self.assertEqual(datos["temperatura_media"], 16.96)
        self.assertEqual(datos["precipitacion"], 7.34)
        self.assertIn("latitude=6.24", urlopen.call_args.args[0].full_url)

    def test_location_without_local_coordinates_does_not_call_a_geocoder(self):
        resultado = contexto_territorial.obtener_contexto_territorial(
            ubicacion={
                "codigo_municipio": "05001",
                "departamento": "Antioquia",
                "municipio": "Medellín",
            },
            fecha_referencia="2026-11-20",
        )

        self.assertEqual(
            resultado["clima"]["estado"],
            "sin_coordenadas_locales",
        )
        self.assertEqual(
            resultado["vigilancia_dengue"]["estado"],
            "sin_fuente_configurada",
        )

    def test_existing_evaluate_endpoint_adds_context_without_sending_patient_data(self):
        db.guardar_geografia_municipio({
            "codigo_municipio": "05001",
            "departamento": "Antioquia",
            "municipio": "Medellín",
            "latitud": 6.24,
            "longitud": -75.57,
            "fuente_coordenadas": "Fuente oficial",
            "fecha_verificacion": "2026-11-20",
        })
        observacion = {
            "temperatura_media": 16.96,
            "humedad": 94.05,
            "precipitacion": 7.34,
            "fecha_referencia": "2026-01-01",
            "latitud": 6.24,
            "longitud": -75.57,
            "fuente": "NASA POWER",
            "unidades": {
                "temperatura_media": "C",
                "humedad": "%",
                "precipitacion": "mm/day",
            },
            "tiempo_fuente": "LST",
        }

        with patch.object(
            nasa_power,
            "obtener_observacion",
            return_value=observacion,
        ) as consulta:
            resultado = api.evaluar({
                "sintomas": {"fiebre": True},
                "ubicacion": {
                    "codigo_municipio": "05001",
                    "departamento": "Antioquia",
                    "municipio": "Medellín",
                },
                "fecha_referencia": "2026-01-01",
            })

        self.assertEqual(resultado["contexto_zona"]["clima"]["estado"], "observacion_externa")
        self.assertEqual(
            consulta.call_args.kwargs,
            {"latitud": 6.24, "longitud": -75.57, "fecha": "2026-01-01"},
        )


if __name__ == "__main__":
    unittest.main()
