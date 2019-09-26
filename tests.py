from biblioteca import *


def testa_criar_usuario(self):
    with self.cls.connection.cursor() as cursor:
        cursor.execute("""
                    INSERT INTO usuarios (nome, sobrenome, email, cidade) 
                    VALUES (%s, %s, %s, %s);
                    """, ("carlos","adao","carlos@adao","carlinhos"))
        res = criar_usuario(self.cls.connection, "carlos", "adao", "carlos@adao", "carlinhos")
        self.assertEqual(res, 1)

