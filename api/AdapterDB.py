import pymysql
from datetime import datetime

class AdapterDB:
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )

    def fetch_all(self, query, params = None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def fetch_one(self, query, params = None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()

    def execute_query(self, query, params = None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor.rowcount  # Retorna o número de linhas afetadas

    def close(self):
        self.connection.close()

    def get_usuarios(self, somente_ativos = True,
                     id=0, email='', nome='', matricula='', telefone='', nivel=''):

        query = "SELECT * FROM usuarios WHERE 1=1"
        params = []  # Lista para armazenar os valores dos parâmetros

        if somente_ativos:
            query += " AND ativo = %s"
            params.append(1)  # Adiciona apenas usuários ativos

        if id != 0:
            query += " AND id = %s"
            params.append(id)

        if email:
            query += " AND email = %s"
            params.append(email)

        if nome:
            query += " AND nome LIKE %s"
            params.append('%' + nome + '%')

        if matricula:
            query += " AND matricula = %s"
            params.append(matricula)

        if telefone:
            query += " AND telefone = %s"
            params.append(telefone)

        if nivel:
            query += " AND nivel = %s"
            params.append(nivel)

        return self.fetch_all(query, params)


    def get_chaves(self, somente_ativos = True, id = 0, nome = '', posse = 0, qrcode = ''):
        query = "SELECT * FROM chaves WHERE 1=1"
        params = []  # Lista para armazenar os valores dos parâmetros

        if somente_ativos:
            query += " AND ativo = %s"
            params.append(1)

        if id != 0:
            query += " AND id = %s"
            params.append(id)

        if nome:
            query += " AND nome LIKE %s"
            params.append('%' + nome + '%')

        if posse != 0:
            query += " AND posse = %s"
            params.append(posse)

        if qrcode:
            query += " AND qrcode = %s"
            params.append(qrcode)

        return self.fetch_all(query, params)

    def get_historico(self, data_inicio, data_fim, hora_inicio, hora_fim, chave, usuario_origem, usuario_destino):
        query = """
            SELECT h.*, c.nome AS nome_chave, u.nome AS nome_usuario_origem
            FROM historico h
            LEFT JOIN chaves c ON h.chave = c.id
            LEFT JOIN usuarios u ON h.usuario_origem = u.id
            WHERE 1=1
        """
        params = []

        if data_inicio:
            query += " AND h.datahora >= %s"
            params.append(data_inicio)
        if data_fim:
            query += " AND h.datahora <= %s"
            params.append(data_fim)
        if hora_inicio:
            query += " AND h.datahora >= %s"
            params.append(hora_inicio)
        if hora_fim:
            query += " AND h.datahora <= %s"
            params.append(hora_fim)
        if chave:
            query += " AND h.chave = %s"
            params.append(chave)
        if usuario_origem:
            query += " AND h.usuario_origem = %s"
            params.append(usuario_origem)
        if usuario_destino:
            query += " AND h.usuario_destino = %s"
            params.append(usuario_destino)

        return self.fetch_all(query, params)

    def get_alunos_chaves(self, somente_ativos = True, id = 0, chave = 0, aluno= 0, responsavel = 0):

        query = "SELECT * FROM alunos_chaves WHERE 1=1"
        params = []  # Lista para armazenar os valores dos parâmetros

        if somente_ativos:
            query += " AND ativo = %s"
            params.append(1)

        if id != 0:
            query += " AND id = %s"
            params.append(id)

        if chave != 0:
            query += " AND chave = %s"
            params.append(chave)

        if aluno != 0:
            query += " AND aluno = %s"
            params.append(aluno)

        if responsavel != 0:
            query += " AND responsavel = %s"
            params.append(responsavel)

        return self.fetch_all(query, params)

    def add_usuario(self, nome, email, senha, nivel, matricula = None, telefone = None):
        query = "INSERT INTO usuarios (nome, email, senha, matricula, telefone, nivel) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (nome, email, senha, matricula, telefone, nivel)

        return self.execute_query(query, params)

    def add_chave(self, nome, qrcode):
        query = "INSERT INTO chaves (nome, qrcode, posse) VALUES (%s, %s, %s)"
        params = (nome, qrcode, 1)
        resultado = self.execute_query(query, params)
        self.connection.commit()  # Confirma a  transação
        self.connection.close()  # Fecha a conexão para garantir atualização
        return resultado

    def add_historico(self, chave, usuario_origem, usuario_destino, datahora = None):
        if datahora is None:
            datahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = "INSERT INTO historico (chave, usuario_origem, usuario_destino, datahora) VALUES (%s, %s, %s, %s)"
        params = (chave, usuario_origem, usuario_destino, datahora)

        return self.execute_query(query, params)

    def add_aluno_chave(self, chave, aluno, responsavel):
        query = "INSERT INTO alunos_chaves (chave, aluno, responsavel) VALUES (%s, %s, %s)"
        params = (chave, aluno, responsavel)

        return self.execute_query(query, params)

    def edit_usuario(self, id, email = None, nome = None, matricula = None, telefone = None, nivel = None):

        query = "UPDATE usuarios SET"
        updates = []
        params = []

        if email is not None:
            updates.append(" email = %s")
            params.append(email)

        if nome is not None:
            updates.append(" nome = %s")
            params.append(nome)

        if matricula is not None:
            updates.append(" matricula = %s")
            params.append(matricula)

        if telefone is not None:
            updates.append(" telefone = %s")
            params.append(telefone)

        if nivel is not None:
            updates.append(" nivel = %s")
            params.append(nivel)

        query += ",".join(updates) + " WHERE id = %s"
        params.append(id)

        return self.execute_query(query, params)

    def pegarChave(self, chave, id_user):
        cursor = self.connection.cursor()

        # Atualiza a posse da chave diretamente pelo QR Code
        update_query = "UPDATE chaves SET posse = %s WHERE qrcode = %s"
        cursor.execute(update_query, (id_user, chave.getQrCode()))
        self.connection.commit()

        # Verifica se alguma linha foi modificada
        if cursor.rowcount > 0:
            return True
           #print("Chave atualizada com sucesso!")

        cursor.close()
        return 2  # Indica erro


    def edit_chave(self, id, nome = None, qrcode = None, posse = None):

        query = "UPDATE chaves SET"
        updates = []
        params = []

        if nome is not None:
            updates.append(" nome = %s")
            params.append(nome)

        if qrcode is not None:
            updates.append(" qrcode = %s")
            params.append(qrcode)

        if posse is not None:
            updates.append(" posse = %s")
            params.append(posse)

        query += ",".join(updates) + " WHERE id = %s"
        params.append(id)

        return self.execute_query(query, params)

    def edit_historico(self, id, chave = None, usuario_origem = None, usuario_destino = None, datahora = None):

        query = "UPDATE historico SET"
        updates = []
        params = []

        if chave is not None:
            updates.append(" chave = %s")
            params.append(chave)

        if usuario_origem is not None:
            updates.append(" usuario_origem = %s")
            params.append(usuario_origem)

        if usuario_destino is not None:
            updates.append(" posse = %s")
            params.append(usuario_destino)

        if datahora is not None:
            updates.append(" datahora = %s")
            params.append(datahora)

        query += ",".join(updates) + " WHERE id = %s"
        params.append(id)

        return self.execute_query(query, params)

    def edit_aluno_chave(self, id, chave = None, aluno = None, responsavel = None):
        query = "UPDATE alunos_chaves SET"
        updates = []
        params = []

        if chave is not None:
            updates.append(" chave = %s")
            params.append(chave)

        if aluno is not None:
            updates.append(" aluno = %s")
            params.append(aluno)

        if responsavel is not None:
            updates.append(" responsavel = %s")
            params.append(responsavel)

        query += ",".join(updates) + " WHERE id = %s"
        params.append(id)

        return self.execute_query(query, params)

    def remove_usuario(self, id):
        query = "UPDATE usuarios SET ativo = 0 WHERE id = %s"
        params = []

        params.append(id)

        return self.execute_query(query, params)

    def remove_chave(self, id):
        query = "UPDATE chaves SET ativo = 0 WHERE id = %s"
        params = []

        params.append(id)

        return self.execute_query(query, params)

    def remove_historico(self):
        query = "UPDATE historico SET ativo = 0 WHERE id = %s"
        params = []

        params.append(id)

        return self.execute_query(query, params)

    def remove_aluno_chave(self):
        query = "UPDATE alunos_chaves SET ativo = 0 WHERE id = %s"
        params = []

        params.append(id)

        return self.execute_query(query, params)

    def buscar_chave_por_qrcode(self, qrcode):
        from Models.Chave import Chave

        # Criar a query para buscar a chave no banco de dados
        query = "SELECT * FROM chaves WHERE qrcode = %s"
        params = (qrcode,)

        # Executa a query e retorna o resultado
        resultado = self.fetch_one(query, params)  # Assumindo que fetch_one é um método que retorna um único resultado

        # Verificar se algum resultado foi encontrado
        if resultado:
            # Caso encontre, retorna os dados da chave
            chave = Chave("","","","")  # Criando um objeto chave
            chave.setId(resultado['id'])
            chave.setNomeSala(resultado['nome'])
            chave.setQrCode(resultado['qrcode'])
            chave.setPosse(resultado['posse'])
            return chave  # Retorna o objeto chave preenchido
        else:
            return None  # Caso não encontre a chave com o qrcode especificado
