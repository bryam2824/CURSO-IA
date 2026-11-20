# Security Policy

## Supported Versions

Actualmente el proyecto se encuentra en fase de desarrollo activo y no dispone de versiones de producción oficialmente liberadas.

| Version | Supported |
| --- | --- |
| Development (main) | ✅ |
| Prototype 0.x | ✅ |
| Future Releases 1.x | 🔄 Planned |
| Legacy Builds | ❌ |

## Security Status

Este proyecto corresponde a un sistema de investigación y desarrollo para el análisis de riesgo de dengue mediante:

- Síntomas clínicos.
- Resultados de laboratorio.
- Signos de alarma.
- Variables de entorno.
- Modelos de Machine Learning basados en XGBoost.

Debido a que el proyecto se encuentra en desarrollo, algunas funcionalidades pueden estar sujetas a cambios frecuentes y aún no han sido sometidas a auditorías de seguridad completas.

## Reporting a Vulnerability

Si identifica una vulnerabilidad de seguridad, una exposición de datos o cualquier comportamiento que pueda comprometer la integridad del sistema, por favor reporte el incidente incluyendo:

- Descripción detallada de la vulnerabilidad.
- Pasos para reproducir el problema.
- Impacto potencial.
- Evidencia disponible (capturas de pantalla, registros o ejemplos).

Los reportes serán revisados y priorizados según:

- Riesgo para la confidencialidad de los datos.
- Riesgo para la integridad de los modelos.
- Riesgo para la disponibilidad del sistema.

## Security Considerations

Durante el desarrollo se recomienda:

- No almacenar información clínica real sin anonimización.
- Utilizar únicamente fuentes oficiales para datos epidemiológicos y ambientales.
- Validar todas las entradas provenientes de usuarios.
- Limitar el acceso a modelos entrenados y archivos de configuración.
- Mantener separados los entornos de desarrollo, pruebas y producción.
- Registrar cambios en modelos y conjuntos de datos utilizados para entrenamiento.

## Data Sources

Las variables utilizadas por el módulo de entorno deberán obtenerse preferiblemente de fuentes oficiales y verificables, tales como:

- Institutos meteorológicos nacionales.
- Sistemas de vigilancia epidemiológica.
- Institutos geográficos oficiales.
- Sistemas de datos abiertos gubernamentales.
- Organismos internacionales de salud pública.

## Disclaimer

Este software es un proyecto de investigación y desarrollo. Los resultados generados por el sistema no constituyen un diagnóstico médico y no deben utilizarse como única base para la toma de decisiones clínicas.

La clasificación de riesgo generada por los modelos tiene fines de apoyo analítico, investigación y vigilancia epidemiológica.

