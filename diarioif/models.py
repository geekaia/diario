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
    anoEntrada = models.CharField(max_length=5, blank=True, null=True)
    curso = models.ForeignKey(Curso)
    dataTranferencia = models.DateField()

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
    nome = models.CharField(max_length=255, blank=True, null=True)
    anosemestre = models.IntegerField(11)
    anoturma = models.CharField(max_length=5, blank=True, null=True)


class Disciplina(models.Model):
    curso = models.ForeignKey(Curso)
    nome = models.CharField(max_length=255, blank=True, null=True)
    periodo = models.IntegerField(11)
    horaaula = models.CharField(max_length=255, blank=True, null=True)
    hora = models.CharField(max_length=10, blank=True, null=True)

class Bimestre(models.Model):
    ano = models.CharField(max_length=5, blank=True, null=True)
    bimestreSemestre = models.CharField(max_length=1, blank=True, null=True)
    dataInicio = models.DateField()
    dataInicio = models.DateField()


class Presenca(models.Model):
    data = models.DateField()
    aluno = models.ForeignKey(User)
    turma = models.ForeignKey(Turma)
    presencafalta = models.BooleanField()


class AtribAula(models.Model):
    disciplinas = models.ForeignKey(Disciplina)


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





