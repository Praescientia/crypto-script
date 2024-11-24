CREATE TABLE data_source (
    sourceid INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

CREATE TABLE coin(
    coinid INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    crncy TEXT
);