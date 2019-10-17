import io, json, logging, os, os.path, subprocess, re, unittest, pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='red_soc_passaros')

########################################################
#                        ADICIONA                   
########################################################
# Adiciona um usuario na tabela usuario
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

# Adiciona um passaro na tabela passaro
def adiciona_passaro(conn,especie):
    query = """
    INSERT INTO passaro (especie) 
    VALUES (%s);
    """
    with conn.cursor() as cursor:
        try:
            cursor.execute(query, (especie))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {especie} na tabela usuario')

# Adiciona um post
def adiciona_post(conn, id_usuario,ativo,titulo, texto = None, url = None):
    query = """
    INSERT INTO post (id_usuario,ativo,titulo, texto, url) 
    VALUES (%s, %s, %s, %s,%s);
    """

    with conn.cursor() as cursor:
        try:
            cursor.execute(query, (id_usuario,ativo,titulo, texto, url))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir o post {titulo} na tabela post')
    
    usuarios_mencionados=parser_usuario(texto)
    passaros_mencionados=parser_passaro(texto)
    for i in usuarios_mencionados:
        menciona_usuario_em_post(conn,acha_post(conn,titulo),acha_usuario(conn,i))
    for j in passaros_mencionados:
        marca_passaro_em_post(conn,acha_passaro(conn,j),acha_post(conn,titulo))

# Adiciona um Usuario e um Passaro a tabela Preferencia
def adiciona_preferencia_a_passaro(conn, id_usuario, id_passaro):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO preferencia VALUES(%s,%s)', (id_usuario,id_passaro))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Erro na inserção')

# Adiciona visualizacao do usuario
def adiciona_visualizacao_post(conn, id_post, id_usuario, aparelho, ip, browser, data_visualizacao):
    query = """
    INSERT INTO visualizacao (id_post, id_usuario, aparelho, ip, browser, data_visualizacao)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    with conn.cursor() as cursor:
        try:
            cursor.execute(query, (id_post, id_usuario, aparelho, ip, browser, data_visualizacao))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Erro na inserção')

#adiciona like de usuario a post
def adiciona_post_like(conn, id_post, id_usuario,post_like):

    if(post_like != "Like" and post_like!="Deslike"):
        raise ValueError(f'COMANDO NAO IDENTIFICADO')
    query = """
    INSERT INTO usuario_post_like (id_post, id_usuario,post_like)
    VALUES (%s, %s, %s)
    """

    with conn.cursor() as cursor:
        try:
            cursor.execute(query, (id_post, id_usuario,post_like))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Erro na inserção')



########################################################
#                   DESATIVA e REMOVE                   
########################################################

#Desativa um usuário
def desativa_usuario(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('UPDATE usuario SET ativo=0 WHERE id_usuario=%s', (id))
  
#Desativa um post
def desativa_post(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('UPDATE post SET ativo=0 WHERE id_post=%s', (id))
        
#Remove uma Preferencia dado um ID Usuario e Passaro
def remove_preferencia_de_passaro(conn, id_usuario, id_passaro):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM preferencia WHERE id_usuario=%s AND id_passaro=%s',(id_usuario, id_passaro))

#Remove Like ou Dislike no Post
def remove_post_like(conn,id_post,id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM usuario_post_like WHERE id_usuario=%s AND id_post=%s',(id_usuario, id_post))

########################################################
#                       STATUS                   
########################################################

#Verifica se o usuário esta desativado pelo ID
def esta_desativado_usuario(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('SELECT ativo FROM usuario WHERE id_usuario=%s',(id))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

#Verifica se o usuário esta desativado pelo ID
def esta_desativado_post(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('SELECT ativo FROM post WHERE id_post=%s',(id))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

#Retorna se o post esta Like ou Deslike pelo Usuario
def esta_like_dislike(conn,id_post,id_usuario):
    with conn.cursor() as cursor:
        cursor.execute('SELECT post_like FROM usuario_post_like WHERE id_post=%s and id_usuario=%s',(id_post,id_usuario))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

########################################################
#                       ACHA                   
########################################################

# Acha um usuario pelo Nick
def acha_usuario(conn, nick):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuario WHERE nick = %s', (nick))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

# Acha um passaro pela Especia
def acha_passaro(conn, especie):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro FROM passaro WHERE especie = %s', (especie))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

# Acha um post pelo Titulo
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



########################################################
#                       MUDA                   
########################################################

#Muda nick de um usuário
def muda_nick_usuario(conn, id, novo_nick):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuario SET nick=%s where id_usuario=%s', (novo_nick, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError('Não posso alterar nick do id {} para {} na tabela usuario'.format(id, novo_nick))

#Muda condicao do Like
def muda_like_post(conn, id_post,id_usuario,like):
    if(like != "Like" and like!="Deslike"):
        raise ValueError(f'COMANDO NAO IDENTIFICADO')

    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuario_post_like SET post_like=%s where id_usuario=%s AND id_post=%s',(like,id_usuario,id_post))
        except pymysql.err.IntegrityError as e:
            raise ValueError('Não posso alterar')



########################################################
#                 MENCIONA e  MARCA                   
########################################################

# Menciona um usuario em um post pelos IDs
def menciona_usuario_em_post(conn, id_post, id_usuario):
    query = """
    INSERT INTO mencao (id_post,id_usuario) 
    VALUES (%s, %s);
    """
    
    with conn.cursor() as cursor:
        try:
            cursor.execute(query, (id_post,id_usuario))
           # 
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Ja tentou adicionar')


# Marca um passaro em um post pelos IDs
def marca_passaro_em_post(conn, id_passaro, id_post):
    query = """
    INSERT INTO marca_passaro (id_passaro,id_post) 
    VALUES (%s, %s);
    """
    with conn.cursor() as cursor:
        try:
            cursor.execute(query, (id_passaro,id_post))
           # 
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Ja tentou adicionar')



########################################################
#                       LISTA                   
########################################################

# Lista os IDs de todos os usuarios
def lista_usuario(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_usuario FROM usuario')
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

#Lista IDs e Especies de todos os Passaros
def lista_passaro(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_passaro,especie FROM passaro')
        res = cursor.fetchall()
        passaros = tuple(x[0:2] for x in res)
        return passaros

#Lista os IDs de todos os posts
def lista_post(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_post FROM post')
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

# Lista uma Tupla dos IDs na tabela Preferencia       
def lista_preferencia(conn):
    query = """
    SELECT id_usuario, id_passaro FROM preferencia
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        res = cursor.fetchall()
        preferencias = tuple(x[0:2] for x in res)
        return preferencias

# Lista os usuarios que visualizaram um post pelo ID do post
def lista_visualizadores_post(conn, id_post):
    query = """
    SELECT id_usuario FROM visualizacao WHERE id_post = %s
    """

    with conn.cursor() as cursor:
        cursor.execute(query, (id_post))
        res = cursor.fetchall()
        visualizadores = tuple(x[0] for x in res)
        return visualizadores

# Lista os posts que um usuario viu
def lista_posts_visualizados_usuario(conn, id_usuario):
    query = """
    SELECT id_post FROM visualizacao WHERE id_usuario = %s
    """

    with conn.cursor() as cursor:
        cursor.execute(query, (id_usuario))
        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

#Lista as menções
def lista_mencoes(conn):
    query="""
    SELECT id_post, id_usuario FROM mencao
    """

    with conn.cursor() as cursor:
        cursor.execute(query)
        res = cursor.fetchall()
        mencoes = tuple(x[0:2] for x in res)
        return mencoes

#Lista os passaros marcados
def lista_marca_passaro(conn):
    query="""
    SELECT id_passaro, id_post FROM marca_passaro
    """

    with conn.cursor() as cursor:
        cursor.execute(query)
        res = cursor.fetchall()
        marcacoes = tuple(x[0:2] for x in res)
        return marcacoes

#lista ids de likes e dislikes do post
def lista_post_like(conn):
    query="""
    SELECT id_post, id_usuario FROM usuario_post_like
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        res = cursor.fetchall()
        marcacoes = tuple(x[0:2] for x in res)
        return marcacoes

########################################################
#                       PARSER                   
########################################################

# Parser para procurar usuarios marcados no texto 
# retorna lista dos usuarios marcados em ordem
def parser_usuario(texto):
    t = []
    txt = re.findall(r"@\w+", texto)
    for i in range(len(txt)):
        t.append(txt[i][1:])
    return t

# Parser para procurar passaros marcados 
# retorna lista dos passaros marcados em ordem
def parser_passaro(texto):
    t = []
    txt = re.findall(r"#\w+", texto)
    for i in range(len(txt)):
        t.append(txt[i][1:])
    return t

    
