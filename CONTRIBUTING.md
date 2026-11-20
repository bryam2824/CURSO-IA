# Contributing Guide

## Introducción

Gracias por tu interés en contribuir a este proyecto.

Este sistema tiene como objetivo desarrollar una plataforma inteligente para la detección temprana del riesgo de dengue mediante el análisis integrado de:

- Síntomas clínicos.
- Resultados de laboratorio.
- Signos de alarma.
- Variables de entorno.
- Modelos de Machine Learning basados en XGBoost.

Actualmente el proyecto se encuentra en fase activa de desarrollo y experimentación.

## Autoría y finalidad social

El proyecto de origen es
[bryam2824/CURSO-IA](https://github.com/bryam2824/CURSO-IA). Toda copia o
trabajo derivado debe conservar la atribución, los avisos de autoría y
`license.md`; las contribuciones deben respetar la licencia social vigente.
No se deben presentar como propios los componentes preexistentes ni retirar
este aviso.

La licencia del repositorio es una licencia personalizada con restricciones
comerciales. La aceptación y alcance legal de esas restricciones pueden variar
según jurisdicción; no se promete que un aviso por sí solo impida una
infracción. Para despliegues o acuerdos institucionales, solicitar revisión
jurídica.

---

## Formas de contribuir

Se aceptan contribuciones en:

### Epidemiología

- Fuentes oficiales de vigilancia epidemiológica.
- Indicadores de riesgo.
- Variables de incidencia y prevalencia.

### Ciencias de Datos

- Ingeniería de características.
- Optimización de modelos XGBoost.
- Evaluación y validación de modelos.

### Desarrollo de Software

- Integración de APIs.
- FastAPI.
- Automatización de procesos.
- Optimización de arquitectura.
- Adaptadores de datos por municipio/territorio, sin incorporar lógica de
  proveedores externos en `apis/db.py` ni en el analizador clínico.

### Infraestructura

- Docker.
- CI/CD.
- Despliegues.
- Seguridad.

---

## Estándares de Código

### Python

- Seguir PEP8.
- Utilizar nombres descriptivos.
- Incluir documentación en funciones públicas.

Ejemplo:

def calcular\_riesgo\_laboratorio(datos):

    """

    Calcula el score de riesgo basado en resultados de laboratorio.

    """

    pass

---

## Estructura de Commits

Formato recomendado:

feat: nueva funcionalidad

fix: corrección de errores

docs: documentación

refactor: mejora interna de código

test: pruebas

Ejemplos:

feat: agregar modulo epidemiologico

fix: corregir calculo de score de plaquetas

docs: actualizar arquitectura del entorno

---

## Pull Requests

Antes de enviar un Pull Request:

- Verificar que el código funcione.
- Mantener compatibilidad con la arquitectura existente.
- Documentar cambios importantes.
- Agregar pruebas cuando aplique.
- Conservar la atribución y licencia original.
- Probar cada adaptador con fixtures; no requerir Internet para ejecutar las
  pruebas unitarias.

---

## Datos y Ética

No se deben subir:

- Datos clínicos reales identificables.
- Información sensible de pacientes.
- Credenciales.
- Archivos de configuración privados.

Toda información epidemiológica deberá provenir de fuentes oficiales o repositorios públicos autorizados.

Las fuentes y sus límites deben documentarse en
[DATA_SOURCE.md](./DATA_SOURCE.md). No enviar identificadores ni síntomas del
paciente a APIs externas.

