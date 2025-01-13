from Models.Usuario import Usuario

class Aluno(Usuario):
    def __init__(self, nome, senha, email, matricula):
        super().__init__(nome, senha, email)
        self._matricula = matricula
        self._listChaves = []

    def setMatricula(self, matricula):
        self._matricula = matricula

    def getMatricula(self):
        return self._matricula

    def adicionarChave(self, chave):
        pass

    def retornarChave(self, id_chave):
        pass

    def removerChave(self, chave):
        self._listChaves.remove(chave)

    def acessarChaves(self):
        for i in self._listChaves:
            pass

    def setListChaves(self, lista):
        self._listChaves = lista

    def passarChaveAluno(self, chave, aluno):
        pass
    def passarChave(self, funcionario):
        pass
