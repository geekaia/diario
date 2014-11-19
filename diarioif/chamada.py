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
def chamada(request):

    context = {}

    # Todos os cursos em que o professor leciona

    return render(request, 'chamada.html', context)


@login_required()
def chamadaDisc(request):

    ano = request.POST['ano']
    idprof = request.POST['idprof']
    disciplinas = []

    # Todas as atribuições de aulas deste professor
    atribs = AtribAula.objects.filter(professor=idprof)

    for atrib in atribs:
        if atrib.periodoInicio.year == int(ano):
            disc = {}
            disc['id'] =atrib.id
            disc['nome'] =atrib.disciplina.nome
            disc['turma'] =atrib.turma.nome
            disc['curso'] =atrib.turma.curso.nome


            disciplinas.append(disc)

    return HttpResponse(json.dumps(disciplinas), content_type="application/json")


@login_required()
def addDia(request):
    try:

        diaDt = request.POST['dia']
        dia_object = datetime.strptime(diaDt, '%d/%m/%Y')


        idatrib = request.POST['id']
        atrib = AtribAula.objects.get(pk=idatrib)

        turma = atrib.turma
        quantidade = int(request.POST['quantidade'])

        # Procura para ver se não tem nenhum desses dias cadastrados
        diafind = Dia.objects.filter(data=dia_object, atrib=atrib)
        if len(diafind) == 0:
            dia = Dia()
            dia.data = dia_object
            dia.atrib = atrib
            dia.save()

            # Adiciona o conteudo
            cont = Conteudo()
            cont.dia = dia
            cont.conteudo = ''
            cont.save()
        else:
            dia = diafind[0]

        # Agora eu tenho que adicionar uma linha para cada aluno e aula
        # Procura por todos os alunos desta turma e insere uma linha
        alunosTurma = Notafalta.objects.values_list('aluno').filter(turma=turma).distinct()
        for aluno in alunosTurma:
            for i in xrange(0, quantidade):
                # print  "Id aluno: ", aluno[0]
                profileAl = ProfileUser.objects.get(pk=int(aluno[0]))
                presenca = Presenca()
                presenca.aluno = profileAl
                presenca.dia = dia
                presenca.presente = True
                presenca.save()

        return HttpResponse(1)

    except Exception, e:
        print "Erro: %s " % e

        return HttpResponse(-1)

@login_required()
def getActualBimestre(request):

    try:
        idatrib = request.POST['id']
        atrib = AtribAula.objects.get(pk=idatrib)
        ano = atrib.turma.anoturma

        data = datetime.now()
        bim = Bimestre.objects.get(ano=ano, dataInicio__lte=data.date(), bimestreSemestre=atrib.turma.curso.avaliacaopor.lower(), dataFim__gte=data.date())

        return HttpResponse(bim.numero)
    except:
        return HttpResponse(-1)

@login_required()
def getDiasBimestre(request):
    datas = []

    try:
        idatrib = request.POST['id']
        atrib = AtribAula.objects.get(pk=idatrib)

        # Get todos os dias desta disciplian
        dias = Dia.objects.filter(atrib=atrib).order_by('-data')

        for dia in dias:
            d = {}
            d['id'] = dia.id
            d['id2'] = dia.id
            d['data'] = dia.data.strftime("%d/%m/%Y")
            first = Presenca.objects.filter(dia=dia)[:1][0]
            d['quant'] = len(Presenca.objects.filter(dia=dia, aluno=first.aluno))

            datas.append(d)
    except:
        print 'Deu erro'

    return HttpResponse(json.dumps(datas), content_type="application/json")

@login_required()
def getContent(request):
    content = []
    try:
        iddia = request.POST['id']
        dia = Dia.objects.get(pk=iddia)
        cont = Conteudo.objects.get(dia=dia)

        ct = {}
        ct['content'] = cont.conteudo
        content.append(ct)
    except Exception, e:
        print "Err: %s " % e


    return HttpResponse(json.dumps(content), content_type="application/json")


@login_required()
def saveContent(request):

    try:
        id=request.POST['id']

        dia = Dia.objects.get(pk=id)
        cont = Conteudo.objects.get(dia=dia)
        cont.conteudo = request.POST['content']
        cont.save()

        return HttpResponse(1)

    except Exception, e:
        print "Err: %s " % e

    return HttpResponse(-1)

@login_required()
def getChamadaList(request):
    lista = []

    try:
        id=request.POST['id']
        dia = Dia.objects.get(pk=id)

        first = Presenca.objects.filter(dia=dia)[:1][0]
        quant = len(Presenca.objects.filter(dia=dia, aluno=first.aluno))

        # Pega todos os alunos da turma

        alunos = Notafalta.objects.values_list('aluno').filter(turma=dia.atrib.turma).distinct()

        for i in alunos:

            aluno = {}
            prof = ProfileUser.objects.get(pk=int(i[0]))
            aluno['id'] = int(i[0])
            aluno['nome'] = prof.nome

            # Pega todas as presenças aluno
            presenca = Presenca.objects.filter(dia=dia, aluno=prof)

            for i in range(0, quant):
                aluno[str(i)] = presenca[i].presente
                aluno[str(i)+'id'] = presenca[i].id

            lista.append(aluno)
    except:
        print 'err'


    return HttpResponse(json.dumps(lista), content_type="application/json")

@login_required()
def salvarChamada(request):
    try:
        # quant aulas
        quant = request.POST['quant']

        for i in range(0, int(quant)):
            id = request.POST[str(i)+'id']
            value = request.POST[str(i)]
            presenca = Presenca.objects.get(pk=id)
            presenca.presente = True if value=='true' else False
            presenca.save()

        return HttpResponse(1)
    except:
        return HttpResponse(-1)

@login_required()
def removerDia(request):
    try:

        iddia = request.POST['id']
        dia = Dia.objects.get(pk=iddia)
        dia.delete()

        return HttpResponse(1)
    except:
        return HttpResponse(-1)




