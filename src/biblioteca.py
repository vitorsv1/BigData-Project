import io, json, logging, os, os.path, subprocess, re, unittest, pymysql

connection = pymysql.connect(
    host='localhost',
    user='megadados',
    password='megadados2019',
    database='red_soc_passaros')

def criar_usuario(connection, nick, nome, sobrenome, email, cidade):
    query = """
    INSERT INTO usuarios (nick, nome, sobrenome, email, cidade) 
    VALUES (%s, %s, %s, %s, %s);
    """

    with connection.cursor() as cursor:
        try:
            cursor.execute(query, (nick, nome,sobrenome,email,cidade))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela usuarios')

def acha_usuario(conn, nick):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id FROM usuarios WHERE nick = %s', (nick))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def remove_usuario(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM usuarios WHERE id=%s', (id))
    
def muda_nick_usuario(conn, id, novo_nick):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuarios SET nick=%s where id=%s', (novo_nick, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar nick do id {id} para {novo_nick} na tabela usuarios')




def criar_post(connection, id_usuario, titulo, texto = None, url = None):
    query = """
    INSERT INTO post (id_usuario, titulo, texto, url) 
    VALUES (%s, %s, %s, %s);
    """

    with connection.cursor() as cursor:
        try:
            cursor.execute(query, (id_usuario, titulo, texto, url))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir o post {titulo} na tabela post')


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