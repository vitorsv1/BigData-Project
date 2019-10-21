USE red_soc_passaros;

ALTER TABLE post
MODIFY COLUMN  url varchar(1000);

ALTER TABLE visualizacao
DROP PRIMARY KEY;
ADD id_visualizacao int PRIMARY KEY auto_increment NOT NULL;


CREATE TABLE IF NOT EXISTS lugar (
id_lugar int auto_increment NOT NULL,
lugar varchar(32) UNIQUE KEY,
PRIMARY KEY (id_lugar)
);

CREATE TABLE IF NOT EXISTS marca_lugar (
id_lugar int,
id_post int,
primary key (id_lugar, id_post),
FOREIGN KEY (id_post) REFERENCES post(id_post),
FOREIGN KEY (id_lugar) REFERENCES lugar(id_lugar)
);