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

from usuarios import gera_senha
from usuarios import geraUsuario



@login_required()
def addvarios(request):
    context = {}
    cursos = Curso.objects.all()
    context['cursos'] = cursos

    profs = ProfileUser.objects.filter(tipo='Professor')
    context['profs'] = profs

    return render(request, 'addvarios.html', context)



@login_required()
def importarAlunos(request):

    try:

        idturma = request.POST['idturma']
        turma = Turma.objects.get(pk=idturma)

        textAlunos = request.POST['listaalunos']

        listAlunos = textAlunos.splitlines()

        alunosAds = []

        for aluno in listAlunos:
            print 'Aluno: ', aluno

            alunoAd = {}
            mensagem=''
            nome=''
            usuario=''
            senha=''
            email=''

            nome = smart_unicode(aluno)
            nomestr = smart_str(nome)
            print "Ok1 nome ", nome
            email = geraUsuario(nomestr)+"@naosei.com"
            print "Ok2"
            senha = gera_senha(40)[0]
            user = User.objects.create_user(geraUsuario(nomestr), email, senha)
            user.set_password(senha)
            user.is_staff = False
            user.is_superuser = False
            user.save()

            # Profile do Usuario
            profuser = ProfileUser()
            profuser.user = user
            profuser.nome = nome
            profuser.email = email
            profuser.mae = ''
            profuser.rua = ''
            profuser.pai = ''
            profuser.nacionalidade = ''
            profuser.naturalidade = ''
            profuser.orgaoexp = ''
            profuser.tipo = 'Aluno'

            profuser.save()

            matri = Matricula()
            matri.curso = turma.curso
            matri.atual = True
            matri.dataMatricula = datetime.now()
            matri.user = user
            matri.save()

            sitMat = SituacaoMatricula()
            sitMat.data = datetime.now()
            sitMat.situacao = 'Matriculado'
            sitMat.matricula = matri
            sitMat.save()

            discs = Disciplina.objects.filter(curso=turma.curso, periodo=turma.anosemestre)

            for disc in discs:
                nota = Notafalta()
                nota.aluno = profuser
                nota.disciplina = disc
                nota.curso = turma.curso
                nota.turma = turma
                nota.falta1b = 0
                nota.falta2b = 0
                nota.falta3b = 0
                nota.falta4b = 0
                nota.falta5b = 0
                nota.save()

        return HttpResponse(1)
    except:
        return HttpResponse(-1)


def importXlsNotas():




    return ''
