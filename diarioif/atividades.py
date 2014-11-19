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


@login_required()
def atividades(request):

    context = {}

    # Todos os cursos em que o professor leciona

    return render(request, 'atividades.html', context)



@login_required()
def criarAtividade(request):

    try:

        # Cria uma nova atividade avaliativa
        at = Atividade()
        at.descricao = request.POST['descricao']

        dataInicio = request.POST['dataInicio']
        at.dataInicio = datetime.strptime(dataInicio, '%d/%m/%Y')

        dataFim = request.POST['dataFim']
        at.dataFim = datetime.strptime(dataFim, '%d/%m/%Y')

        at.bimestre = request.POST['bimestre']
        at.disciplina = request.POST['disciplina']
        at.calculo = request.POST['calculo']
        at.turma = request.POST['turma']
        at.tipo = request.POST['tipo']
        at.save()

        idatrib = request.POST['idatirb']
        atrib = AtribAula.objects.get(pk=idatrib)

        alunosTurma = Notafalta.objects.values_list('aluno').filter(turma=atrib.turma).distinct()
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

