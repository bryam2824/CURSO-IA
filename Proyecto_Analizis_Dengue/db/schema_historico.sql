CREATE TABLE IF NOT EXISTS clima (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio TEXT,
    departamento TEXT,
    municipio TEXT,
    fecha_referencia TEXT,
    temperatura_media REAL,
    humedad REAL,
    precipitacion REAL,
    fuente TEXT NOT NULL,
    fecha_consulta_utc TEXT NOT NULL,
    UNIQUE (codigo_municipio, fecha_referencia, fuente)
);

CREATE TABLE IF NOT EXISTS epidemiologia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio TEXT,
    departamento TEXT,
    municipio TEXT,
    incidencia_semanal REAL,
    incidencia_mensual REAL,
    brote_activo INTEGER,
    tendencia_epidemiologica TEXT,

    casos_graves INTEGER,

    fecha_referencia TEXT,
    fuente TEXT,
    fecha_consulta_utc TEXT
);

CREATE TABLE IF NOT EXISTS geografia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio TEXT UNIQUE,
    departamento TEXT,
    municipio TEXT,
    latitud REAL CHECK (latitud IS NULL OR latitud BETWEEN -90 AND 90),
    longitud REAL CHECK (longitud IS NULL OR longitud BETWEEN -180 AND 180),
    altitud REAL,

    cercania_cuerpos_agua REAL,

    pendiente REAL,
    fuente_coordenadas TEXT,
    fecha_verificacion TEXT
);

CREATE TABLE IF NOT EXISTS urbanismo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_municipio TEXT UNIQUE,
    departamento TEXT,
    municipio TEXT,
    densidad_poblacional REAL,
    acceso_agua_potable REAL,
    recoleccion_basuras REAL,

    infraestructura_sanitaria REAL
);

CREATE TABLE IF NOT EXISTS vigilancia_dengue (
    codigo_municipio TEXT NOT NULL,
    departamento TEXT NOT NULL,
    municipio TEXT NOT NULL,
    periodo_inicio TEXT NOT NULL,
    periodo_fin TEXT NOT NULL,
    casos_probables INTEGER CHECK (casos_probables IS NULL OR casos_probables >= 0),
    casos_confirmados INTEGER CHECK (casos_confirmados IS NULL OR casos_confirmados >= 0),
    casos_graves INTEGER CHECK (casos_graves IS NULL OR casos_graves >= 0),
    fuente TEXT NOT NULL,
    id_conjunto_datos TEXT,
    fecha_publicacion TEXT,
    fecha_consulta_utc TEXT NOT NULL,
    licencia TEXT,
    PRIMARY KEY (codigo_municipio, periodo_inicio, periodo_fin, fuente)
);

CREATE TABLE IF NOT EXISTS zona (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    municipio TEXT,
    zona TEXT,
    riesgo_historico REAL,
    observaciones TEXT
);
