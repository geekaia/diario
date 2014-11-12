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


class Presenca(models.Model):
    data = models.DateField()
    aluno = models.ForeignKey(User)
    turma = models.ForeignKey(Turma)
    presencafalta = models.BooleanField()


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
    disciplina = models.ForeignKey(Disciplina)
    turma = models.ForeignKey(Turma)
    data = models.DateField()

class Conteudo(models.Model):
    conteudo = models.TextField()
    dia = models.ForeignKey(Dia)

class Chamada(models.Model):
    presenca = models.BooleanField(default=True)
    dia = models.ForeignKey(Dia)
    numero = models.IntegerField() # id da aula. Para 4 aulas temos 1, 2, 3, 4 ....


# Tenho que pensar em uma atividade avlaiativa
# Como criar com exercícios randômicos
# Pensar em como criar classes de forma randômica
# Tenho que verificar a segurança de aocrdo com os níveis dos usuários

