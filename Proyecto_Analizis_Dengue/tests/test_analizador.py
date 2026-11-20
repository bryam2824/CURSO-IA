import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from modelos.Analizador import CARACTERISTICAS, analizar_paciente
from modelos.entrenamiento_xgboost import _leer_dataset, _separar_por_paciente
from modelo_meta_dengue import calcular_riesgo_final


class AnalizadorTests(unittest.TestCase):
    def test_estimacion_local_expone_datos_faltantes_y_no_es_probabilidad(self):
        resultado = analizar_paciente(
            {"sintomas": {"fiebre": True, "cefalea": False}},
            model_path="modelo_inexistente.json",
        )

        self.assertEqual(resultado["estado"], "estimacion_orientativa")
        self.assertEqual(
            resultado["estimacion"]["indice_sintomas_reportados"],
            0.5,
        )
        self.assertIn("no es una probabilidad", resultado["estimacion"]["interpretacion"])
        self.assertIn("sintomas.mialgia", resultado["calidad_datos"]["campos_faltantes"])
        self.assertEqual(resultado["hallazgos"]["sintomas_informados"], 2)
        self.assertEqual(resultado["calidad_datos"]["campos_informados"], 2)
        self.assertEqual(resultado["calidad_datos"]["completitud_porcentaje"], 11.8)

    def test_sin_sintomas_no_fabrica_una_estimacion(self):
        resultado = analizar_paciente({}, model_path="modelo_inexistente.json")

        self.assertEqual(resultado["estado"], "datos_insuficientes")
        self.assertIsNone(resultado["estimacion"]["indice_sintomas_reportados"])

    def test_alarma_se_informa_por_separado_del_indice(self):
        resultado = analizar_paciente(
            {
                "sintomas": {"fiebre": True},
                "alarmas": {"sangrado": True},
                "laboratorios": {"plaquetas": 100000},
            },
            model_path="modelo_inexistente.json",
        )

        self.assertEqual(resultado["hallazgos"]["alarmas_presentes"], ["sangrado"])
        self.assertEqual(
            resultado["estimacion"]["indice_sintomas_reportados"],
            1.0,
        )
        self.assertEqual(resultado["hallazgos"]["laboratorios_recibidos"]["plaquetas"], 100000.0)

    def test_valores_invalidos_se_marcan_como_faltantes(self):
        resultado = analizar_paciente(
            {"sintomas": {"fiebre": "tal vez"}},
            model_path="modelo_inexistente.json",
        )

        self.assertIn("sintomas.fiebre", resultado["calidad_datos"]["campos_invalidos"])
        self.assertIn("sintomas.fiebre", resultado["calidad_datos"]["campos_faltantes"])
        self.assertEqual(resultado["estado"], "datos_insuficientes")

    def test_rechaza_secciones_con_formato_incorrecto(self):
        with self.assertRaises(ValueError):
            analizar_paciente({"sintomas": []})

    def test_modelo_candidato_no_se_carga_como_publicado(self):
        with TemporaryDirectory() as directorio:
            model_path = Path(directorio) / "candidato.json"
            model_path.write_text("{}", encoding="utf-8")
            model_path.with_suffix(".json.metadata.json").write_text(
                json.dumps(
                    {
                        "estado": "candidato_requiere_revision_clinica",
                        "caracteristicas_y_orden": list(CARACTERISTICAS),
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "candidato"):
                analizar_paciente({}, model_path=model_path)

    def test_particion_separa_pacientes_y_conserva_ambas_clases(self):
        etiquetas = [0, 0, 0, 0, 1, 1, 1, 1]
        pacientes = ["n1", "n2", "n3", "n4", "p1", "p2", "p3", "p4"]

        entrenamiento, prueba = _separar_por_paciente(
            etiquetas, pacientes, semilla=3, fraccion_prueba=0.25
        )
        pacientes_entrenamiento = {pacientes[i] for i in entrenamiento}
        pacientes_prueba = {pacientes[i] for i in prueba}

        self.assertFalse(pacientes_entrenamiento & pacientes_prueba)
        self.assertEqual({etiquetas[i] for i in prueba}, {0, 1})

    def test_csv_entrenamiento_admite_datos_ausentes_sin_imputarlos(self):
        with TemporaryDirectory() as directorio:
            csv_path = Path(directorio) / "casos.csv"
            encabezados = ["id_paciente", "dengue_confirmado", *CARACTERISTICAS]
            filas = [
                ["p1", "1", "si", *([""] * (len(CARACTERISTICAS) - 1))],
                ["p2", "0", "no", *([""] * (len(CARACTERISTICAS) - 1))],
            ]
            csv_path.write_text(
                ",".join(encabezados)
                + "\n"
                + "\n".join(",".join(fila) for fila in filas),
                encoding="utf-8",
            )

            caracteristicas, etiquetas, _ = _leer_dataset(csv_path)

        self.assertEqual(etiquetas, [1, 0])
        self.assertEqual(caracteristicas[0][0], 1.0)
        self.assertTrue(caracteristicas[0][1] != caracteristicas[0][1])


class AgregadorTests(unittest.TestCase):
    def test_riesgo_ambiental_no_se_convierte_en_riesgo_clinico(self):
        score, variable, componentes = calcular_riesgo_final(
            {"riesgo": 0.1},
            {"riesgo": 0.2},
            {"riesgo": 0.3},
            {"riesgo": 1.0},
        )

        self.assertEqual(score, 0.3)
        self.assertEqual(variable, "riesgo_laboratorio")
        self.assertEqual(componentes["riesgo_entorno"], 1.0)


if __name__ == "__main__":
    unittest.main()
