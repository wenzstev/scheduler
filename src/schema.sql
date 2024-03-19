DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS appointment;
DROP TABLE IF EXISTS clientproviderrelationship;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname VARCHAR (50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    is_provider bool default FALSE,
    password VARCHAR(250) NOT NULL
);

CREATE TABLE appointment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    starttime TIMESTAMPTZ,
    endtime TIMESTAMPTZ,
    provider_id INTEGER NOT NULL,
    client_id INTEGER,
    is_confirmed bool default false,
    FOREIGN KEY (provider_id) REFERENCES user(id),
    FOREIGN KEY (client_id) REFERENCES user(id)
);

--CREATE TABLE clientproviderrelationship (
--    client_id INTEGER NOT NULL,
--    provider_id INTEGER NOT NULL, 
--    PRIMARY KEY (client_id, provider_id),
--    FOREIGN KEY (client_id) REFERENCES user(id),
--    FOREIGN KEY (provider_id) REFERENCES user(id)
--);
