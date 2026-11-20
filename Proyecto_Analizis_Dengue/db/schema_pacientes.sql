CREATE TABLE IF NOT EXISTS pacientes (
    id_paciente INTEGER PRIMARY KEY,
    documento TEXT,
    nombre TEXT,
    edad INTEGER,
    sexo TEXT,
    municipio TEXT,
    departamento TEXT,
    codigo_municipio TEXT,
    zona TEXT,
    fecha_inicio_sintomas TEXT,
    fecha_consulta TEXT
);
