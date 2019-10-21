USE red_soc_passaros;

ALTER TABLE post
MODIFY COLUMN  url varchar(1000);

ALTER TABLE visualizacao DROP FOREIGN KEY visualizacao_ibfk_1;
ALTER TABLE visualizacao DROP FOREIGN KEY visualizacao_ibfk_2; 
ALTER TABLE visualizacao
DROP PRIMARY KEY;
ALTER TABLE visualizacao
add id_visualizacao int primary key auto_increment;


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

CREATE TABLE IF NOT EXISTS usuario_post_like (
id_post int,
id_usuario int,
post_like varchar(32),
PRIMARY KEY (id_post, id_usuario),
FOREIGN KEY (id_post) REFERENCES post(id_post),
FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);
