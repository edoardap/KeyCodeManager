
## Metodos:

#### Read:
1. readHistorico("completo") ou readHistorico("periodo", data_inicial(datetime), data_final(datetime)): retorna uma lista de tuplas
2. readChave (recebe um id (int)): retorna uma chave ou [ ]
3. readALunoChave(id_aluno, id_chave, id_professor)(0 se nao quizer considerar no filtro): retorna uma lista de tuplas
4. readFuncionario/ readProfessor/ readGerente/ readAluno (recebe um email (str)): retorna o objeto ou []

#### Write:
1. writeHistorico(Chave, Usuario)
2. writeAlunoChave(Aluno, Chave, Professor)
3. writeChave/ writeUsuario/ writeAluno/ writeFuncionario/ writeGerente/ writeProfessor (o objeto referente)

#### Update:
1. Nao ha update historico
2. updateAlunoChave(id(da tabela alunos_chaves), Aluno, Chave, Professor)
3. updateChave/ updateUsuario/ updateAluno/ updateFuncionario/ updateGerente/ updateProfessor(o objeto referente)

#### Delete:
1. Nao ha delete historico
2. deleteAlunoChave((Aluno, Chave, Professor))
3.  deleteChave/ deleteUsuario/ deleteAluno/ deleteFuncionario/ deleteGerente/ deleteProfessor(o objeto referente)

