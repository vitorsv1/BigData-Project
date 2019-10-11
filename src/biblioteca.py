import io, json, logging, os, os.path, subprocess, re, unittest, pymysql

connection = pymysql.connect(
    host='localhost',
    user='megadados',
    password='megadados2019',
    database='red_soc_passaros')

def criar_usuario(conn, nick, nome, sobrenome, email, cidade):
    query = """
    INSERT INTO usuario (nick, nome, sobrenome, email, cidade) 
    VALUES (%s, %s, %s, %s, %s);
    """
    with conn.cursor() as cursor:
        try:
            cursor.execute(query, (nick, nome,sobrenome,email,cidade))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela usuario')

def acha_usuario(conn, nick):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuario WHERE nick = %s', (nick))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def remove_usuario(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM usuario WHERE id=%s', (id))
    
def muda_nick_usuario(conn, id, novo_nick):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuario SET nick=%s where id_usuario=%s', (novo_nick, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar nick do id {id} para {novo_nick} na tabela usuario')

def lista_usuario(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuario')
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

def criar_post(conn, id_usuario, titulo, texto = None, url = None):
    query = """
    INSERT INTO post (id_usuario, titulo, texto, url) 
    VALUES (%s, %s, %s, %s);
    """

    with conn.cursor() as cursor:
        try:
            cursor.execute(query, (id_usuario, titulo, texto, url))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir o post {titulo} na tabela post')

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

def remove_post(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('UPDATE post SET ativo=0 WHERE id_post=%s', (id))

def lista_post(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM post')
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

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