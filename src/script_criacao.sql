drop database if exists red_soc_passaros;
create database if not exists red_soc_passaros;
create table if not exists red_soc_passaros.usuarios (
id int PRIMARY KEY auto_increment NOT NULL,
nome varchar(32),
sobrenome varchar(32),
email varchar(32),
cidade varchar(32)
);

create table if not exists red_soc_passaros.passaros (
id int auto_increment NOT NULL,
especie varchar(32) UNIQUE KEY,
PRIMARY KEY (id)
);

create table if not exists red_soc_passaros.preferencia (
id_usuarios int NOT NULL,
id_passaros int NOT NULL,
PRIMARY KEY (id_usuarios, id_passaros),
FOREIGN KEY (id_usuarios) REFERENCES usuarios(id),
FOREIGN KEY (id_passaros) REFERENCES passaros(id)
);

create table if not exists red_soc_passaros.post (
id int PRIMARY KEY auto_increment NOT NULL,
id_usuario int,
titulo varchar(32) NOT NULL,
texto text,
url varchar(32),
foreign key (id_usuario) references usuarios(id)
);

create table if not exists red_soc_passaros.mençao (
id_post int,
id_usuario int,
PRIMARY KEY (id_post, id_usuario),
FOREIGN KEY (id_post) REFERENCES post(id),
FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);

create table if not exists red_soc_passaros.marca_passaro (
id_passaro int,
id_post int,
primary key (id_passaro, id_post),
FOREIGN KEY (id_post) REFERENCES post(id),
FOREIGN KEY (id_passaro) REFERENCES passaros(id)
);

create table if not exists red_soc_passaros.visualizaçao (
id_post int,
id_usuario int,
aparelho varchar(32),
ip varchar(32),
browser varchar(32),
data_visualizaçao timestamp,
PRIMARY KEY (id_post, id_usuario),
FOREIGN KEY (id_post) REFERENCES post(id),
FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);