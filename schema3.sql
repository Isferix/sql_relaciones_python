DROP TABLE IF EXISTS autor;

DROP TABLE IF EXISTS libro;

CREATE TABLE autor(
    [id] INTEGER PRIMARY KEY,
    [author] STRING NOT NULL
);

CREATE TABLE libro(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [title] STRING NOT NULL,
    [pags] INTEGER NOT NULL,
    [fk_author_id] INTEGER NOT NULL REFERENCES autor(id)
);
