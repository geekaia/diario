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
getcontext().rounding=ROUND_HALF_UP # Para arredondar


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

    # profs = ProfileUser.objects.filter(tipo='Professor')
    # context['profs'] = profs
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


def toDecimal(val):
    try:
        return Decimal(str(val))
    except:
        return Decimal(str(0.0))

def toInt(val):
    try:
        return int(val)
    except:
        return 0


@login_required()
def saveNotas(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    user = User.objects.get(pk=request.user.id)
    prof = ProfileUser.objects.get(user=user)

    rec = ''
    try:
        rec = request.POST['situacaofinal']
    except:
        print 'Erro sitf'

    try:
        nota = Notafalta.objects.get(pk=int(request.POST['id']))

        # Prosso salvar esta nota -- aqui evita que um professor salve notas e/ou presenças de outros professores
        if prof.tipo == 'Professor':
            canAtr = AtribAula.objects.filter(disciplina=nota.disciplina, turma=nota.turma, professor=prof)
            if len(canAtr) == 0:
                return HttpResponse(-1)


        nota.nota1b = toDecimal(request.POST['nota1b'])
        nota.nota2b = toDecimal(request.POST['nota2b'])
        nota.nota3b = toDecimal(request.POST['nota3b'])
        nota.nota4b = toDecimal(request.POST['nota4b'])
        nota.falta1b = toInt(request.POST['falta1b'])
        nota.falta2b = toInt(request.POST['falta2b'])
        nota.falta3b = toInt(request.POST['falta3b'])
        nota.falta4b = toInt(request.POST['falta4b'])
        nota.recuperacao = toDecimal(request.POST['recuperacao'])

        getcontext().prec=3


        # Para cursos anuais e bimestrais
        md = Decimal(str((float(nota.nota1b) + float(nota.nota2b) + float(nota.nota3b) + float(nota.nota4b))/4.))
        nota.mediaanual = round(md, 2) # Arredonda igual o excell

        # print 'okkkk'


        if nota.mediaanual >= 6:
            nota.situacaofinal = 'Aprovado'
            nota.mediafinal = nota.mediaanual
            nota.mediapospf = nota.mediaanual
        elif nota.mediaanual < 3:
            nota.situacaofinal = 'Reprovado' if nota.situacaofinal !='APC' else 'APC'
            nota.mediafinal = nota.mediaanual
            nota.mediapospf = nota.mediaanual
        else: # Aprovado pelo conselho
            md = Decimal(str((float(nota.mediaanual) + float(nota.recuperacao))/2.))
            nota.mediapospf = round(md, 2)
            nota.mediafinal = nota.mediapospf

            if nota.mediapospf >= 5:
                nota.situacaofinal = 'Aprovado'
            else:
                nota.situacaofinal = 'Reprovado'

        if nota.id == 1665:
            print "Sitf ", nota.situacaofinal
            print "mf ", nota.mediafinal


        # Falta gera uma função que recalcule a situação final do aluno
        nota.save()


        return HttpResponse(1)
    except Exception, e:
        print "Error %s " % e

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



