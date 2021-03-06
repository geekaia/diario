# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ProfileUser(models.Model):
    user = models.ForeignKey(User)
    nome = models.CharField(max_length=255, blank=True, null=True)
    mae = models.CharField(max_length=255, blank=True, null=True)
    pai = models.CharField(max_length=255, blank=True, null=True)
    nascimento = models.DateField(blank=True, null=True)
    telefone1 = models.CharField(max_length=20, blank=True, null=True)
    telefone2 = models.CharField(max_length=20, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    orgaoexp = models.CharField(max_length=30, blank=True, null=True)
    cpfcnpj = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    nacionalidade = models.CharField(max_length=255, blank=True, null=True)
    naturalidade = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.CharField(max_length=255, blank=True, null=True)
    cep = models.CharField(max_length=30, blank=True, null=True)
    bairro = models.CharField(max_length=255, blank=True, null=True)
    rua = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=255, blank=True, null=True)
    complemento = models.TextField()
    observacoes = models.TextField()
    tipo = models.CharField(max_length=255, blank=True, null=True)

class Curso(models.Model):
    nome = models.CharField(max_length=255, blank=True, null=True)
    anoGrade = models.CharField(max_length=255, blank=True, null=True)
    periodo = models.CharField(max_length=255, blank=True, null=True)
    quantPeriodo = models.IntegerField(11)
    habilitacao = models.CharField(max_length=255, blank=True, null=True)
    resolucaoreconhecimento = models.CharField(max_length=255, blank=True, null=True)
    dataPublicacao = models.CharField(max_length=255, blank=True, null=True)
    formaingresso = models.CharField(max_length=255, blank=True, null=True)
    avaliacaopor = models.CharField(max_length=255, blank=True, null=True)


class Matricula(models.Model):
    user = models.ForeignKey(User)
    curso = models.ForeignKey(Curso)
    dataMatricula = models.DateField()

    # o aluno só pode ter uma matrícula
    atual = models.BooleanField()

class SituacaoMatricula(models.Model):
    """
        Com esta entidade podemos armazenazr o histórico de uma Matrícula. Com isto poderemos ter um histórico completo da situação
        Pois os usuários vai e vão.
    """
    matricula = models.ForeignKey(Matricula)
    situacao = models.CharField(max_length=255, blank=True, null=True)
    data = models.DateField(blank=True, null=True)

class Turma(models.Model):
    curso = models.ForeignKey(Curso)
    nome = models.CharField(max_length=5, blank=True, null=True)
    anosemestre = models.IntegerField(11)
    anoturma = models.CharField(max_length=10, blank=True, null=True)


class Disciplina(models.Model):
    curso = models.ForeignKey(Curso)
    nome = models.CharField(max_length=255, blank=True, null=True)
    periodo = models.IntegerField(11)
    horaaula = models.CharField(max_length=255, blank=True, null=True)
    hora = models.CharField(max_length=10, blank=True, null=True)


class Bimestre(models.Model):
    ano = models.CharField(max_length=5, blank=True, null=True)
    bimestreSemestre = models.CharField(max_length=15, blank=True, null=True)
    numero = models.CharField(max_length=5, blank=True, null=True) # número do bimestre 4 para anual e 2 para semestral
    dataInicio = models.DateField()
    dataFim = models.DateField()


class AtribAula(models.Model):
    disciplina = models.ForeignKey(Disciplina)
    turma = models.ForeignKey(Turma)
    professor = models.ForeignKey(ProfileUser, blank=True, null=True)

    # default 1 ano para cursos anuais e 6 meses para cursos semestrais
    periodoInicio = models.DateField()
    periodoFim = models.DateField()
    acesso = models.BooleanField()
    # Esta variável permite finalizar o ano.

class Uf(models.Model):
    sigla = models.CharField(max_length=2, blank=True, null=True)
    nome = models.CharField(max_length=255, blank=True, null=True)


class Cidade(models.Model):
    uf = models.ForeignKey(Uf)
    nome = models.CharField(max_length=500, blank=True, null=True)


class Bairro(models.Model):
    cidade = models.ForeignKey(Cidade)
    nome = models.CharField(max_length=255, blank=True, null=True)

class Rua(models.Model):
    bairro = models.ForeignKey(Bairro)
    tipo = models.IntegerField(11)
    nome = models.CharField(max_length=500, blank=True, null=True)
    cep = models.CharField(max_length=50, blank=True, null=True)


class Notafalta(models.Model):
    aluno = models.ForeignKey(ProfileUser)
    disciplina = models.ForeignKey(Disciplina)
    turma = models.ForeignKey(Turma)
    nota1b = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    nota2b = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    nota3b = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    nota4b = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    falta1b = models.IntegerField()
    falta2b = models.IntegerField()
    falta3b = models.IntegerField()
    falta4b = models.IntegerField()
    falta5b = models.IntegerField()
    mediafinal = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    recuperacao = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    situacaofinal = models.CharField(max_length=255, blank=True, null=True)
    mediaanual = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    mediapospf = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)


class Dia(models.Model):
    atrib = models.ForeignKey(AtribAula)
    data = models.DateField()

class Conteudo(models.Model):
    conteudo = models.TextField()
    dia = models.ForeignKey(Dia)

class Presenca(models.Model):
    dia = models.ForeignKey(Dia)
    aluno = models.ForeignKey(ProfileUser)
    presente = models.BooleanField(default=True)


class Atividade(models.Model):
    """
        Cadastra as atividades avaliativas de um bimestre
    """
    descricao = models.TextField(blank=True, null=True)
    dataInicio = models.DateField() # periodo que pode ser entregue a atividade
    dataFim = models.DateField() # é igual ao início quando a atividade no início
    bimestre = models.IntegerField()
    disciplina = models.ForeignKey(Disciplina)
    calculo = models.CharField(max_length=10) # Soma ou Média
    turma = models.ForeignKey(Turma)

    # atitudinal, prova, trabalho, lista de exercicios, prova final, recuperação bimestral
    tipo = models.CharField(max_length=255)

class NotaAtividade(models.Model):
    aluno = models.ForeignKey(ProfileUser)
    atividade = models.ForeignKey(Atividade)
    nota0 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    nota1 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    nota2 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    nota3 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    nota4 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)


class Building(models.Model):
    nome = models.CharField(max_length=255)

class Sala(models.Model):
    build = models.ForeignKey(Building)
    nome = models.CharField(max_length=255)



class DiaExcept(models.Model):
    """
    Dias em que ocorre coisas diferentes no campus. Por obrigação tem que adicionar os sábados que não tem aula, pois no sábado pode ter aula..
    """
    # Aqui é ano letivo e não o ano corrente, apesar de que sempre pegamos o ano atual para termos como base
    ano = models.CharField(max_length=10)
    # por padrão o domingo não pode ter aula e, portanto já fica desmarcado no registro
    dataInicio = models.DateField()
    dataFim = models.DateField(blank=True, null=True)

    # FD - Férias Docentes, F - Feriados, PF - Período de Provas Finais, PFAC - Ponto Facultativo, SB - Sábado(Este é ao contrário dos demais aqui habilita registrar no sábado)
    # PFAC - Ponto Facultativo , RC - Recesso
    tipo = models.CharField(max_length=50)
    descricao = models.CharField(max_length=255)

class HorariodeAula(models.Model):
    # Ano letivo corrente
    ano = models.CharField(max_length=10)
    # Matutino, Vespertino, Noturno
    turno = models.CharField(max_length=255)
    horaInicio = models.TimeField()
    horaFim = models.TimeField()

