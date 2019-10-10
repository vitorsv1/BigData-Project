import io, logging, os, os.path, subprocess, re, unittest, pymysql

connection = pymysql.connect(
    host='localhost',
    user='megadados',
    password='megadados2019',
    database='red_soc_passaros')

def criar_usuario(connection, nome, sobrenome, email, cidade):
    query = """
    INSERT INTO usuarios (nick, nome, sobrenome, email, cidade) 
    VALUES (%s, %s, %s, %s, %s);
    """

    with connection.cursor() as cursor:
        try:
            cursor.execute(query, (nome,sobrenome,email,cidade))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela usuarios')

def acha_usuario(connection, )














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