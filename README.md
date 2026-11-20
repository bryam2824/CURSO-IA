# Sistema de Vigilancia, Detección y Análisis de Dengue

> **Proyecto social:** conservar la atribución al proyecto original y el aviso
> de licencia en las copias y trabajos derivados. La licencia `LUSSC v1.0`
> permite el uso por entidades públicas, educativas, sanitarias y de
> investigación, y restringe la explotación comercial privada no autorizada.
> Véase [license.md](./license.md). La aplicación no reemplaza el juicio
> clínico ni confirma un caso activo.

## Descripción

Este proyecto tiene como objetivo desarrollar una plataforma tecnológica para el análisis, monitoreo y detección temprana de factores asociados al dengue mediante técnicas de inteligencia artificial, aprendizaje automático, análisis epidemiológico y sistemas de automatización.

La arquitectura contempla la integración de redes neuronales, modelos predictivos, análisis estadístico, procesamiento de síntomas clínicos, variables ambientales, resultados de laboratorio y sistemas de comunicación mediante bots y APIs.

## Estado del Proyecto

Actualmente el proyecto se encuentra en proceso de rediseño y reestructuración arquitectónica.

Las funcionalidades, modelos y algoritmos disponibles representan versiones experimentales y de investigación. Ningún componente debe ser considerado una herramienta de diagnóstico médico ni utilizado como sustituto de la evaluación realizada por profesionales de la salud.

Durante el proceso de desarrollo se llevarán a cabo validaciones técnicas, científicas y epidemiológicas para determinar la viabilidad y precisión de los modelos implementados.

## Objetivos

- Apoyar la vigilancia epidemiológica.
- Facilitar el análisis de síntomas relacionados con dengue.
- Contribuir al desarrollo de herramientas tecnológicas para el sector salud.
- Fomentar la investigación científica y académica.
- Desarrollar sistemas de alerta temprana.
- Promover el acceso abierto al conocimiento médico y tecnológico.

## Enfoque Social

Este proyecto nace con una finalidad social, educativa, científica y sanitaria.

Su propósito principal es contribuir al bienestar colectivo mediante el desarrollo de herramientas que puedan fortalecer los procesos de investigación, prevención y vigilancia epidemiológica relacionados con el dengue y otras enfermedades transmitidas por vectores.

Se solicita respetar el espíritu de la iniciativa evitando usos que restrinjan, monopolicen o limiten el acceso a los beneficios derivados de este trabajo.

## Descargo de Responsabilidad

Este software se distribuye exclusivamente con fines educativos, científicos y de investigación.

Los desarrolladores no garantizan la exactitud de los resultados producidos por los modelos implementados y no asumen responsabilidad por decisiones médicas, clínicas, administrativas o de cualquier otra naturaleza que sean tomadas a partir de la información generada por el sistema.

La utilización de este software no sustituye el criterio de médicos, epidemiólogos, profesionales sanitarios o autoridades de salud pública.

## Uso local y sin conexión

El API analiza la información enviada directamente y no necesita conectarse a
servicios externos ni a las bases SQLite experimentales del repositorio. Usa
Python 3.10 o posterior.

Prepara las dependencias en un equipo conectado:

```powershell
python -m pip download -r requirements.txt -d ruedas
```

Transfiere el repositorio y `ruedas/` al equipo sin internet e instala desde el
directorio del proyecto:

```powershell
python -m pip install --no-index --find-links ..\ruedas -r ..\requirements.txt
python -m uvicorn apis.api:app --host 127.0.0.1 --port 8000
```

El archivo de ruedas debe corresponder al sistema operativo y versión de Python
del equipo de destino. El endpoint `POST /evaluar` acepta un JSON como:

```json
{
  "sintomas": {"fiebre": true, "cefalea": false},
  "laboratorios": {"plaquetas": 120000},
  "alarmas": {"sangrado": false}
}
```

Los campos omitidos se devuelven en `calidad_datos.campos_faltantes`; los
valores inválidos no se reemplazan por valores normales. Mientras no haya un
modelo local revisado, el sistema devuelve una proporción descriptiva de los
síntomas informados. **No es una probabilidad de dengue ni una clasificación
clínica.** Las alarmas se informan aparte. La herramienta es experimental y no
sustituye protocolos ni evaluación profesional.

## Entrenamiento XGBoost

El repositorio no incluye casos clínicos confirmados ni un modelo entrenado.
Cuando exista un dataset autorizado, desidentificado y con desenlace confirmado,
prepara un CSV con `id_paciente`, `dengue_confirmado` (0/1) y las variables
de `sintomas`, `laboratorios` y `alarmas` que admite el analizador. Las columnas
faltantes se permiten como celdas vacías; las filas sin desenlace verificable
no deben incluirse.

Desde `Proyecto_Analizis_Dengue/`, entrena un candidato local:

```powershell
python -m modelos.entrenamiento_xgboost casos_confirmados.csv
```

El candidato y sus metadatos/métricas de prueba quedan en
`modelos/candidatos/`; la partición de evaluación es por paciente, no una
validación temporal o externa. No se publica automáticamente. Requiere revisión
clínica y de datos antes de cambiar manualmente sus metadatos a
`aprobado_para_uso_experimental`. Renombra el artefacto a
`modelos/modelo_dengue_publicado.json` y sus metadatos a
`modelos/modelo_dengue_publicado.json.metadata.json`. Incluso así, su salida se
identifica como no validada para uso clínico.

Consulta [ARCHITECTURE.md](./ARCHITECTURE.md),
[DATA_SOURCE.md](./DATA_SOURCE.md) y [ROADMAP.md](./ROADMAP.md) para
limitaciones y gobierno de datos.




