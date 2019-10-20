from biblioteca import *

class TestProjeto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global config
        cls.connection = pymysql.connect(
            host=config['HOST'],
            user=config['USER'],
            password=config['PASS'],
            database='red_soc_passaros'
        )
    
    @classmethod
    def tearDownClass(cls):
        cls.connection.close()
    
    def setUp(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('START TRANSACTION')

    def tearDown(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('ROLLBACK')

########################################################
#                        ADICIONA                   
########################################################

    def test_adiciona_usuario(self):
        conn = self.__class__.connection
        
        nick = "Jukes"
        nome = "Junior"
        sobrenome = "Cria"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"

        adiciona_usuario(conn, nick, nome, sobrenome, email, cidade)

        try:
            adiciona_usuario(conn, nick, nome, sobrenome, email, cidade)
            self.fail('Não deveria ter adicionado o mesmo usuario duas vezes')
        except ValueError as e:
            pass
    
    def test_adiciona_passaro(self):
        conn = self.__class__.connection
        
        especie = "Canario"

        adiciona_passaro(conn, especie)

        try:
            adiciona_passaro(conn, especie)
            self.fail('Não deveria ter adicionado o mesmo usuario duas vezes')
        except ValueError as e:
            pass
        
        id = acha_passaro(conn, especie)
        self.assertIsNotNone(id)

        id = acha_passaro(conn, 'pokadskopdsa')
        self.assertIsNone(id)   

    def test_adiciona_post(self):
        conn = self.__class__.connection

        nick = "Jukes"
        nome = "Junior"
        sobrenome = "Cria"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn, nick, nome, sobrenome, email, cidade)
        id_usuario=acha_usuario(conn,"Jukes")
        titulo="Mas que bela Araponga"
        texto="TEIN TEIN TEIN TEIN TEIN"
        url="http://s2.glbimg.com/R-XKif4dYrgSxkvE6ThOCgcbCcc=/s.glbimg.com/jo/g1/f/original/2015/01/06/fotoara.jpg"

        adiciona_post(conn,id_usuario,1,titulo,texto,url)

        try:
            adiciona_post(conn,id_usuario,1,titulo,texto,url)
            self.fail('Não deveria ter adicionado o mesmo post duas vezes')
        except ValueError as e:
            pass
        
        id = acha_post(conn, titulo)
        self.assertIsNotNone(id)

        id = acha_post(conn, 'pokadskopdsa')
        self.assertIsNone(id)

    def test_adiciona_preferencia_a_passaro(self):
        conn = self.__class__.connection

        nick = "Ju"
        nome = "Junior"
        sobrenome = "Desativa"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn, nick, nome, sobrenome, email, cidade)
        idJu = acha_usuario(conn, "Ju")
        
        adiciona_passaro(conn, "Bicudo")
        idBicudo = acha_passaro(conn, "Bicudo")

        adiciona_preferencia_a_passaro(conn, idJu, idBicudo)

        try:
            adiciona_preferencia_a_passaro(conn, idJu, idBicudo)
            self.fail("Não deveria ter adicionado novamente")
        except ValueError as e:
            pass
    
        res = lista_preferencia(conn)
        t1 = (idJu, idBicudo)
        self.assertEqual(res[0], t1)

    def test_adiciona_visualizacao_post(self):
        conn = self.__class__.connection

        nick = "Juks"
        nome = "Junior"
        sobrenome = "Visualiza"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn,nick, nome, sobrenome, email, cidade)
        id = acha_usuario(conn,nick)

        titulo= "Teste post"
        texto = "aoskdoapsdk"
        url = "sokdapodkpao.com"
        adiciona_post(conn, id,1,titulo,texto, url)
        id_post = acha_post(conn, titulo)

        adiciona_visualizacao_post(conn, id_post, id, "Android", "192.129.3.1","Chrome", "2019-02-01")

        try:
            adiciona_visualizacao_post(conn, id_post, id, "Android", "192.129.3.1","Chrome", "2019-02-01")
            self.fail("Não deveria adicionar uma visualizacao nova")
        except ValueError as e:
            pass

    def test_adiociona_post_like(self):
        conn = self.__class__.connection

        nick = "Jukes"
        nome = "Junior"
        sobrenome = "Visualiza"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"

        adiciona_usuario(conn,nick, nome, sobrenome, email, cidade)
        adiciona_usuario(conn,"Teste1", nome, sobrenome, email, cidade)
        adiciona_usuario(conn,"Postador", nome, sobrenome, email, cidade)

        idUser1 = acha_usuario(conn,nick)
        idUser2 = acha_usuario(conn,"Teste1")
        idPostador = acha_usuario(conn,"Postador")

        titulo= "Teste post"
        texto = "aoskdoapsdk"
        url = "sokdapodkpao.com"
        adiciona_post(conn, idPostador,1,titulo,texto, url)
        adiciona_post(conn, idPostador,1,"tituloT",texto, url)

        id_post1 = acha_post(conn, titulo)
        id_post2 = acha_post(conn,"tituloT")

        adiciona_post_like(conn, id_post1, idUser1, "Like")
        adiciona_post_like(conn, id_post1, idUser2, "Like")
        adiciona_post_like(conn, id_post2, idUser1, "Like")
        adiciona_post_like(conn, id_post2, idUser2, "Deslike")
        res = lista_post_like(conn)
        likes = ((id_post1,idUser1),(id_post1,idUser2),(id_post2,idUser1),(id_post2,idUser2))
        self.assertCountEqual(res,likes)
        
########################################################
#                   DESATIVA e REMOVE                   
########################################################

    def test_desativa_usuario(self):
        conn = self.__class__.connection

        nick = "Ju"
        nome = "Junior"
        sobrenome = "Desativa"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn, nick, nome, sobrenome, email, cidade)
        id = acha_usuario(conn, nick)

        res = lista_usuario(conn)
        self.assertCountEqual(res, (id,))

        desativa_usuario(conn, id)

        res = esta_desativado_usuario(conn, id)
        self.assertFalse(res)

    def test_desativa_post(self):
        conn = self.__class__.connection

        nick = "Juks"
        nome = "Junior"
        sobrenome = "Visualiza"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn,nick, nome, sobrenome, email, cidade)
        id = acha_usuario(conn,nick)

        titulo= "Teste post"
        texto = "aoskdoapsdk"
        url = "sokdapodkpao.com"
        adiciona_post(conn, id,1,titulo,texto, url)
        id_post = acha_post(conn, titulo)
        
        desativa_post(conn, id_post)
        res = esta_desativado_post(conn, id_post)
      
        
        self.assertEqual(0,res)

    def test_remove_preferencia_de_passaro(self):
        conn = self.__class__.connection

        nick = "Ju"
        nome = "Junior"
        sobrenome = "Desativa"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn, nick, nome, sobrenome, email, cidade)
        idJu = acha_usuario(conn, "Ju")
    
        adiciona_passaro(conn, "Bicudo")
        idBicudo = acha_passaro(conn, "Bicudo")

        adiciona_preferencia_a_passaro(conn, idJu, idBicudo)

        remove_preferencia_de_passaro(conn, idJu, idBicudo)

        res = lista_preferencia(conn)
        self.assertFalse(res)

    def test_remove_post_like(self):
        conn = self.__class__.connection
        nick = "Jukes"
        nome = "Junior"
        sobrenome = "Desativa"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn, nick, nome, sobrenome, email, cidade)
        idJukes = acha_usuario(conn, "Jukes")
        adiciona_post(conn,idJukes,1,"Titulo","texto","url")
        idPost=acha_post(conn,"Titulo")
        remove_post_like(conn,idPost,idJukes)
        res = lista_post_like(conn)
        self.assertFalse(res)


########################################################
#                       STATUS                   
########################################################

    def test_esta_desativado_usuario(self):
        conn = self.__class__.connection

        adiciona_usuario(conn,"Jukes","teste","teste","teste@teste.com","testLandia")
        adiciona_usuario(conn,"Jukes2","teste","teste","teste@teste.com","testLandia")

        idUser1=acha_usuario(conn,"Jukes")
        idUser2=acha_usuario(conn,"Jukes2")
        
        status1=esta_desativado_usuario(conn,idUser1)
        status2=esta_desativado_usuario(conn,idUser2)

        self.assertEqual(1,status1)
        self.assertEqual(1,status2)

        desativa_usuario(conn,idUser1)
        desativa_usuario(conn,idUser2)

        status1=esta_desativado_usuario(conn,idUser1)
        status2=esta_desativado_usuario(conn,idUser2)

        self.assertEqual(0,status1)
        self.assertEqual(0,status2)

    def test_esta_desativado_post(self):
        conn = self.__class__.connection
        nick = "Juks"
        nome = "Junior"
        sobrenome = "Visualiza"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn,nick, nome, sobrenome, email, cidade)
        id = acha_usuario(conn,nick)
        titulo= "Teste post"
        texto = "aoskdoapsdk"
        url = "sokdapodkpao.com"
        adiciona_post(conn, id,1,titulo,texto, url)
        id_post = acha_post(conn, titulo)
        status1 = esta_desativado_post(conn, id_post)

        self.assertEqual(1,status1)

        desativa_post(conn,id_post)

        status1 = esta_desativado_post(conn, id_post)

        self.assertEqual(0,status1)

    def test_esta_like_dislike(self):
        conn = self.__class__.connection
        nick = "Jukes"
        nome = "Junior"
        sobrenome = "Visualiza"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn,nick, nome, sobrenome, email, cidade)
        adiciona_usuario(conn,"Jovi", nome, sobrenome, email, cidade)
        idUsuario = acha_usuario(conn,nick)
        idUsuario2 = acha_usuario(conn,"Jovi")
        titulo= "Teste post"
        texto = "aoskdoapsdk"
        url = "sokdapodkpao.com"
        adiciona_post(conn,idUsuario,1,titulo,texto, url)
        idPost = acha_post(conn, titulo)
        adiciona_post_like(conn,idPost,idUsuario2,"Like")
        status=esta_like_dislike(conn,idPost,idUsuario2)


      
########################################################
#                       ACHA                   
########################################################


    def test_acha_usuario(self):
        conn = self.__class__.connection
        id=10
        nick = "Jukes"
        nome = "Junior"
        sobrenome = "Cria"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn,nick, nome, sobrenome, email, cidade)

        id=acha_usuario(conn,"Jukes")
        self.assertIsNotNone(id)
        res= lista_usuario(conn)
        self.assertEqual(res[0],id)

    def test_acha_post(self):
        conn = self.__class__.connection
        nick = "Jukes"
        nome = "Junior"
        sobrenome = "Cria"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn,nick, nome, sobrenome, email, cidade)
        id=acha_usuario(conn,"Jukes")

        titulo= "Teste post"
        texto = "aoskdoapsdk"
        url = "sokdapodkpao.com"
        adiciona_post(conn, id,1,titulo,texto, url)
        id_post = acha_post(conn, titulo)
        self.assertIsNotNone(id_post)
        res=lista_post(conn)
        self.assertEqual(res[0],id_post)

    def test_acha_passaro(self):
        conn = self.__class__.connection
        adiciona_passaro(conn,"Araponga")
        idPassaro=acha_passaro(conn,"Araponga")
        adiciona_passaro(conn,"Sabia")
        idPassaro2=acha_passaro(conn,"Sabia")
        self.assertIsNotNone(idPassaro)
        res=lista_passaro(conn)
        res2=((idPassaro,"Araponga"),(idPassaro2,"Sabia"))
        self.assertCountEqual(res,res2)

########################################################
#                       MUDA                   
########################################################


    def test_muda_nick_usuario(self):
        conn = self.__class__.connection

        nick = "Jukes"
        nome = "Junior"
        sobrenome = "Cria"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"

        adiciona_usuario(conn, nick, nome, sobrenome, email, cidade)
        adiciona_usuario(conn, "Jukera", nome, sobrenome, email, cidade)
        id = acha_usuario(conn,"Jukera")

        try:
            muda_nick_usuario(conn, id, "Jukes")
            self.fail('Não deveria ter mudado o nome.')
        except ValueError as e:
            pass

        muda_nick_usuario(conn, id, 'MecLord')

        id_novo = acha_usuario(conn,'MecLord')
        self.assertEqual(id,id_novo)

    def test_muda_like_post(self):
        conn = self.__class__.connection

        nick = "Jukes"
        nome = "Junior"
        sobrenome = "Cria"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"

        adiciona_usuario(conn, nick, nome, sobrenome, email, cidade)
        adiciona_usuario(conn, "Jukera", nome, sobrenome, email, cidade)
        idUser1 = acha_usuario(conn,"Jukera")
        idUser2= acha_usuario(conn,"Jukes")

        adiciona_post(conn,idUser1,1,"Titulo","texto","URL")
        idPost=acha_post(conn,"Titulo")
        adiciona_post_like(conn,idPost,idUser2,"Like")
        
        muda_like_post(conn,idPost,idUser2,"Deslike")

        res=esta_like_dislike(conn,idPost,idUser2)

        self.assertNotEqual("Like",res)


########################################################
#                 MENCIONA e  MARCA                   
########################################################


    def test_menciona_usuario_em_post(self):
        conn = self.__class__.connection
        
        nick = "Ju"
        nome = "Junior"
        sobrenome = "Desativa"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        
        adiciona_usuario(conn, nick, nome, sobrenome, email, cidade)
        adiciona_usuario(conn, "Jovi", nome, sobrenome, email, cidade)
        adiciona_usuario(conn, "Rakin", nome, sobrenome, email, cidade)
        
        idJu = acha_usuario(conn, "Ju")
        idJovi = acha_usuario(conn,"Jovi")
        idRakin = acha_usuario(conn,"Rakin")

        #adiciona_post(conn, idJu, "Breskein", "Muito legal @jovi")
        adiciona_post(conn, idJu, 1,"Breskein", "Muito legal @jovi @rakin","askdpaosd.com")
        idPost = acha_post(conn, "Breskein")

        self.assertIsNotNone(idJovi)
        self.assertIsNotNone(idJu)
        self.assertIsNotNone(idPost)

        mencoes = lista_mencoes(conn)
        rak = (idPost, idRakin)
        jovi = (idPost, idJovi)

        self.assertEqual(mencoes[0], jovi)
        self.assertEqual(mencoes[1], rak)

    def test_marca_passaro_em_post(self):
        conn = self.__class__.connection
        
        nick = "Ju"
        nome = "Junior"
        sobrenome = "Desativa"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn, nick, nome, sobrenome, email, cidade)
        idJu = acha_usuario(conn, "Ju")
        
        adiciona_passaro(conn, "Bicudo")
        adiciona_passaro(conn, "Canario")
        
        idBicudo = acha_passaro(conn, "Bicudo")
        idCanario = acha_passaro(conn, "Canario")
        
        adiciona_post(conn, idJu,1, "Breskein", "Muito legal esse #bicudo #canario","askdpaosd.com")
        idPost = acha_post(conn, "Breskein")
        
        marcacoes = lista_marca_passaro(conn)
        t1 = (idBicudo, idPost)
        t2 = (idCanario, idPost)

        self.assertEqual(marcacoes[0], t1)
        self.assertEqual(marcacoes[1], t2)



########################################################
#                       LISTA                   
########################################################


    def test_lista_usuarios(self):
        conn = self.__class__.connection
        res=lista_usuario(conn)
        self.assertFalse(res)
        
        usuariosids=[]
        for i in range(3):
            nick="JuninhoXD{}".format(i)
            adiciona_usuario(conn,nick,"Junior","Teste","teste@teste.com","testelandia")
            usuariosids.append(acha_usuario(conn,nick))
        
        res=lista_usuario(conn)
        self.assertCountEqual(res,usuariosids)

        for j in usuariosids:
            desativa_usuario(conn,j)
        
        for k in usuariosids:
            res=esta_desativado_usuario(conn, k)
            self.assertFalse(res)

    def test_lista_passaro(self):
        conn = self.__class__.connection
        res=lista_passaro(conn)
        self.assertFalse(res)
        
        passarosids=[]
        for i in range(3):
            especie="Araponga{}".format(i)
            adiciona_passaro(conn,especie)
            passarosids.append(acha_passaro(conn,especie))
        
        res=lista_passaro(conn)
        res=list(zip(*res))[0]
        self.assertCountEqual(res,passarosids)
   
    def test_lista_post(self):
        conn = self.__class__.connection
        res=lista_post(conn)
        self.assertFalse(res)
        adiciona_usuario(conn,"Jukes","Junior","Teste","teste@teste.com","testelandia")
        idUsuario=acha_usuario(conn,"Jukes")
        postsids=[]
        for i in range(3):
            titulo="titulo{}".format(i)
            adiciona_post(conn,idUsuario,1,titulo,"ola","www")
            postsids.append(acha_post(conn,titulo))
        
        res=lista_post(conn)
        self.assertCountEqual(res,postsids)

    def test_lista_post_usuario(self):
        conn = self.__class__.connection
        adiciona_usuario(conn,"Jukes","Junior","Teste","teste@teste.com","testelandia")
        idUsuario=acha_usuario(conn,"Jukes")
   
        adiciona_post(conn,idUsuario,1,"titulo1","ola","www")
        adiciona_post(conn,idUsuario,1,"titulo2","ola","www")
        adiciona_post(conn,idUsuario,1,"titulo3","ola","www")
        adiciona_post(conn,idUsuario,1,"titulo4","ola","www")

        idsPosts=[]
        res=lista_post_usuario(conn,idUsuario)
        for i in range(4,0,-1):
            titulo="titulo{}".format(i)
            idPost=acha_post(conn,titulo)
            idsPosts.append(idPost)
        
        for i in range(len(idsPosts)):
            self.assertEqual(idsPosts[i],res[i])
        
    def test_lista_preferencia(self):
        conn = self.__class__.connection
        adiciona_usuario(conn,"Jukes","teste","teste","test@test","testlandia")
        adiciona_passaro(conn,"Araponga")
        adiciona_passaro(conn,"Staraptor")
        idUsuario=acha_usuario(conn,"Jukes")
        idPassaro1=acha_passaro(conn,"Araponga")
        idPassaro2=acha_passaro(conn,"Staraptor")
        adiciona_preferencia_a_passaro(conn,idUsuario,idPassaro1)
        adiciona_preferencia_a_passaro(conn,idUsuario,idPassaro2)
        preferencias1=lista_preferencia(conn)
        preferencias2=((idUsuario,idPassaro1),(idUsuario,idPassaro2))
        
        self.assertCountEqual(preferencias1,preferencias2)

    def test_lista_visualizadores_post(self):
        conn = self.__class__.connection
        
        nick = "Jovi"
        nome = "Junior"
        sobrenome = "Lista Visualiza"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn,nick, nome, sobrenome, email, cidade)
        id = acha_usuario(conn,nick)

        titulo= "Teste post2"
        texto = "aoskdoapsdk"
        url = "sokdapodkpao.com"
        adiciona_post(conn, id,1,titulo,texto, url)
        id_post = acha_post(conn, titulo)

        adiciona_visualizacao_post(conn, id_post, id, "Android", "192.129.3.1","Chrome", "2019-02-01")

        res=lista_visualizadores_post(conn, id_post)
        self.assertTrue(res)
        
        usuariosids=[id]
        for i in range(3):
            nick="JuninhoXD{}".format(i)
            adiciona_usuario(conn,nick,"Junior","Teste","teste@teste.com","testelandia")
            id = acha_usuario(conn,nick)
            adiciona_visualizacao_post(conn, id_post, id, "Android", "192.129.3.1","Chrome", "2019-02-01")
            usuariosids.append(id)

        res=lista_visualizadores_post(conn, id_post)
        self.assertCountEqual(res,usuariosids)
     
    def test_lista_posts_visualizados_usuario(self):
        conn = self.__class__.connection

        nick = "Jai"
        nome = "Junior"
        sobrenome = "Lista Visualiza"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"
        adiciona_usuario(conn,nick, nome, sobrenome, email, cidade)
        id = acha_usuario(conn,nick)

        titulo= "Teste post2"
        texto = "aoskdoapsdk"
        url = "sokdapodkpao.com"

        postsids=[]
        for i in range(3):
            titulo="TituloTest{}".format(i)
            adiciona_post(conn, id,1,titulo,texto, url)
            id_post = acha_post(conn, titulo)
            adiciona_visualizacao_post(conn, id_post, id, "Android", "192.129.3.1","Chrome", "2019-02-01")
            postsids.append(id_post)

        res=lista_posts_visualizados_usuario(conn,id)
        self.assertCountEqual(res,postsids)

    def teste_lista_mencoes(self):

        conn = self.__class__.connection
        adiciona_usuario(conn,"Jukes","teste","teste","test@test","testlandia")
        adiciona_usuario(conn,"Jovi","teste","teste","test@test","testlandia")
        adiciona_usuario(conn,"Rakin","teste","teste","test@test","testlandia")
       
        idUsuario1=acha_usuario(conn,"Jukes")
        idUsuario2=acha_usuario(conn,"Jovi")
        idUsuario3=acha_usuario(conn,"Rakin")

        adiciona_post(conn,idUsuario1,1,"titulo","texto","url")
        idPost=acha_post(conn,"titulo")
        menciona_usuario_em_post(conn,idPost,idUsuario2)
        menciona_usuario_em_post(conn,idPost,idUsuario3)

        mencoes1=lista_mencoes(conn)
        mencoes2=((idPost,idUsuario2),(idPost,idUsuario3))
        
        self.assertCountEqual(mencoes1,mencoes2)

    def lista_marca_passaro(self):
        conn = self.__class__.connection
        adiciona_usuario(conn,"Jukes","teste","teste","test@test","testlandia")
        adiciona_passaro(conn,"Araponga")
        adiciona_passaro(conn,"Sabia")
    
        idUsuario1=acha_usuario(conn,"Jukes")
        idPassaro1=acha_passaro(conn,"Araponga")
        idPassaro2=acha_passaro(conn,"Sabia")

        adiciona_post(conn,idUsuario1,1,"titulo","texto","url")
        idPost=acha_post(conn,"titulo")

        marca_passaro_em_post(conn,idPassaro1,idPost)
        marca_passaro_em_post(conn,idPassaro2,idPost)

        marcacoes1=lista_marca_passaro(conn)
        marcacoes2=((idPassaro1,idPost),(idPassaro2,idPost))
        
        self.assertCountEqual(marcacoes1,marcacoes2)

    def lista_post_like(self):
        conn = self.__class__.connection
        adiciona_usuario(conn,"Jukes","teste","teste","test@test","testlandia")
        adiciona_usuario(conn,"Jovi","teste","teste","test@test","testlandia")
        adiciona_usuario(conn,"Rakin","teste","teste","test@test","testlandia")
        idUsuario1=acha_usuario(conn,"Jukes")
        idUsuario2=acha_usuario(conn,"Jovi")
        idUsuario3=acha_usuario(conn,"Rakin")

        adiciona_post(conn,idUsuario1,1,"titulo","texto","url")
        idPost=acha_post(conn,"titulo")
        adiciona_post_like(conn,idPost,idUsuario2,"Like")
        adiciona_post_like(conn,idPost,idUsuario2,"Deslike")
        likes=lista_post_like(conn)
        likes2=((idPost,idUsuario2),(idPost,idUsuario3))
        self.assertCountEqual(likes,likes2)



def run_sql_script(filename):
    global config
    with open(filename, 'rb') as f:
        subprocess.run(
            [
                config['MYSQL'], 
                '-u', config['USER'], 
                '-p' + config['PASS'], 
                '-h', config['HOST']
            ], 
            stdin=f
        )

def setUpModule():
    filenames = [entry for entry in os.listdir() 
        if os.path.isfile(entry) and re.match(r'.*_\d{3}\.sql', entry)]
    for filename in filenames:
        run_sql_script(filename)

def tearDownModule():
    run_sql_script('script_criacao.sql')

if __name__ == '__main__':
    global config
    with open('config_tests.json', 'r') as f:
        config = json.load(f)
    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
    unittest.main(verbosity=2)