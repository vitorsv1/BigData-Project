import io, json, logging, os, os.path, subprocess, re, unittest, pymysql

connection = pymysql.connect(
    host='localhost',
    user='megadados',
    password='megadados2019',
    database='red_soc_passaros')

# Adiciona um usuario
def adiciona_usuario(conn, nick, nome, sobrenome, email, cidade):
    query = """
    INSERT INTO usuario (nick, nome, sobrenome, email, cidade) 
    VALUES (%s, %s, %s, %s, %s);
    """
    with conn.cursor() as cursor:
        try:
            cursor.execute(query, (nick, nome,sobrenome,email,cidade))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela usuario')

#Acha um usuario pelo Nick
def acha_usuario(conn, nick):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuario WHERE nick = %s', (nick))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

#Desativa um usuário
def desativa_usuario(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('UPDATE usuario SET ativo=0 WHERE id_usuario=%s', (id))
    
#Muda nick de um usuário
def muda_nick_usuario(conn, id, novo_nick):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuario SET nick=%s where id_usuario=%s', (novo_nick, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError('Não posso alterar nick do id {} para {} na tabela usuario'.format(id, novo_nick))

#Verifica se o usuário esta desativado pelo ID
def esta_desativado_usuario(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('SELECT ativo FROM usuario WHERE id_usuario=%s', (id))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

#Lista os IDs de todos os usuarios
def lista_usuario(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuario')
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

#Adiciona um Usuario e um Passaro a tabela Preferencia
def adiciona_preferencia_a_passaro(conn, id_usuario, id_passaro):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO preferencia VALUES(%s,%s)', (id_usuario,id_passaro))

#Remove uma Preferencia dado um ID Usuario e Passaro
def remove_preferencia_de_passaro(conn, id_usuario, id_passaro):
        with conn.cursor() as cursor:
            cursor.execute('DELETE FROM preferencia WHERE id_usuario=%s AND id_passaro=%s',(id_usuario, id_passaro))

# Lista todos os passaros preferidos de um Usuario
def lista_passaro_de_preferencia(conn, id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro FROM preferencia WHERE id_usuario=%s', (id_usuario))
        res = cursor.fetchall()
        passaros = tuple(x[0] for x in res)
        return passaros

#Lista todos os usuarios que preferem um Passaro
def lista_preferencia_de_passaro(conn, id_passaro):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM preferencia WHERE id_passaro=%s', (id_passaro))
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

##############################################

#                       USUARIO

# ID do post mecionado e ID de quem esta marcando
#def menciona_usuario_em_post(conn, id_post, id_usuario):

#def visualiza_post(conn, id_post, id_usuario, aparelho, ip, browser, data):

#def lista_visualizadores_post(conn, id_post):

#def lista_posts_visualizados_usuario(conn, id_usuario):

#def lista_usuarios_mencionados_de_usuario(conn, id_usuario):

################################################

#Adiciona um post
def adiciona_post(conn, id_usuario, titulo, texto = None, url = None):
    query = """
    INSERT INTO post (id_usuario, titulo, texto, url) 
    VALUES (%s, %s, %s, %s);
    """

    with conn.cursor() as cursor:
        try:
            cursor.execute(query, (id_usuario, titulo, texto, url))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir o post {titulo} na tabela post')

#Acha um post
def acha_post(conn, titulo):
    query = """
    SELECT id_post FROM post WHERE titulo=%s
    """

    with conn.cursor() as cursor:
        cursor.execute(query, (titulo))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

#Desativa um post
def desativa_post(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('UPDATE post SET ativo=0 WHERE id_post=%s', (id))

#Lista os IDs de todos os posts
def lista_post(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM post')
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

#################################################

#                       POST

#def adiciona_marca_passaro(conn, id_passaro, id_post):

#def lista_usuarios_mencionados_no_post(conn, id_post):


#################################################


def parser_usuario(texto):
    t = []
    txt = re.findall(r"@\w+", texto)
    for i in range(len(txt)):
        t.append(txt[i][1:])
    return t

def parser_passaro(texto):
    t = []
    txt = re.findall(r"#\w+", texto)
    for i in range(len(txt)):
        t.append(txt[i][1:])
    return t