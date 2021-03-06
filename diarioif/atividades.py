# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout
# Create your views here.
from django.http import HttpResponse

from diarioif.models import *
import json

from django.template.response import TemplateResponse
from django.shortcuts import render_to_response, redirect, render
from datetime import datetime
from django.contrib.auth.models import User
from datetime import *
from random import choice
import django
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.utils.encoding import smart_str, smart_unicode

from unicodedata import normalize

from lancarnotas import defaultencode
from usuarios import temAcesso


@login_required()
def atividades(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    context = {}

    # Todos os cursos em que o professor leciona

    return render(request, 'atividades.html', context)



@login_required()
def criarAtividade(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    try:
        # Cria uma nova atividade avaliativa
        idAtividadeEdit = int(request.POST['idAtividadeEdit'])

        if idAtividadeEdit == -1:
            at = Atividade()
        else:
            at = Atividade.objects.get(pk=idAtividadeEdit)

        at.descricao = request.POST['descricao']

        idatrib = request.POST['idAtrib']
        atrib = AtribAula.objects.get(pk=idatrib)

        at.tipo = request.POST['tipo']


        dataInicio = request.POST['dataInicio']
        at.dataInicio = datetime.strptime(dataInicio, '%d/%m/%Y')

        dataFim = request.POST['dataFim']
        at.dataFim = datetime.strptime(dataFim, '%d/%m/%Y') if at.tipo == 'Trabalho' else at.dataInicio

        at.bimestre = int(request.POST['bimestre']) if request.POST['bimestre'] != 'PF' else 7 # CÓDIGO PARA A PF
        at.disciplina = atrib.disciplina
        at.calculo = request.POST['calculo']
        at.turma = atrib.turma

        at.save()

        if idAtividadeEdit != -1:
            return HttpResponse(1)


        alunosTurma = Notafalta.objects.values_list('aluno').filter(turma=atrib.turma).distinct()

        print "AlunosTurma: ", alunosTurma, ' Tamanho: ', len(alunosTurma)

        for aluno in alunosTurma:
            profileAl = ProfileUser.objects.get(pk=int(aluno[0]))
            ntat = NotaAtividade()
            ntat.aluno = profileAl
            ntat.atividade = at
            ntat.nota1 = 0.0
            ntat.nota2 = 0.0
            ntat.nota3 = 0.0
            ntat.nota4 = 0.0
            ntat.nota0 = 0.0
            ntat.save()

        return HttpResponse(1)
    except Exception, e:
        print "Error: %s " % e

    return HttpResponse(1)


@login_required()
def listAtividades(request):
    if temAcesso(request):
        return HttpResponse(status=500)
    atividades = []

    try:
        idatrib = request.POST['idAtrib']
        atrib = AtribAula.objects.get(pk=idatrib)

        ativs = Atividade.objects.filter(turma=atrib.turma, disciplina=atrib.disciplina).order_by('-dataFim')

        for atv in ativs:
            atividade = {}
            atividade['id'] = atv.id
            atividade['descricao'] = atv.descricao
            atividade['tipo'] = atv.tipo
            atividade['dataInicio'] = atv.dataInicio.strftime("%d/%m/%Y")
            atividade['dataFim'] = atv.dataFim.strftime("%d/%m/%Y") if atv.tipo == 'Trabalho' else ''
            atividade['calculo'] = atv.calculo
            atividade['bimestre'] = atv.bimestre if atv.bimestre != 7  else 'PF'

            atividades.append(atividade)
    except Exception, e:
        print "Erro %s " % e

    return HttpResponse(json.dumps(atividades), content_type="application/json")

@login_required()
def removeAtiv(request):
    if temAcesso(request):
        return HttpResponse(status=500)
    try:
        idativ = int(request.POST['idativ'])
        atv = Atividade.objects.get(pk=idativ)
        atv.delete()

        return  HttpResponse(1)
    except Exception, e:
        print "Error %s " % e

    return  HttpResponse(-1)

@login_required()
def getAlunosAtivs(request):
    if temAcesso(request):
        return HttpResponse(status=500)
    alunosList = []
    try:

        idativ = int(request.POST['idativ'])
        atv = Atividade.objects.get(pk=idativ)

        notasAtvs = NotaAtividade.objects.filter(atividade=atv)

        for AtNt in notasAtvs:
            print "oi"
            al = {}

            al['id'] = AtNt.id
            al['nome'] = AtNt.aluno.nome
            al['nota0'] = AtNt.nota0
            al['nota1'] = AtNt.nota1
            al['nota2'] = AtNt.nota2
            al['nota3'] = AtNt.nota3
            al['nota4'] = AtNt.nota4

            alunosList.append(al)


    except Exception, e:
        print "Error %s " % e

    return HttpResponse(json.dumps(alunosList, default=defaultencode), content_type="application/json")

@login_required()
def salvarNotasAtivs(request):
    if temAcesso(request):
        return HttpResponse(status=500)
    try:
        id = int(request.POST['id'])
        ntfa = NotaAtividade.objects.get(pk=id)
        ntfa.nota0 = request.POST['nota0']
        ntfa.nota1 = request.POST['nota1']
        ntfa.nota2 = request.POST['nota2']
        ntfa.nota3 = request.POST['nota3']
        ntfa.nota4 = request.POST['nota4']

        ntfa.save()

        return HttpResponse(1)
    except:
        print 'err'


    return HttpResponse(-1)

