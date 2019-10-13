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
        
        id = acha_usuario(conn, nick)
        self.assertIsNotNone(id)

        id = acha_usuario(conn, 'pokadskopdsa')
        self.assertIsNone(id)

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
        adiciona_post(conn, id,titulo,texto, url)
        id_post = acha_post(conn, titulo)

        adiciona_visualizacao_post(conn, id_post, id, "Android", "192.129.3.1","Chrome", "2019-02-01")

        try:
            adiciona_visualizacao_post(conn, id_post, id, "Android", "192.129.3.1","Chrome", "2019-02-01")
            self.fail("Não deveria adicionar uma visualizacao nova")
        except ValueError as e:
            pass

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
        adiciona_post(conn, id,titulo,texto, url)
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
            adiciona_post(conn, id,titulo,texto, url)
            id_post = acha_post(conn, titulo)
            adiciona_visualizacao_post(conn, id_post, id, "Android", "192.129.3.1","Chrome", "2019-02-01")
            postsids.append(id_post)

        res=lista_posts_visualizados_usuario(conn,id)
        self.assertCountEqual(res,postsids)

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

    def test_menciona_usuario(self):
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
        adiciona_post(conn, idJu, "Breskein", "Muito legal @jovi @rakin","askdpaosd.com")
        idPost = acha_post(conn, "Breskein")

        self.assertIsNotNone(idJovi)
        self.assertIsNotNone(idJu)
        self.assertIsNotNone(idPost)

        mencoes = lista_mencoes(conn)
        rak = (idPost, idRakin)
        jovi = (idPost, idJovi)

        self.assertEqual(mencoes[0], jovi)
        self.assertEqual(mencoes[1], rak)

    def test_marca_passaro(self):
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
        
        adiciona_post(conn, idJu, "Breskein", "Muito legal esse #bicudo #canario","askdpaosd.com")
        idPost = acha_post(conn, "Breskein")
        
        marcacoes = lista_marca_passaro(conn)
        t1 = (idBicudo, idPost)
        t2 = (idCanario, idPost)

        self.assertEqual(marcacoes[0], t1)
        self.assertEqual(marcacoes[1], t2)

    def test_adiciona_preferencia_de_passaro(self):
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
        adiciona_post(conn, id,titulo,texto, url)
        id_post = acha_post(conn, titulo)
        
        desativa_post(conn, id_post)

        res = esta_desativado_post(conn, id_post)
        self.assertFalse(res)


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
