CREATE TABLE data_source (
    sourceid INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

CREATE TABLE asset_type(
    assetid INTEGER PRIMARY KEY AUTOINCREMENT,
    coin TEXT,
    crncy TEXT
);