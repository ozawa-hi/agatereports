\c agatereports;

CREATE TABLE photos (
  id SERIAL PRIMARY KEY,
  filename VARCHAR(45) NOT NULL
);

INSERT INTO photos (filename) VALUES ('./data/photo_1.jpg');
INSERT INTO photos (filename) VALUES ('./data/photo_2.jpg');
INSERT INTO photos (filename) VALUES ('./data/photo_3.jpg');
INSERT INTO photos (filename) VALUES ('./data/photo_4.jpg');
INSERT INTO photos (filename) VALUES ('./data/photo_5.jpg');

