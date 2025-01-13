from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, nome, senha, email):
        self._nome = nome
        self._email = email
        self._senha = senha

    def setNome(self, nome):
        self._nome = nome

    def setEmail(self, email):
        self._email = email

    def setSenha(self, senha):
        self._senha = senha

    def getNome(self):
        return self._nome

    def getEmail(self):
        return self._email

    def getSenha(self):
        return self._senha


    @abstractmethod
    def pegarChave(self, chave):
        pass

    @abstractmethod
    def passarChave(self, funcionario):
        pass
