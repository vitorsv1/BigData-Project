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

    def test_criar_usuario(self):
        conn = self.__class__.connection
        
        nick = "Jukes"
        nome = "Junior"
        sobrenome = "Test"
        email = "junior.test@hotmail.com"
        cidade = "Testlandia"

        criar_usuario(conn, nick, nome, sobrenome, email, cidade)

        try:
            criar_usuario(conn, nick, nome, sobrenome, email, cidade)
            self.fail('Não deveria ter adicionado o mesmo usuario duas vezes')
        except ValueError as e:
            pass
        
        id = acha_usuario(conn, nick)
        self.assertIsNotNone(id)

        id = acha_usuario(conn, 'pokadskopdsa')
        self.assertIsNone(id)

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
    run_sql_script('tear_down.sql')

if __name__ == '__main__':
    global config
    with open('config_tests.json', 'r') as f:
        config = json.load(f)
    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
    unittest.main(verbosity=2)
