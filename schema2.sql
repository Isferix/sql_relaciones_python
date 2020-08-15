DROP TABLE IF EXISTS estudiante;

DROP TABLE IF EXISTS tutor;

CREATE TABLE tutor(
    [id] INTEGER PRIMARY KEY,
    [name] TEXT NOT NULL
);

CREATE TABLE estudiante(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] TEXT NOT NULL,
    [age] INTEGER NOT NULL,
    [grade] INTEGER NOT NULL,
    [fk_tutor_id] INTEGER NOT NULL REFERENCES tutor(id)
);