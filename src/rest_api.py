from functools import partial
import io, json, os, os.path, subprocess, pymysql
from fastapi import FastAPI
from pydantic import BaseModel
from biblioteca import *

app = FastAPI()

def run_db_query(conn, query, args=None):
    with conn.cursor() as cursor:
        cursor.execute(query, args)
        for result in cursor:
            print(result)

global config
conn = connection
db = partial(run_db_query, conn)

class Usuario(BaseModel):
    nick: str
    nome: str
    sobrenome: str
    email: str
    cidade: str

class Post(BaseModel):
    nick: str
    ativo: str
    titulo: str
    texto: str
    url: str

class Passaro(BaseModel):
    especie: str

class Lugar(BaseModel):
    lugar: str

class Vizualizacao(BaseModel):
    aparelho:str
    ip:str
    browser:str
    data:str


@app.get("/usuario")
def get_lista_usuario():
    try:
        return lista_usuario(conn)
    except:
        return f'Não posso listar os usuarios na tabela Usuario'


@app.post("/usuario")
def post_adiciona_usuario(usuario: Usuario):
    try:
        adiciona_usuario(conn, usuario.nick, usuario.nome,
                   usuario.sobrenome, usuario.email, usuario.cidade)
        conn.commit()
        return "Usuario foi adicionado"
    except:
        return f'Não posso inserir {usuario.nick, usuario.nome,usuario.sobrenome, usuario.email, usuario.cidade} na tabela person'


@app.delete("/usuario")
def delete_desativa_usuario(nick: str):
    try:
        idUsuario = acha_usuario(conn, nick)
        if idUsuario:
            desativa_usuario(conn, idUsuario)
            conn.commit()
            return f"Usuario {nick} foi desativado"
        else:
            return f"Nao existe um usuario {nick}"

    except:
        return f'Não posso desativar {nick} na tabela Usuario'


@app.put("/usuario")
def update_muda_nick_usuario(nick: str, new_nick: str):
    try:
        idUsuario = acha_usuario(conn, nick)
        if idUsuario:
            muda_nick_usuario(conn, idUsuario, new_nick)
            conn.commit()
            return f"Username alterado de: {nick} para: {new_nick}"
        else:
            return f"Nao existe uma pessoa com o username {nick}"
    except:
        return f'Não posso alterar o username para: {new_nick} tente outro username'


@app.get("/post")
def get_lista_post():
    try:
        return lista_post(conn)
    except:
        return f'Não foi possível listar os posts'


@app.post("/post")
def post_adiciona_post(post: Post):
    try:
        idUsuario = acha_usuario(conn, post.nick)
        if idUsuario:
            adiciona_post(conn, idUsuario, post.ativo, post.titulo, post.texto, post.url)
            conn.commit()
            return f"Post {post.titulo} foi adicionado"
        else:
            return f"Nao existe um usuario para adicionar o post"

    except:
        return f'Não posso inserir o post'


@app.delete("/post")
def delete_desativa_post(titulo: str):
    try:
        idPost = acha_post(conn, titulo)
        if idPost:
            desativa_post(conn, idPost)
            conn.commit()
            return f"Post {titulo} foi removido"
        else:
            return f"Nao existe um post {titulo}"
    except:
        return f'Não posso remover o post {titulo}'

@app.delete("/preferencia/passaro")
def delete_remove_preferencia_de_passaro(nick: str, especie: str):
    try:
        idUsuario = acha_usuario(conn, nick)
        idPassaro = acha_passaro(conn, especie)
        if idUsuario:
            if idPassaro:    
                remove_preferencia_de_passaro(conn, idUsuario, idPassaro)
                conn.commit()
                return f"Preferencia removida do passaro {especie}"
            else:
                return f"Não existe passaro"
        else:
            return f"Não existe usuario"
    except:
        return f'Não foi possivel remover preferencia de passaro'

@app.delete("/post/like")
def delete_remove_post_like(titulo: str, nick: str):
    try:
        idPost = acha_post(conn, titulo)
        idUsuario = acha_usuario(conn, nick)
        if idUsuario:
            if idPost:    
                remove_post_like(conn, idPost, idUsuario)
                conn.commit()
                return f"Removido o like ou dislike do post {titulo}"
            else:
                return f"Não existe post"
        else:
            return f"Não existe usuario"
    except :
        return f'Não foi possivel remover like do post'


@app.get("/passaro")
def get_lista_passaro():
    try:
        return lista_passaro(conn)
    except:
        return f'Não posso listar os usuarios na tabela Usuario'


@app.post("/passaro")
def post_adiciona_passaro(passaro: Passaro):
    try:
        adiciona_passaro(conn,passaro.especie)
        conn.commit()
        return "Passaro Adiconado"
    except:
        return f'Não posso inserir {passaro.especie} na tabela passaro'

@app.get("/usuario/status")
def get_esta_desativado_usuario(nick: str):
    try:
        idUsuario = acha_usuario(conn, nick)
        if idUsuario:
            return esta_desativado_usuario(conn, idUsuario)
        else:
            return f'Usuario não encontrado {nick}'
    except:
        return f'Nao posso desativar um usuario'

@app.get("/post/status")
def get_esta_desativado_post(titulo: str):
    try:
        idPost = acha_post(conn, titulo)
        if idPost:
            return esta_desativado_usuario(conn, idPost)
        else:
            return f'Post não encontrado {titulo}'
    except:
        return f'Nao posso desativar um post'

@app.get("/post/status/like")
def get_esta_like_dislike(titulo: str, nick: str):
    try:
        idPost = acha_post(conn, titulo)
        idUsuario = acha_usuario(conn, nick)
        if idPost:
            if idUsuario:
                return esta_like_dislike(conn, idPost, idUsuario)
            else:
                return f'Não existe usuario {nick}'
        else:
            return f'Post não encontrado {titulo}'
    except:
        f'Não foi possivel pegar o status like deslike'

@app.put("/post/like")
def put_muda_like_post(titulo: str, nick: str, like: str):
    try:
        idPost = acha_post(conn, titulo)
        idUsuario = acha_usuario(conn, nick)
        if idPost:
            if idUsuario:
                muda_like_post(conn, idPost, idUsuario, like)
                return f'Mudou para {like}'
            else:
                return f'Não existe usuario {nick}'
        else:
            return f'Post não encontrado {titulo}'
    except:
        return f'Não foi possivel mudar like para deslike'

@app.post("/lugar")
def post_adiciona_lugar(lugar: Lugar):
    try:
        adiciona_lugar(conn,lugar.lugar)
        conn.commit()
        return "lugar adicionado"
    except:
        print(lugar.lugar)
        return f'Não posso inserir {lugar.lugar} na tabela lugar'

@app.post("/preferencia")
def post_adiciona_preferencia_a_passaro(nick:str,especie:str):
    try:
        idUsuario=acha_usuario(conn,nick)
        idPassaro=acha_passaro(conn,especie)
        adiciona_preferencia_a_passaro(conn,idUsuario,idPassaro)
        conn.commit()
        return ""
    except:
        return f'operacao invalida'

@app.post("/vizualizacao")
def post_adiciona_vizualizacao_post(nick:str,titulo:str,vizualizacao:Vizualizacao):
    try:
        idUsuario=acha_usuario(conn,nick)
        idPost=acha_post(conn,titulo)
        adiciona_preferencia_a_passaro(conn,idUsuario,idPassaro)
        adiciona_visualizacao_post(conn,idPost,idUsuario,vizualizacao.aparelho,vizualizacao.ip,vizualizacao.browser,vizualizacao.data_visualizacao)
        conn.commit()
        return ""
    except:
        return f'operacao invalida'

@app.post("/post/like")
def post_adiciona_post_like(nick:str,titulo:str,like:str):
    try:
        idUsuario=acha_usuario(conn,nick)
        idPost=acha_post(conn,titulo)
        adiciona_post_like(conn,idPost,idUsuario,like)
        conn.commit()
        return ""
    except:
        return f'operacao invalida'


@app.post("/menciona")
def post_menciona_usuario_em_post(nick:str,titulo:str):
    try:
        idUsuario=acha_usuario(conn,nick)
        idPost=acha_post(conn,titulo)
        menciona_usuario_em_post(conn,idPost,idUsuario)
        conn.commit()
        return ""
    except:
        return f'operacao invalida'

@app.post("/lugar/marca")
def post_marca_lugar_em_post(lugar:str,titulo:str):
    try:
        idLugar=acha_lugar(conn,lugar)
        idPost=acha_post(conn,titulo)
        marca_lugar_em_post(conn,idLugar,idPost)
        conn.commit()
        return ""
    except:
        return f'operacao invalida'

@app.post("/passaro/marca")
def post_marca_passaro_em_post(titulo:str,especie:str):
    try:
        idPost=acha_post(conn,titulo)
        idPassaro=acha_passaro(conn,especie)
        marca_passaro_em_post(conn,idPassaro,idPost)
        conn.commit()
        return ""
    except:
        return f'operacao invalida'

@app.get("/lugar")
def get_lista_lugar():
    try:
        return lista_lugar(conn)
    except:
        return f'Não posso listar lugares'

@app.get("/usuario/post")
def get_lista_post_usuario(nick: str):
    try:
        idUsuario=acha_usuario(conn,nick)
        if idUsuario:
            return lista_post_usuario(conn, idUsuario)
        else:
            f'Usuario não encontrado'
    except:
        return f'Não posso listar os posts dos usuarios em ordem cronologica reversa'

@app.get("/preferencia")
def get_lista_preferencia():
    try:
        return lista_preferencia(conn)
    except:
        return f'Não foi possivel retornar preferencia'


@app.get("/usuario/post")
def get_lista_posts_visualizados_usuario(nick: str):
    try:
        idUsuario=acha_usuario(conn,nick)
        if idUsuario:
            return lista_posts_visualizados_usuario(conn, idUsuario)
        else:
            f'Usuario não encontrado'
    except:
        return f'Não posso listar os posts dos usuarios em ordem cronologica reversa'

@app.get("/usuario/popular")
def get_lista_usuario_popular_cidade():
    try:
        return lista_usuario_popular_cidade(conn)
    except:
        return f'Não foi possivel listar o usuario popular de cada cidade'

@app.get("/post/usuario")
def get_lista_visualizadores_post(titulo: str):
    try:
        idPost=acha_post(conn,titulo)
        if idPost:
            return lista_posts_visualizados_usuario(conn, idPost)
        else:
            f'Post não encontrado'
    except:
        return f'Não posso listar os posts dos usuarios em ordem cronologica reversa'

@app.get("/mencoes")
def get_lista_mencoes():
    try:
        return lista_mencoes(conn)
    except:
        return f'Não foi possivel retornar as mençoes'


@app.get("/passaro/marca")
def get_lista_marca_passaro():
    try:
        return lista_marca_passaro(conn)
    except:
        return f'operacao invalida'

@app.get("/lugar/marca")
def get_lista_marca_lugar():
    try:
        return lista_marca_lugar(conn)
    except:
        return f'operacao invalida'


@app.get("/post/like")
def get_lista_post_like():
    try:
        return lista_post_like(conn)
    except:
        return f'operacao invalida'


@app.get("/usuario/referenciado")
def get_lista_usuarios_refenciados(nick:str):
    try:
        idUsuario=acha_usuario(conn,nick)
        return lista_usuarios_refenciados(conn,idUsuario)
    except:
        return f'operacao invalida'


@app.get("/vizualizacao/quantidade")
def get_lista_vizualizacao_quantidade():
    try:
        return lista_visualizacao_quantidade(conn)
    except:
        return f'operacao invalida'

@app.get("/post/passaro-url")
def get_lista_url_passaro():
    try:
        return lista_url_passaro(conn)
    except:
        return f'Operação invalida'

@app.get("/vizualizacao/tipo-browser")
def get_lista_visualizacao_tipo_browser():
    try:
        return lista_visualizacao_tipo_browser(conn)
    except:
        return f'operacao invliada'