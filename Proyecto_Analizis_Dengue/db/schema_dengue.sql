CREATE TABLE IF NOT EXISTS alarmas (
    id_paciente INTEGER PRIMARY KEY,
    dolor_abdominal INTEGER,
    hipotension INTEGER,
    sangrado INTEGER,
    somnolencia INTEGER,
    fecha_registro TEXT
);

CREATE TABLE IF NOT EXISTS sintomas (
    id_paciente INTEGER PRIMARY KEY,
    artralgia TEXT,
    cefalea TEXT,
    mialgia TEXT,
    retroocular TEXT,
    rash TEXT,
    sangrado TEXT,
    nauseas INTEGER,
    vomitos INTEGER,
    fiebre REAL,
    fecha_registro TEXT
);

CREATE TABLE IF NOT EXISTS laboratorios (
    id_paciente INTEGER PRIMARY KEY,
    hematocrito REAL,
    hemoglobina REAL,
    leucocitos REAL,
    neutrofilos REAL,
    plaquetas REAL,
    fecha_laboratorio TEXT
);
