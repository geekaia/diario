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

from random import choice
import django
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from decimal import *


import json
from importar import FileUploadedForm
from usuarios import temAcesso

from utils import defaultencode

@login_required()
def notas(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    context = {}
    cursos = Curso.objects.all()
    context['cursos'] = cursos

    profs = ProfileUser.objects.filter(tipo='Professor')
    context['profs'] = profs
    context['form'] = FileUploadedForm

    return render(request, 'lancarnotas.html', context)




@login_required()
def notasAlunosTurma(request):
    if temAcesso(request):
        return HttpResponse(status=500)
    alunos = []

    try:
        turma = Turma.objects.get(pk=request.POST['idturma'])
        atrib = AtribAula.objects.get(pk=request.POST['atrib'])
        data = Notafalta.objects.filter(turma=turma, disciplina=atrib.disciplina)

        for i in data:
            # no meu caso precisa ter uma entrada em nota falta
            aluno = {}
            aluno['id'] = i.id
            aluno['nome'] = i.aluno.nome
            print "i.nota1b ", i.nota1b, " if else ", 0.0 if type(i.mediafinal)==type(None) else i.nota1b
            aluno['nota1b'] = 0.0 if type(i.nota1b)==type(None) else i.nota1b
            aluno['nota2b'] = 0.0 if type(i.nota2b)==type(None) else i.nota2b
            aluno['nota3b'] = 0.0 if type(i.nota3b)==type(None) else i.nota3b
            aluno['nota4b'] = 0.0 if type(i.nota4b)==type(None) else i.nota4b
            aluno['falta1b'] = i.falta1b
            aluno['falta2b'] = i.falta2b
            aluno['falta3b'] = i.falta3b
            aluno['falta4b'] = i.falta4b
            aluno['mediafinal'] = 0.0 if type(i.mediafinal)==type(None) else i.mediafinal
            aluno['recuperacao'] = 0.0 if type(i.recuperacao)==type(None) else i.recuperacao
            aluno['situacaofinal'] = '' if type(i.situacaofinal)==type(None) else i.situacaofinal
            aluno['mediaanual'] = 0.0 if type(i.mediaanual)==type(None) else i.mediaanual
            aluno['mediapospf'] = 0.0 if type(i.mediapospf)==type(None) else i.mediapospf

            alunos.append(aluno)
    except Exception, e:
        print 'Err %s ' % e

    return HttpResponse(json.dumps(alunos, default=defaultencode), content_type="application/json")


@login_required()
def saveNotas(request):
    if temAcesso(request):
        return HttpResponse(status=500)
    try:
        nota = Notafalta.objects.get(pk=request.POST['id'])
        nota.nota1b = Decimal(request.POST['nota1b'])
        nota.nota2b = Decimal(request.POST['nota2b'])
        nota.nota3b = Decimal(request.POST['nota3b'])
        nota.nota4b = Decimal(request.POST['nota4b'])
        nota.falta1b = int(request.POST['falta1b'])
        nota.falta2b = int(request.POST['falta2b'])
        nota.falta3b = int(request.POST['falta3b'])
        nota.falta4b = int(request.POST['falta4b'])
        nota.recuperacao = Decimal(request.POST['recuperacao'])
        nota.situacaofinal = request.POST['situacaofinal']

        # Falta gera uma função que recalcule a situação final do aluno
        nota.save()


        return HttpResponse(1)
    except Exception, e:
        print "Error %s", e

        return HttpResponse(-1)


@login_required()
def saveNotasImport(request):
    if temAcesso(request):
        return HttpResponse(status=500)
    try:
        nota = Notafalta.objects.get(pk=request.POST['id'])
        nota.nota1b = Decimal(request.POST['nota1b'])
        nota.nota2b = Decimal(request.POST['nota2b'])
        nota.nota3b = Decimal(request.POST['nota3b'])
        nota.nota4b = Decimal(request.POST['nota4b'])
        nota.falta1b = int(request.POST['falta1b'])
        nota.falta2b = int(request.POST['falta2b'])
        nota.falta3b = int(request.POST['falta3b'])
        nota.falta4b = int(request.POST['falta4b'])
        nota.recuperacao = Decimal(request.POST['recuperacao'])
        nota.situacaofinal = request.POST['situacaofinal']

        # Falta gera uma função que recalcule a situação final do aluno
        nota.save()


        return HttpResponse(1)
    except Exception, e:
        print "Error %s", e

        return HttpResponse(-1)


@login_required()
def quantBimestre(request):
    if temAcesso(request):
        return HttpResponse(status=500)
    try:
        # Byidturma
        try:
            turma = Turma.objects.get(pk=request.POST['idturma'])
            print 'By idturma'
        except:
            print 'By idatrib'
            atrib = AtribAula.objects.get(pk=int(request.POST['idatrib']))
            turma = atrib.turma

        quantP = 0
        if turma.curso.periodo == 'Ano' and turma.curso.avaliacaopor == 'Bimestre':
            quantP = 4
        elif turma.curso.periodo == 'Ano' and turma.curso.avaliacaopor == 'Semestre':
            quantP = 2
        elif turma.curso.periodo == 'Semestre' and turma.curso.avaliacaopor == 'Bimestre':
            quantP = 2
        # Ainda falta determinar o início e fim pelo período
        elif turma.curso.periodo == 'Semestre' and turma.curso.avaliacaopor == 'Semestre':
            quantP = 1

        return HttpResponse(quantP)
    except:
        return HttpResponse(-1)



