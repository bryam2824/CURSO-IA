# ROADMAP

## Visión General

Desarrollar una plataforma inteligente de apoyo para la detección temprana del dengue mediante la integración de:

- Síntomas clínicos.
- Resultados de laboratorio.
- Signos de alarma.
- Factores ambientales.
- Variables geográficas.
- Indicadores epidemiológicos.
- Variables urbanísticas.
- Modelos de Machine Learning basados en XGBoost.

---

# Fase 1: Arquitectura Base

Estado: ✅ Completada

Objetivos:

- Definir estructura modular del proyecto.
- Implementar organizador de carpetas.
- Diseñar flujo principal de análisis.
- Crear módulos independientes.

Entregables:

- Sintomas/
- Laboratorios/
- Alarmas/
- Entorno/
- Resultado.py
- Analizador.py

---

# Fase 2: Motor Clínico

Estado: ✅ Completada

Objetivos:

- Implementar análisis de síntomas.
- Implementar análisis de laboratorios.
- Estandarizar scores clínicos.

Módulos:

## Síntomas

- Fiebre
- Cefalea
- Artralgia
- Mialgia
- Náuseas
- Vómitos
- Dolor retroocular
- Rash
- Sangrado

## Laboratorio

- Plaquetas
- Leucocitos
- Hematocrito
- Hemoglobina
- Neutrófilos

---

# Fase 3: Sistema de Alarmas

Estado: 🚧 En desarrollo

Objetivos:

- Consolidar signos de alarma.
- Generar score de gravedad.

Variables:

- Sangrado
- Hipotensión
- Somnolencia
- Alteración del estado general

Entregable:

Alarmas/

└── alarmas.py

---

# Fase 4: Módulo de Entorno

Estado: 🚧 En desarrollo

Objetivos:

- Analizar factores ambientales asociados al vector.

Estructura:

Entorno/

├── clima.py

├── geografia.py

├── epidemiologia.py

├── urbanismo.py

├── zona.py

└── xgboost\_entorno.py

---

## Submódulo Clima

Variables:

- Temperatura media
- Humedad relativa
- Precipitación

Fuentes objetivo:

- IDEAM
- NOAA
- NASA POWER

---

## Submódulo Geografía

Variables:

- Altitud
- Latitud
- Longitud
- Cercanía a cuerpos de agua

Fuentes objetivo:

- IGAC
- OpenStreetMap
- SRTM

---

## Submódulo Epidemiología

Variables:

- Casos semanales
- Casos mensuales
- Incidencia municipal
- Incidencia departamental

Fuentes objetivo:

- INS
- SIVIGILA
- Ministerio de Salud

---

## Submódulo Urbanismo

Variables:

- Densidad poblacional
- Acceso a agua potable
- Cobertura de alcantarillado
- Índice de hacinamiento

Fuentes objetivo:

- DANE
- Datos Abiertos Colombia

---

# Fase 5: Configuración de Zonas

Estado: 🚧 En desarrollo

Objetivos:

Permitir evaluación mediante:

- Departamento.
- Municipio.
- Coordenadas geográficas.
- Datos adicionales validados manualmente.

Casos de uso:

Zona(

    departamento="Antioquia",

    municipio="Rionegro"

)

o

Zona(

    latitud=6.15,

    longitud=\-75.37

)

---

# Fase 6: XGBoost de Entorno

Estado: 🚧 En desarrollo

Objetivo:

Generar un score de entorno basado en:

- Clima.
- Geografía.
- Epidemiología.
- Urbanismo.

Entradas:

[

    score\_clima,

    score\_geografico,

    score\_epidemiologico,

    score\_urbano

]

Salida:

score\_entorno

---

# Fase 7: Meta Modelo Dengue

Estado: ⏳ Planeada

Objetivo:

Fusionar todos los componentes mediante XGBoost.

Entradas:

[

    score\_sintomas,

    score\_laboratorio,

    score\_alarmas,

    score\_entorno

]

Salida:

probabilidad\_dengue

---

# Fase 8: Explicabilidad (XAI)

Estado: ⏳ Planeada

Objetivos:

- Identificar variables más influyentes.
- Interpretar decisiones del modelo.
- Incorporar SHAP.

Resultados esperados:

- Factor principal de riesgo.
- Ranking de importancia.
- Explicación automática.

---

# Fase 9: API de Producción

Estado: ⏳ Planeada

Objetivos:

- Exponer servicios mediante FastAPI.
- Validar entradas.
- Documentar endpoints.

Funciones:

- Análisis individual.
- Consulta de entorno.
- Generación de reportes.

---

# Fase 10: Integración con Telegram

Estado: ⏳ Planeada

Objetivos:

- Captura de datos desde Telegram.
- Consulta rápida de riesgo.
- Notificación de alertas.

---

# Fase 11: Dashboard Epidemiológico

Estado: ⏳ Planeada

Objetivos:

- Visualizar zonas de riesgo.
- Visualizar tendencias.
- Mostrar indicadores del entorno.

Tecnologías evaluadas:

- Plotly
- Dash
- Power BI
- Grafana

---

# Fase 12: Validación Científica

Estado: ⏳ Planeada

Objetivos:

- Comparar resultados con casos reales.
- Medir precisión.
- Medir sensibilidad.
- Medir especificidad.
- Ajustar modelos.

Indicadores esperados:

- Accuracy
- Recall
- Precision
- F1 Score
- ROC\-AUC

---

# Fase 13: Preparación para Producción

Estado: ⏳ Planeada

Objetivos:

- Dockerización.
- Auditoría de seguridad.
- Monitoreo.
- Registro de eventos.
- Versionamiento de modelos.

---

# Meta Final

Construir una plataforma modular, escalable y explicable para apoyo a la detección temprana del dengue, combinando información clínica, epidemiológica, geográfica y ambiental mediante inteligencia artificial y fuentes oficiales de datos.

---

# Fases para aprendizaje controlado

## Fase 14: Contratos de datos y procedencia

Definir esquemas versionados para observaciones externas, variables clínicas, desenlaces y documentos. Registrar origen, fecha, cobertura, licencia, unidad, controles de calidad y linaje de cada dato.

**Criterio de salida:** cada dato procesado puede rastrearse hasta su fuente y periodo; los errores de API y datos faltantes no se convierten en valores ficticios.

## Fase 15: Conectores y almacenamiento

Implementar conectores individuales para fuentes oficiales priorizadas, empezando por una fuente y un caso de uso verificable. Separar almacenamiento bruto, normalizado y clínico; agregar timeout, límites, reintentos controlados y monitoreo.

**Criterio de salida:** pruebas de contrato con respuestas reales anonimizadas o fixtures versionados, y documentación de cobertura, límites y calidad de la fuente.

## Fase 16: Biblioteca de conocimiento documental

Crear catálogo de documentos autorizados/versionados e indexación para recuperación de fragmentos con citas. Revisar vigencia, jurisdicción y licencia; no entrenar el clasificador a partir de texto de guías ni permitir que una respuesta generada cambie decisiones clínicas.

**Criterio de salida:** toda respuesta documental puede citar título, versión/fecha y fragmento de origen; las fuentes vencidas se identifican y retiran.

## Fase 17: Dataset de desenlaces confirmados

Establecer gobernanza, desidentificación, definición de caso y etiqueta clínica verificable; preparar diccionario de datos, controles de calidad y partición por paciente/tiempo/centro.

**Criterio de salida:** revisión de privacidad y aprobación clínica/epidemiológica del protocolo y dataset antes de entrenar.

## Fase 18: Entrenamiento candidato y evaluación

Entrenar de forma reproducible fuera del flujo de predicción. Registrar código, datos, características, hiperparámetros, métricas, limitaciones y artefacto. Evaluar sensibilidad, especificidad, valores predictivos, calibración, intervalos y subgrupos; comparar con una línea base y validación externa.

**Criterio de salida:** criterios de aceptación predefinidos cumplidos y revisión humana documentada. El entrenamiento nunca publica automáticamente un modelo.

## Fase 19: Publicación, monitoreo y reversión

Versionar y aprobar manualmente cada modelo, monitorear deriva y calidad de datos, auditar cambios y conservar la posibilidad de volver a la versión anterior. Deshabilitar uso clínico si falla la calidad, la calibración o la disponibilidad de datos críticos.

**Criterio de salida:** modelo, dataset y parámetros reproducibles; responsables de aprobación y procedimiento de reversión identificados.

