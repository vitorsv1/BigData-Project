DROP DATABASE IF EXISTS red_soc_passaros;
CREATE DATABASE IF NOT EXISTS red_soc_passaros;
USE red_soc_passaros;

CREATE TABLE IF NOT EXISTS usuario (
id_usuario int PRIMARY KEY auto_increment NOT NULL,
nick varchar(32) NOT NULL UNIQUE,
nome varchar(32),
sobrenome varchar(32),
email varchar(32),
cidade varchar(32),
ativo tinyint default 1
);

CREATE TABLE IF NOT EXISTS passaro (
id_passaro int auto_increment NOT NULL,
especie varchar(32) UNIQUE KEY,
PRIMARY KEY (id_passaro)
);

CREATE TABLE IF NOT EXISTS preferencia (
id_usuario int NOT NULL,
id_passaro int NOT NULL,
PRIMARY KEY (id_usuario, id_passaro),
FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
FOREIGN KEY (id_passaro) REFERENCES passaro(id_passaro)
);


CREATE TABLE IF NOT EXISTS post (
id_post int PRIMARY KEY auto_increment NOT NULL,
id_usuario int,
ativo tinyint default 1,
titulo varchar(32) NOT NULL UNIQUE,
texto text,
url varchar(32),
foreign key (id_usuario) references usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS mencao (
id_post int,
id_usuario int,
PRIMARY KEY (id_post, id_usuario),
FOREIGN KEY (id_post) REFERENCES post(id_post),
FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS marca_passaro (
id_passaro int,
id_post int,
primary key (id_passaro, id_post),
FOREIGN KEY (id_post) REFERENCES post(id_post),
FOREIGN KEY (id_passaro) REFERENCES passaro(id_passaro)
);

CREATE TABLE IF NOT EXISTS visualizacao (
id_post int,
id_usuario int,
aparelho varchar(32),
ip varchar(32),
browser varchar(32),
data_visualizacao timestamp,
PRIMARY KEY (id_post, id_usuario),
FOREIGN KEY (id_post) REFERENCES post(id_post),
FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS usuario_post_like (
id_post int,
id_usuario int,
post_like varchar(32),
PRIMARY KEY (id_post, id_usuario),
FOREIGN KEY (id_post) REFERENCES post(id_post),
FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);
