drop database if exists red_soc_passaros;
create database if not exists red_soc_passaros;
create table if not exists red_soc_passaros.usuario (
id_usuario int PRIMARY KEY auto_increment NOT NULL,
nick varchar(32) UNIQUE,
nome varchar(32),
sobrenome varchar(32),
email varchar(32),
cidade varchar(32)
);

create table if not exists red_soc_passaros.passaro (
id_passaro int auto_increment NOT NULL,
especie varchar(32) UNIQUE KEY,
PRIMARY KEY (id_passaro)
);

create table if not exists red_soc_passaros.preferencia (
id_usuario int NOT NULL,
id_passaro int NOT NULL,
PRIMARY KEY (id_usuario, id_passaro),
FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
FOREIGN KEY (id_passaro) REFERENCES passaro(id_passaro)
);

create table if not exists red_soc_passaros.post (
id_post int PRIMARY KEY auto_increment NOT NULL,
id_usuario int,
titulo varchar(32) NOT NULL,
texto text,
url varchar(32),
foreign key (id_usuario) references usuario(id_usuario)
);

create table if not exists red_soc_passaros.mençao (
id_post int,
id_usuario int,
PRIMARY KEY (id_post, id_usuario),
FOREIGN KEY (id_post) REFERENCES post(id_post),
FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

create table if not exists red_soc_passaros.marca_passaro (
id_passaro int,
id_post int,
primary key (id_passaro, id_post),
FOREIGN KEY (id_post) REFERENCES post(id_post),
FOREIGN KEY (id_passaro) REFERENCES passaro(id_passaro)
);

create table if not exists red_soc_passaros.visualizaçao (
id_post int,
id_usuario int,
aparelho varchar(32),
ip varchar(32),
browser varchar(32),
data_visualizaçao timestamp,
PRIMARY KEY (id_post, id_usuario),
FOREIGN KEY (id_post) REFERENCES post(id_post),
FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);
