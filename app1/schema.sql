DROP TABLE IF EXISTS images; 

CREATE TABLE images ( 
    id INTEGER PRIMARY KEY,
    link VARCHAR UNIQUE NOT NULL, 
    elo INTEGER NOT NULL
);
