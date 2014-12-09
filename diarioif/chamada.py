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
from usuarios import temAcesso

@login_required()
def chamada(request):
    if temAcesso(request):
        return HttpResponse(status=500)
    context = {}

    # Todos os cursos em que o professor leciona

    return render(request, 'chamada.html', context)


@login_required()
def chamadaDisc(request):
    if temAcesso(request):
        return HttpResponse(status=500)
    ano = request.POST['ano']
    idprof = request.POST['idprof']
    disciplinas = []

    # Todas as atribuições de aulas deste professor
    atribs = AtribAula.objects.filter(professor=idprof)

    for atrib in atribs:
        if atrib.periodoInicio.year == int(ano):
            disc = {}
            disc['id'] = atrib.id
            disc['nome'] = atrib.disciplina.nome
            disc['turma'] = atrib.turma.nome
            disc['curso'] = atrib.turma.curso.nome

            disciplinas.append(disc)

    return HttpResponse(json.dumps(disciplinas), content_type="application/json")


@login_required()
def addDia(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    try:
        diaDt = request.POST['dia']
        dia_ob = datetime.strptime(diaDt, '%d/%m/%Y')
        dia_object = dia_ob.date()

        # -2 - Código do domingo
        if dia_object.weekday() == 6:
            return HttpResponse(-2)

        # -3 - É sábado letivo?
        elif dia_object.weekday() == 5:
            try:
                DiaExcept.objects.get(dataInicio=dia_object, tipo='SB')
            except Exception, e:
                return HttpResponse(-3)

        else:
            # É feriado?
            try:
                dias = DiaExcept.objects.filter(dataInicio__lte=dia_object, dataFim__gte=dia_object)
                diasCant = ['FD', 'FDS', 'F', 'PF', 'RC', 'SP']

                for d in dias:
                    if d.tipo in diasCant and dia_object >= d.dataInicio and dia_object <= d.dataFim:
                        return HttpResponse(-4)

            except Exception, e:
                print "Não é um dia letivo " % e


            # Está entre o periodo letivo ?
            try:
                idsOk = False
                ano = request.POST['ano']
                print "Ano: ", ano
                bims = Bimestre.objects.filter(ano=str(ano), bimestreSemestre='semestre')
                print "ok111"
                for bi in bims:
                    if bi.dataInicio <= dia_object and bi.dataFim >= dia_object:
                        print "ok t"
                        idsOk = True
                        break

                print "ok t2"
                if idsOk == False:
                    return HttpResponse(-5)
                print "ok t3"

            except Exception, e:
                print "Não é um dia letivo " % e


        idatrib = request.POST['id']
        print "ok1"
        atrib = AtribAula.objects.get(pk=idatrib)

        turma = atrib.turma
        quantidade = int(request.POST['quantidade'])
        print "ok1"

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

        print "ok2"
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

        print "ok3"
        return HttpResponse(1)

    except Exception, e:
        print "Erro: %s " % e

        return HttpResponse(-1)

@login_required()
def getActualBimestre(request):
    if temAcesso(request):
        return HttpResponse(status=500)
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
    if temAcesso(request):
        return HttpResponse(status=500)
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
    if temAcesso(request):
        return HttpResponse(status=500)
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
    if temAcesso(request):
        return HttpResponse(status=500)
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
    if temAcesso(request):
        return HttpResponse(status=500)
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
    if temAcesso(request):
        return HttpResponse(status=500)
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
    if temAcesso(request):
        return HttpResponse(status=500)

    try:

        iddia = request.POST['id']
        dia = Dia.objects.get(pk=iddia)
        dia.delete()

        return HttpResponse(1)
    except:
        return HttpResponse(-1)

