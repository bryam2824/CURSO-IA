# System Architecture

## Descripción General

El flujo activo de la API es local y recibe un caso en `POST /evaluar`. No
consulta internet ni necesita las bases SQLite de prototipo. XGBoost es un
componente opcional: solo se carga un artefacto local junto con metadatos que
declaren su aprobación experimental. No se distribuye un modelo entrenado.

El agregador histórico `modelo_meta_dengue.py` se mantiene separado; el riesgo
ambiental se conserva como contexto y ya no puede elevar el resultado clínico.
Ni el índice descriptivo ni un candidato XGBoost deben interpretarse como una
probabilidad clínica validada.

---

## Arquitectura General

```text
Profesional / sistema local
            │
            ▼
      POST /evaluar
            │
            ▼
 modelos/Analizador.py ──> faltantes, inválidos, hallazgos y alarmas
            │
            ├── Sin modelo publicado: índice descriptivo no probabilístico
            └── Con artefacto local: salida XGBoost experimental
```

---

## Módulo de Síntomas

Ubicación:

```text
modelos/Sintomas/
```

Responsabilidad:

- Evaluar síntomas individuales.
- Generar score de síntomas.

Variables:

- Fiebre.
- Cefalea.
- Mialgia.
- Artralgia.
- Dolor retroocular.
- Náuseas.
- Vómitos.
- Rash.
- Sangrado.

Salida:

```python
score_sintomas
```

---

## Módulo de Laboratorios

Ubicación:

```text
modelos/Laboratorios/
```

Variables:

- Plaquetas.
- Leucocitos.
- Hematocrito.
- Hemoglobina.
- Neutrófilos.

Salida:

```python
score_laboratorio
```

---

## Módulo de Alarmas

Ubicación:

```text
modelos/Alarmas/
```

Variables:

- Sangrado.
- Hipotensión.
- Somnolencia.
- Dolor abdominal

Salida:

```python
score_alarmas
```

---

## Módulo de Entorno

Ubicación:

```text
Entorno/
```

Estructura:

```text
Entorno/

├── zona.py
├── clima.py
├── geografia.py
├── epidemiologia.py
├── urbanismo.py
└── xgboost_entorno.py
```

Salida:

```python
score_entorno
```

---

## Agregador histórico y modelo opcional

El agregador histórico recibe:

```python
score_sintomas
score_laboratorio
score_alarmas
score_entorno
```

Selecciona el mayor de los componentes clínicos. El riesgo ambiental se
presenta como contexto y no participa en el máximo clínico. Su salida **no
es** una probabilidad individual de dengue y los umbrales no están validados.

El modelo XGBoost puede estimar el desenlace etiquetado en los casos locales
solo si existe un artefacto aprobado para uso experimental. La idoneidad
ambiental y la incidencia poblacional se mantienen separadas.

Una salida de modelo solo se habilita al validar localmente el artefacto y su
esquema. Actualmente no hay modelo distribuido:

```python
probabilidad_modelo_no_validada
```

---

## Arquitectura de aprendizaje y actualización

El aprendizaje se separa en tres flujos, que no deben confundirse:

```text
Fuentes externas oficiales ──> Ingesta ──> Datos brutos inmutables
                                          └─> Datos normalizados y validados
Documentación revisada ──────> Catálogo versionado ──> Recuperación con citas
Casos con desenlace confirmado ──────────> Dataset etiquetado ──> Entrenamiento candidato
                                                                  │
                                  Evaluación temporal y externa ──┤
                                                                  ▼
                                                   Revisión/aprobación humana
                                                                  │
                                                                  ▼
                                                   Versión publicada del modelo
```

### Ingesta de datos

- Los conectores consultan fuentes públicas autorizadas y guardan fuente, fecha de consulta, periodo cubierto, ubicación, unidad y versión del esquema.
- La respuesta original se conserva separada de los datos limpios; los errores, faltantes y cambios de esquema se reportan, no se sustituyen por valores inventados.
- Los datos ambientales y epidemiológicos agregados describen contexto poblacional. No son etiquetas de infección de una persona.
- Los datos clínicos identificables no se envían a proveedores de APIs externas.

### Conocimiento documental

- Se admiten documentos autorizados y revisados, con título, autor/institución, fecha, jurisdicción, versión, licencia y hash.
- La recuperación de fragmentos relevantes (RAG) aporta contexto y citas; no modifica por sí sola los pesos ni las reglas del predictor.
- Una respuesta generada debe identificar sus fuentes y fecha, y no presentarse como diagnóstico ni reemplazar protocolos clínicos vigentes.
- Documentos obsoletos, duplicados o sin procedencia verificable se ponen en cuarentena.

### Aprendizaje predictivo

- El modelo solo aprende de ejemplos con desenlace clínico definido y etiqueta verificable, no de texto documental ni de predicciones anteriores del propio modelo.
- Cada entrenamiento produce un candidato versionado y reproducible. Se evalúa con particiones por paciente y tiempo, evitando fuga de información; se documentan sensibilidad, especificidad, valor predictivo, calibración y desempeño por subgrupos.
- Ningún candidato reemplaza al modelo publicado hasta superar criterios predefinidos, validación externa y aprobación de responsables clínicos y de datos.
- La idoneidad ambiental del vector, el riesgo de infección y la gravedad clínica son resultados distintos y deben exponerse por separado. Los signos de alarma requieren una ruta de atención clínica independiente del score predictivo.

## Brechas conocidas del prototipo

- `Datos/variables_climaticas.py` todavía no implementa un proveedor climático.
- No se dispone en el repositorio de un conjunto de entrenamiento con desenlaces clínicos confirmados; el flujo candidato no realiza validación temporal o externa.
- Las puntuaciones y umbrales existentes son experimentales; no están validados para estimar probabilidades clínicas.
- Los modelos de los módulos históricos aún no están integrados con el endpoint local nuevo.

## Operación local, datos faltantes y aprendizaje

- La API activa no realiza consultas de red. Sus resultados son reproducibles a
  partir del JSON recibido y del artefacto XGBoost local, si existe.
- Los campos opcionales omitidos aparecen en `calidad_datos`; los valores
  inválidos también se identifican y nunca se convierten en valores normales.
- Sin XGBoost publicado, el índice corresponde únicamente a la proporción de
  síntomas reportados marcados como presentes. No es riesgo ni probabilidad de
  dengue. Laboratorios se muestran como recibidos, sin inventar unidades,
  rangos de referencia o diagnósticos.
- Las alarmas se muestran fuera del índice. La aplicación no determina
  tratamiento; se deben aplicar los protocolos clínicos locales.
- `modelos/entrenamiento_xgboost.py` crea un candidato desde casos confirmados,
  informa exactitud, sensibilidad y especificidad en un holdout agrupado por
  paciente, guarda hash/versiones y nunca lo publica automáticamente. No
  reemplaza la necesaria validación temporal, externa, calibración ni revisión
  clínica.
- Para ejecutar sin internet, instala previamente las dependencias desde un
  paquete local compatible con el sistema operativo y Python de destino. El
  uso de XGBoost en inferencia exige que su artefacto aprobado esté disponible
  en disco.

---

## Resultado

La API devuelve hallazgos observados, campos faltantes e inválidos, y
advertencias. Sin modelo publicado, `indice_sintomas_reportados` es una
proporción descriptiva, no una probabilidad ni una clase clínica. Ejemplo
reducido:

```json
{
  "estado": "estimacion_orientativa",
  "estimacion": {
    "metodo": "indice_descriptivo_no_validado",
    "indice_sintomas_reportados": 0.5
  },
  "calidad_datos": {
    "campos_faltantes": ["sintomas.mialgia"]
  }
}
```