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
from lancarnotas import defaultencode

@login_required()
def minhasfaltas(request):

    if temAcesso(request):
        return HttpResponse(status=500)
    """
        Aqui irá mostrar todos as faltas de cada disciplina que o aluno está fazendo
    """
    context = {}


    return render(request, 'minhasfaltas.html', context)

@login_required()
def MinhasAtividades(request):

    if temAcesso(request):
        return HttpResponse(status=500)

    """
        Aqui irá mostrar todos as faltas de cada disciplina que o aluno está fazendo
    """
    context = {}
    return render(request, 'minhasatividades.html', context)


@login_required()
def MinhasMatriculas(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    matriculas = []

    idaluno = request.user.id
    user =User.objects.get(pk=idaluno)
    Matriculas = Matricula.objects.filter(user=user)

    for mt in Matriculas:
        matri = {}
        matri['id'] = mt.id
        matri['idcurso'] = mt.curso.id
        matri['nome'] = mt.curso.nome
        matri['anograde'] = mt.curso.anoGrade
        matri['datamat'] = mt.dataMatricula.strftime("%m/%d/%Y")
        matri['atual'] = mt.atual
        matriculas.append(matri)

    return HttpResponse(json.dumps(matriculas), content_type="application/json")


@login_required()
def MinhasTurmas(request):

    if temAcesso(request):
        return HttpResponse(status=500)

    turmas = []
    try:
        idaluno = request.user.id
        user =User.objects.get(pk=idaluno)

        idcurso = request.POST['idcurso']
        curso = Curso.objects.get(pk=idcurso)

        # Pega todos as turmas de um curso
        turmasCurso = Turma.objects.filter(curso=curso)

        for tm in turmasCurso:

            profuser = ProfileUser.objects.get(user=user)
            notasF = Notafalta.objects.filter(turma=tm, aluno=profuser)[:4]
            turma = {}

            if len(notasF) > 0:
                turma['id'] = tm.id
                turma['letra'] = tm.nome
                turma['ano'] = tm.anoturma
                turmas.append(turma)

        return HttpResponse(json.dumps(turmas), content_type="application/json")
    except:
        print 'err'
    return HttpResponse(json.dumps(turmas), content_type="application/json")


@login_required()
def MinhasDisciplinas(request):
    discs = []
    if temAcesso(request):
        return HttpResponse(status=500)

    try:
        idaluno = request.user.id
        user =User.objects.get(pk=idaluno)
        myprof = ProfileUser.objects.get(user=user)

        idturma = request.POST['idturma']

        t = Turma.objects.get(pk=idturma)

        atribs = AtribAula.objects.filter(turma=t)

        for atrib in atribs:
            disciplina = {}
            disciplina['id'] = atrib.id
            disciplina['nome'] = atrib.disciplina.nome
            disciplina['professor'] = atrib.professor.nome
            disciplina['periodo'] = atrib.disciplina.periodo

            discs.append(disciplina)

    except Exception, e:
        print 'Hello exception %s !!!' % e

    return HttpResponse(json.dumps(discs), content_type="application/json")


@login_required()
def MinhasFaltas(request):
    faltas = []
    if temAcesso(request):
        return HttpResponse(status=500)

    try:
        idaluno = request.user.id
        user =User.objects.get(pk=idaluno)
        myprof = ProfileUser.objects.get(user=user)

        idAtrib = request.POST['discId']


        atrib = AtribAula.objects.get(pk=int(idAtrib))

        dias = Dia.objects.filter(atrib=atrib).order_by('-data')

        for d in dias:
            falta = {}
            presS = Presenca.objects.filter(dia=d, presente=False, aluno=myprof)
            cont = Conteudo.objects.get(dia=d)
            falta['quant'] = 0
            falta['dia'] = d.data.strftime("%d/%m/%Y")
            falta['conteudo'] = cont.conteudo

            ativ = Atividade.objects.filter(turma=atrib.turma, disciplina=atrib.disciplina, dataInicio=d.data)
            falta['ativ'] = ''
            cont =0
            for at in ativ:
                falta['ativ'] += str(cont) + '-'+ at.descricao + '-' + at.tipo +' '
                cont += 1

            for pres in presS:
                falta['quant'] += 1


            if len(presS) != 0:
                faltas.append(falta)

    except Exception, e:
        print 'Hello exception %s !!!' % e

    return HttpResponse(json.dumps(faltas), content_type="application/json")

@login_required()
def MinhasAtividadesl(request):
    atividades = []
    if temAcesso(request):
        return HttpResponse(status=500)

    try:
        idaluno = request.user.id
        user =User.objects.get(pk=idaluno)
        myprof = ProfileUser.objects.get(user=user)

        idAtrib = request.POST['discId']
        atrib = AtribAula.objects.get(pk=int(idAtrib))

        ativs = Atividade.objects.filter(turma=atrib.turma, disciplina=atrib.disciplina).order_by('-dataInicio')

        for ativ in ativs:
            atv = {}
            atv['descricao'] = ativ.descricao
            atv['dataInicio'] = ativ.dataInicio.strftime("%d/%m/%Y")
            atv['dataFim'] = ativ.dataFim.strftime("%d/%m/%Y")

            nota = NotaAtividade.objects.get(atividade=ativ, aluno=myprof)
            atv['nota0'] = '' if type(nota.nota0) == type(None) else nota.nota0

            if ativ.tipo == 'Atitudinal':
                atv['nota1'] = '' if type(nota.nota1) == type(None) else nota.nota1
                atv['nota2'] = '' if type(nota.nota2) == type(None) else nota.nota2
                atv['nota3'] = '' if type(nota.nota3) == type(None) else nota.nota3
            else:
                atv['nota2'] = ''
                atv['nota3'] = ''


            atv['bimestre'] = ativ.bimestre
            atv['tipo'] = ativ.tipo

            atividades.append(atv)


    except Exception, e:
        print 'Hello exception %s !!!' % e

    return HttpResponse(json.dumps(atividades, default=defaultencode), content_type="application/json")



