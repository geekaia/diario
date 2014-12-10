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
from django.forms import *
from xlrd import open_workbook,cellname
from usuarios import temAcesso, remover_acentos
from utils import defaultencode


@login_required()
def addvarios(request):
    if temAcesso(request):
        return HttpResponse(status=500)
    context = {}
    cursos = Curso.objects.all()
    context['cursos'] = cursos

    profs = ProfileUser.objects.filter(tipo='Professor')
    context['profs'] = profs

    return render(request, 'addvarios.html', context)



@login_required()
def importarAlunos(request):
    if temAcesso(request):
        return HttpResponse(status=500)
    try:

        idturma = request.POST['idturma']
        turma = Turma.objects.get(pk=idturma)

        textAlunos = request.POST['listaalunos']

        listAlunos = textAlunos.splitlines()

        alunosAds = []


        allprofs = ProfileUser.objects.all()



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



            # Se o nome tiver poucos caracteres será ignorado
            if len(nome) < 6:
                continue

            cadNew = True
            proffind = None


            # Procura para ver se o usuário já está cadastrado no Banco de dados
            hasProf = ProfileUser.objects.filter(nome__icontains=nome)

            if len(hasProf) == 0:
                for i in allprofs:
                    nomeDatabase = remover_acentos(i.nome)
                    nomeTxt = remover_acentos(nome)

                    if nomeDatabase.lower() in nomeTxt.lower() or nomeTxt.lower() in nomeDatabase.lower():
                        cadNew = False
                        proffind = i
                        break
            else:
                cadNew = False
                proffind = hasProf[0]


            if cadNew == True:
                email = geraUsuario(nomestr)+"@naosei.com"
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
            else:
                profuser = proffind


            # Procura Para ver se o aluno ja está matriculado neste curso
            nMatri = False
            try:
                matri = Matricula.objects.get(curso=turma.curso, user=profuser.user)
                matri.atual = True
                matri.save()
            except:
                matri = Matricula()
                matri.curso = turma.curso
                matri.atual = True
                matri.dataMatricula = datetime.now()
                matri.user = profuser.user
                matri.save()

            # Isto é necessário para todas as vezes em que criamos um novo usuário
            sitMat = SituacaoMatricula()
            sitMat.data = datetime.now()
            sitMat.situacao = 'Matriculado'
            sitMat.matricula = matri
            sitMat.save()

            discs = Disciplina.objects.filter(curso=turma.curso, periodo=turma.anosemestre)

            for disc in discs:
                # Verifica se já está cadastrado nesta disciplina
                ntfs = Notafalta.objects.filter(aluno=profuser, disciplina=disc, turma=turma)

                if len(ntfs) >= 1:
                    # O aluno já está matriculado nesta disciplina
                    continue

                nota = Notafalta()
                nota.aluno = profuser
                nota.disciplina = disc
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


class FileUploadedForm(forms.Form):
    uploaded_file = forms.FileField(required=False)

def importXlsNotas(request):
    listAls = []
    listResp = []

    if temAcesso(request):
        return HttpResponse(status=500)

    try:
        idattrib = request.POST['idatrib']
        atrib = AtribAula.objects.get(pk=int(idattrib))

        data = Notafalta.objects.values_list('aluno').filter(turma=atrib.turma).distinct()
        # Carrega a listagem de todos os alunos do cursoi
        for i in data:
            aluno = {}
            prof = ProfileUser.objects.get(pk=int(i[0]))

            # Aqui gera uma excessão caso o aluno não faça mais esta disciplina
            try:
                ntf = Notafalta.objects.get(aluno=prof, disciplina=atrib.disciplina, turma=atrib.turma)
                aluno['id'] = ntf.id
                aluno['nome'] = prof.nome
                listAls.append(aluno)
            except:
                print "Err"

        # Não poderemos ter 2 alunos que match thenselves
        if request.method == 'POST':
            form = FileUploadedForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES.get('uploaded_file')

                f = file.read()
                book = open_workbook(file_contents=f)
                sheet = book.sheet_by_name('Resultado')

                #print 'Nome', '\t\t\t\tNota 1B', 'Nota 2B', 'Nota 3B', 'Nota 4B', 'PF'
                for row_index in range(12, 60):
                    try:
                        # Percorre toda a listagem de alunos para verificar se há pessoas que
                        cont = 0

                        # Renta converter a primeira coluna -- caso ocorra uma excessão não tem aluno na linha
                        row = int(sheet.cell(row_index, 0).value)

                        if len(sheet.cell(row_index, 2).value) < 3:
                          continue

                        sheet1b = book.sheet_by_name('Nota 1B') # 45 AT
                        sheet2b = book.sheet_by_name('Nota 2B')
                        sheet3b = book.sheet_by_name('Nota 3B')
                        sheet4b = book.sheet_by_name('Nota 4B')

                        ft1b = int(sheet1b.cell(row_index, 45).value)
                        ft2b = int(sheet2b.cell(row_index, 45).value)
                        ft3b = int(sheet3b.cell(row_index, 45).value)
                        ft4b = int(sheet4b.cell(row_index, 45).value)

                        for al in listAls:
                            nomePlan = remover_acentos(sheet.cell(row_index, 2).value)
                            nomeList = remover_acentos(al['nome'])

                            if nomePlan in nomeList or nomeList in nomePlan and (len(nomeList)>3 and len(nomePlan)>3):
                                al['nota1b'] = sheet.cell(row_index, 21).value
                                al['nota2b'] = sheet.cell(row_index, 24).value
                                al['nota3b'] = sheet.cell(row_index, 27).value
                                al['nota4b'] = sheet.cell(row_index, 30).value
                                al['falta1b'] = ft1b
                                al['falta2b'] = ft2b
                                al['falta3b'] = ft3b
                                al['falta4b'] = ft4b
                                al['PF'] = sheet.cell(row_index, 39).value

                                listResp.append(al)
                                listAls[cont] = al

                            cont += 1
                    except:
                        print 'Nao tem aluno nesta linha'

            # Dados necessários
             # { name: 'nome'},
             #            { name: 'nota1b',  type: 'number'},
             #            { name: 'falta1b',  type: 'number'},
             #            { name: 'nota2b',  type: 'number'},
             #            { name: 'falta2b',  type: 'number'},
             #            { name: 'nota3b',  type: 'number'},
             #            { name: 'falta3b',  type: 'number'},
             #            { name: 'nota4b',  type: 'number'},
             #            { name: 'falta4b',  type: 'number'},
             #            { name: 'mediafinal',  type: 'number'},
             #            { name: 'recuperacao',  type: 'number'},
             #            { name: 'situacaofinal',  type: 'number'},
             #            { name: 'mediaanual',  type: 'number'},
             #            { name: 'mediapospf',  type: 'number'},
    except Exception, e:
        print 'Exception %s' % e

    return HttpResponse(json.dumps(listResp, default=defaultencode), content_type="application/json")

def fileupload(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    context = {}
    context['form'] = FileUploadedForm

    return render(request, 'fileupload.html', context)

