class TelaLogin():
    def __init__(self, email="", senha="", nome=""):
        self.email = email
        self.senha = senha
        self.nome = nome
        self.id = ""

    def setEmail(self, email):
        self.email = email

    def setSenha(self, password):
        self.senha = password

    def setNome(self, nome):
        self.nome = nome

    def setId(self, id):
        self.id = id

    def getEmail(self):
        return self.email

    def getSenha(self):
        return self.senha

    def getNome(self):
        return self.nome

    def getId(self):
        return self.id
