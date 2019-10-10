from biblioteca import *

class TestProjeto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global config
        cls.connection = pymysql.connect(
            host=config['localhost'],
            user=config['megadados'],
            password=config['megadados2019'],
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

    def test_criar_usuario(self):
        conn = self.__class__.connection
        
        nome = "Junior"
        sobrenome = "Test"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"

        criar_usuario(conn, nome, sobrenome, email, cidade)

        try:
            criar_usuario(conn, nome, sobrenome, email, cidade)
            self.fail('Não deveria ter adicionado o mesmo usuario duas vezes')
        except ValueError as e:
            pass
        
        
        
        with conn.cursor() as cursor:
        