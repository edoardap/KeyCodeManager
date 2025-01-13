from Models.Funcionario import Funcionario

class Professor(Funcionario):
    def __init__(self, nome, senha, email, contrato, matricula):
        super().__init__(nome, senha, email, contrato)
        self._matricula = matricula

    def setMatricula(self, matricula):
        self._matricula = matricula

    def getMatricula(self):
        return self._matricula

    def consultarChaveAluno(self, aluno):
        # Consulta a tabela alunos_chaves a procura das chaves que o aluno tem permissão(obs: daquele professor)
        pass

    def concederPermissao(self, aluno, chave):
        # adiciona permissao
        pass

    def revogarPermissao(self, aluno, chave):
        # deleta a permissao
        pass
