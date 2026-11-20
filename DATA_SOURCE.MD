# Data Sources

## Objetivo

Este documento describe las fuentes oficiales y verificables utilizadas para alimentar los módulos del sistema.

El uso de fuentes oficiales es obligatorio para garantizar la calidad y trazabilidad de los datos.

---

# Entorno

## Clima

Variables:

- Temperatura media.
- Temperatura máxima.
- Temperatura mínima.
- Humedad relativa.
- Precipitación.

Fuentes sugeridas:

- IDEAM.
- NOAA.
- NASA POWER.
- Copernicus Climate Data Store.

---

## Geografía

Variables:

- Altitud.
- Latitud.
- Longitud.
- Cercanía a cuerpos de agua.
- Índices de vegetación.

Fuentes sugeridas:

- IGAC.
- OpenStreetMap.
- NASA SRTM.
- Copernicus Land Monitoring Service.

---

## Epidemiología

Variables:

- Casos por municipio.
- Casos por departamento.
- Casos semanales.
- Casos mensuales.
- Tasas de incidencia.

Fuentes sugeridas:

- Instituto Nacional de Salud (INS).
- SIVIGILA.
- Ministerio de Salud.
- Organización Panamericana de la Salud.
- Organización Mundial de la Salud.

---

## Urbanismo

Variables:

- Densidad poblacional.
- Cobertura de agua potable.
- Cobertura de alcantarillado.
- Índice de hacinamiento.
- Gestión de residuos.

Fuentes sugeridas:

- DANE.
- Datos Abiertos Colombia.
- Planeación Municipal.
- Alcaldías locales.

---

# Datos Clínicos

## Síntomas

Variables:

- Fiebre.
- Cefalea.
- Artralgia.
- Mialgia.
- Náuseas.
- Vómitos.
- Rash.
- Sangrado.
- Dolor retroocular.

Origen:

- Personal médico.
- Sistemas clínicos.
- Formularios de captura.

---

## Laboratorios

Variables:

- Plaquetas.
- Leucocitos.
- Hematocrito.
- Hemoglobina.
- Neutrófilos.

Origen:

- Laboratorios clínicos.
- Sistemas hospitalarios.

---

## Alarmas

Variables:

- Sangrado.
- Hipotensión.
- Somnolencia.

Origen:

- Evaluación clínica.
- Historia médica.

---

# Principios de Calidad

Todos los datos deberán cumplir:

- Fuente verificable.
- Fecha de actualización identificable.
- Trazabilidad.
- Validación previa al procesamiento.
- Almacenamiento seguro.
- Cumplimiento de normativas de protección de datos.

---

# Estado Actual

Actualmente algunas integraciones con fuentes oficiales se encuentran en fase de diseño y desarrollo.

Las futuras versiones incorporarán conectores automáticos para la consulta y actualización periódica de datos epidemiológicos, geográficos y ambientales.

---

# Ingesta para aprendizaje y conocimiento

## Separación de conjuntos de datos

Los datos se almacenarán por propósito y no se mezclarán como si tuvieran el mismo significado:

1. **Datos brutos de fuente:** respuesta original, fuente, URL o identificador, fecha de captura, periodo de referencia, ubicación, licencia y hash.
2. **Datos normalizados:** valores validados con unidades, códigos geográficos, zona horaria, reglas de calidad y referencia al registro bruto.
3. **Casos clínicos etiquetados:** variables clínicas mínimas necesarias y desenlace confirmado, método/fecha de confirmación y procedencia autorizada. Deben estar desidentificados o seudonimizados y contar con base legal y controles de acceso.
4. **Documentación:** archivos o páginas con metadatos de autoría, institución, fecha, versión, jurisdicción, licencia y hash. Se indexan para búsqueda y recuperación con citas, no como etiquetas de entrenamiento.

Las APIs de clima y vigilancia pueden enriquecer características temporales o geográficas. No deben utilizarse para inferir el diagnóstico individual ni para generar etiquetas clínicas. Ningún identificador personal se enviará a esas APIs.

## Contrato de calidad para cada conector

Antes de habilitar una fuente, documentar:

- Propietario, endpoint/conjunto de datos, licencia, términos y contacto.
- Cobertura geográfica y temporal, frecuencia de actualización y retraso de publicación.
- Esquema, unidades, códigos, resolución espacial y semántica de cada campo.
- Límites de uso, autenticación, timeout, reintentos y política ante indisponibilidad.
- Validaciones de rango, duplicados, faltantes, cambios de esquema y controles de consistencia temporal.
- Procedimiento de versionado, auditoría y corrección de datos.

Los fallos de consulta deben quedar visibles como datos no disponibles; no se reemplazan por valores por defecto que aparenten ser observaciones reales.

## Documentación de conocimiento

Priorizar guías clínicas y epidemiológicas oficiales vigentes de OMS/OPS, INS y Ministerio de Salud de Colombia, además de documentación técnica de los proveedores de datos. Registrar fecha de consulta, versión, región aplicable y licencia. Revisar cambios de guías antes de publicarlos en el índice de conocimiento.

La respuesta basada en documentos debe conservar citas recuperables al documento y fragmento de origen. El contenido recuperado sirve para consulta informativa; no actualiza automáticamente el modelo predictivo.

## Desenlaces para entrenamiento

Para entrenar un predictor individual se requieren etiquetas definidas por protocolo y confirmadas por una fuente autorizada. Deben registrarse la definición de caso, método diagnóstico, fechas relevantes y resolución del caso. Excluir registros sin desenlace verificable del entrenamiento supervisado; mantenerlos, si corresponde, en análisis descriptivos claramente separados.

La separación de entrenamiento/validación/prueba debe evitar que observaciones de una misma persona o periodos futuros filtren información al entrenamiento. La evaluación debe reportar sensibilidad, especificidad, valores predictivos, calibración, intervalos de incertidumbre y desempeño por subgrupos y ubicación.

## Estado de integración

- `Datos/proveedores/nasa_power.py` consulta la API diaria de NASA POWER para
  temperatura media, humedad relativa y precipitación. La consulta requiere
  coordenadas verificadas guardadas localmente; no geocodifica ni transmite
  nombre, documento, síntomas o `id_paciente`.
- `Datos/configuracion_fuentes.json` selecciona proveedores por código DANE.
  NASA POWER es la opción climática por defecto; no hay proveedor
  epidemiológico configurado.
- Las bases locales pueden cachear la respuesta junto con fuente, fecha,
  unidades y referencia territorial. Una falla de red aparece como no
  disponible, no como valores cero.
- No se identificó un API nacional de SIVIGILA que entregue indicadores
  municipales actuales en un esquema uniforme. El catálogo de datos abiertos
  contiene conjuntos distintos por territorio: Bucaramanga (`qzc7-jbg3`, con
  última actualización de filas reportada en noviembre de 2025), Caquetá
  (`fhz2-4x64`, octubre de 2024) y Medellín (`ke8u-qixu`, enlace federado a un
  CSV cuya última actualización indicada es de 2023). No se deben presentar
  como vigilancia nacional en tiempo real ni como fuente de casos activos en
  noviembre de 2026.

El API no concluye que un paciente tenga dengue, ni que haya un caso activo
individual. Solo puede devolver observaciones climáticas y, cuando se
configure un proveedor territorial vigente, conteos oficiales agregados con su
periodo y procedencia. La decisión clínica corresponde al profesional.

## Fuentes iniciales recomendadas y adecuación

La fuente debe elegirse según el objetivo; no existe una única base que sirva
para entrenar vigilancia territorial, infección individual y gravedad clínica.
La reputación institucional tampoco significa que sus datos estén validados
para cualquier modelo o que puedan reutilizarse sin condiciones.

| Fuente | Uso inicial razonable | Lo que no permite concluir por sí sola |
|---|---|---|
| [INS Colombia: informes y tableros de eventos](https://www.ins.gov.co/buscador-eventos/Paginas/Info-Evento.aspx?Event=13) | Describir vigilancia de dengue en Colombia por evento y periodo; revisar boletines y cobertura antes de descargar o transcribir. | No asumir acceso a registros clínicos individuales ni usar conteos agregados como etiqueta de infección por paciente. Verificar licencia, formato y nivel geográfico de cada producto. |
| [CDC: datos y estadísticas de dengue](https://www.cdc.gov/dengue/data-research/facts-stats/index.html) | Ejemplo documentado de datos actuales e históricos de vigilancia de EE. UU.; página consultada indica datos históricos desde 2010 y menciona ArboNET. | No representa automáticamente Colombia: difieren población, vigilancia, exposición, definiciones y contexto sanitario. |
| [NASA POWER Data Access Viewer](https://power.larc.nasa.gov/data-access-viewer/) | Obtener covariables meteorológicas/ambientales para análisis espacio-temporal, registrando coordenadas, escala y periodo. | No es una fuente de casos confirmados de dengue ni una etiqueta clínica. Comparar resolución y sesgo con observaciones locales. |
| Cohorte clínica autorizada de hospital/universidad o entidad de salud | Entrenar un modelo individual únicamente si contiene predictores medidos antes del momento de predicción y desenlaces clínicos con definición y confirmación verificables. | La existencia de una publicación no concede acceso a sus datos individuales. Se requieren permisos, revisión ética/legal y condiciones de uso; los datos agregados no sustituyen esta cohorte. |

### Recomendación para este repositorio

1. Para comenzar sin datos clínicos, usar boletines del INS para análisis
   descriptivo de vigilancia municipal/temporal y NASA POWER o IDEAM solo para
   enriquecer covariables ambientales. Mantener el producto como análisis
   poblacional, no como detector de casos individuales.
2. Para entrenar `dengue_confirmado` a nivel de paciente, primero obtener un
   conjunto autorizado, desidentificado y documentado con positivos
   confirmados y controles comparables. Para predecir gravedad, definir un
   desenlace de gravedad por separado. No mezclar ambos objetivos.
3. Antes de importar, registrar acceso y licencia, jurisdicción, periodo,
   definición de caso, método de confirmación, unidad de análisis, variables,
   unidades, faltantes, duplicados, sesgo de selección y posibles fugas
   temporales. Dividir evaluación por paciente y tiempo/centro.
4. No incorporar datos reales de pacientes al repositorio Git ni a APIs
   externas. El entrenador actual solo crea un candidato y su partición
   aleatoria por paciente no constituye validación temporal o externa.

### Estado de las bases locales

Los archivos `db/dengue.db`, `db/historico.db` y `db/pacientes.db` se
reconstruyeron como SQLite válidas desde los esquemas
`db/schema_dengue.sql`, `db/schema_historico.sql` y
`db/schema_pacientes.sql`. Se mantienen vacías: no se añadieron datos de INS,
CDC, NASA ni historias clínicas. `geografia` admite código DANE, coordenadas,
fuente y fecha de verificación para un mapeo local revisado. Los campos de
alarma no tienen valor por defecto; un campo no registrado sigue siendo
desconocido, no “ausente”.

`pacientes.db` incluye columnas para documento y nombre por compatibilidad con
el esquema anterior. No almacenar datos identificables reales allí hasta
definir controles de acceso, cifrado, base legal, retención y exclusión del
control de versiones. `POST /evaluar` consulta los datos clínicos locales si
recibe `id_paciente`; si recibe `ubicacion`, agrega contexto territorial y puede
consultar el proveedor configurado para esa zona. Sin esos campos, conserva el
flujo JSON existente y no consulta las bases ni la red.

## Cómo agregar un proveedor sin cambiar el flujo clínico

1. Implementar un adaptador en `Proyecto_Analizis_Dengue/Datos/proveedores/`
   que cumpla el contrato pertinente de `proveedores/contratos.py`.
2. Registrarlo en `Datos/registro_proveedores.py`.
3. Seleccionarlo en `Datos/configuracion_fuentes.json`, por código DANE de
   cinco dígitos. La configuración admite una fuente distinta por municipio.
4. Probar respuesta, unidades, atribución, límites, disponibilidad y
   procedencia con fixtures locales. No incluir consultas de red en las
   pruebas unitarias.
5. Si es fuente epidemiológica, devolver solo datos agregados; guardar
   conjunto, territorio, periodo, fecha de publicación/consulta y licencia.
   No usar filas de personas para producir “casos activos” ni transferirlas a
   otra fuente.

`apis/db.py` es el repositorio local y no debe contener clientes HTTP ni
reglas específicas de un proveedor. Los adaptadores externos se reemplazan o
configuran sin modificar el endpoint de evaluación ni añadir análisis clínico.

Las páginas enlazadas fueron consultadas el 20 de noviembre de 2026 como
orientación de procedencia. Revalidar URL, versión, condiciones de acceso,
licencia y cobertura antes de cada extracción; una página institucional no
garantiza que un archivo concreto sea descargable, abierto o apropiado para
entrenamiento.

