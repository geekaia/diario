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


@login_required()
def home(request):
    mensagem = ''

    isAuth = request.user.is_authenticated()

    context = {'mensagem': mensagem, 'isAuth':isAuth}

    return render(request, 'base.html', context)





@login_required()
def changeProfile(request, id=None):

    context = {'ola': 1}
    user = User.objects.get(pk=request.user.id)

    print "ola mundo"

    if id != None:
        user = User.objects.get(pk=id)
        myprof = ProfileUser.objects.get(user=user)
        context['myprof'] = myprof
    try:

        if request.POST:
            # If user == Aluno
            myprof = ProfileUser.objects.get(user=user)
            myprof.nome = request.POST['nome']
            myprof.mae = request.POST['mae']
            myprof.pai = request.POST['pai']

            try:
                # date_object = datetime.strptime(request.POST['nascimento'], '%d/%m/%Y')
                # myprof.nascimento = date_object
                date_object = datetime.strptime(request.POST['nascimento'], '%d/%m/%Y')

                myprof.nascimento = date_object
            except:
                print 'err'

            myprof.telefone1 = request.POST['telefone1']
            myprof.telefone2 = request.POST['telefone2']
            myprof.rg = request.POST['rg']
            myprof.orgaoexp = request.POST['orgaoexp']
            myprof.cpfcnpj = request.POST['cpfcnpj']
            myprof.email = request.POST['email']
            myprof.nacionalidade = request.POST['nacionalidade']
            myprof.naturalidade = request.POST['naturalidade']
            myprof.estado = request.POST['estado']
            myprof.cidade = request.POST['cidade']
            myprof.bairro = request.POST['bairro']
            myprof.cep = request.POST['cep']
            myprof.rua = request.POST['rua']

            # Caso não haja o Bairro selecionado
            try:

                UfReg = Uf.objects.get(nome=myprof.estado)
                mycity = Cidade.objects.get(uf=UfReg, nome=myprof.cidade)
                bairro = Bairro.objects.filter(cidade=mycity, nome=myprof.bairro)

                if len(bairro) == 0:
                    bairroCad = Bairro()
                    bairroCad.nome = myprof.bairro
                    bairroCad.cidade = mycity
                    bairroCad.save()

            except:
                print 'Erro ao Cadastrar o Bairro'


            # Caso não haja a rua selecionada
            try:
                UfReg = Uf.objects.get(nome=myprof.estado)
                mycity = Cidade.objects.get(uf=UfReg, nome=myprof.cidade)
                bairro = Bairro.objects.get(cidade=mycity, nome=myprof.bairro)

                ruas = Rua.objects.filter(bairro=bairro, nome=myprof.rua)

                if len(ruas) == 0:
                    rua = Rua()
                    rua.nome = myprof.rua
                    rua.bairro = bairro
                    rua.tipo = 1 # Não irei utilizar
                    rua.cep = myprof.cep
                    rua.save()
            except:
                print 'Erro a rua '

            myprof.numero = request.POST['numero']
            myprof.complemento = request.POST['complemento']
            myprof.observacoes = request.POST['observacoes']
            myprof.tipo = request.POST['tipo']

            myprof.save()

        context['prof'] = myprof

    except Exception, e:
        print 'Erro ' + str(e)


    return render(request, 'profile.html', context)


@login_required()
def getCities(request):


    cidades = []
    if request.POST:
        estado=request.POST['estado']

        try:
            print "Estado: ", estado

            UfReg = Uf.objects.get(nome=estado)

            print "Estou aqui", UfReg.nome, " sigla: ", UfReg.sigla

            cities = Cidade.objects.filter(uf=UfReg)

            print "Cidades: ", len(cities)

            for i in cities:
                cidade = {}
                cidade['id'] = i.id
                cidade['nome'] = i.nome
                cidades.append(cidade)
                # cidades[i.id] = i.nome
        except:
            print 'Erro ao pegar cidades'


    return HttpResponse(json.dumps(cidades), content_type="application/json")


@login_required()
def cursocad(request, id=None):

    context ={}


    if request.POST:
        try:
            curso = Curso.objects.get(pk=int(request.POST['id']))
            print 'Peguei o id'
        except:
            curso = Curso()

        curso.nome = request.POST['nome']
        curso.anoGrade = request.POST['anoGrade']
        curso.periodo = request.POST['periodo']
        curso.quantPeriodo = request.POST['quantPeriodo']
        curso.habilitacao = request.POST['habilitacao']
        curso.resolucaoreconhecimento = request.POST['resolucaoreconhecimento']

        date_manip = datetime.strptime(request.POST['dataPublicacao'], '%d/%m/%Y')
        curso.dataPublicacao = date_manip
        curso.formaingresso = request.POST['formaingresso']
        curso.avaliacaopor = request.POST['avaliacaopor']

        curso.save()


    if id != None:
        curso = Curso.objects.get(pk=id)
        context['curso'] = curso


    return render(request, 'cursoCad.html', context)


def toUTF8(val):
    """ Converte algumas variaveis para UTF-8 """

    try:
        if type(val) == type(5) or type(val) == type(44444444444444444444):
            # print "int", val
            return val

        if type(val) == type(5.5):
            # print "float", val
            return val

        if isinstance(val, unicode):
            # print "unicode", val
            return val.encode('utf8')

        if type(val) == type(None):
            # print "None", val
            return ""

        if type(val) == type([]): # List
            cont=0
            STR ='('
            for i in val:
                cont+=1
                if cont==len(val):
                    STR+=i+')'
                else:
                    STR+=i+', '
            return STR


        # print "Outro: ", type(val), val
        return unicode(val, 'utf-8')+""

    except:

        return ""



@login_required()
def getUsers(request):

    users = []


    profs = ProfileUser.objects.all()

    for prof in profs:
        user = {}
        user['id'] = prof.id
        user['nome'] =  prof.nome
        user['username'] =  prof.user.username
        users.append(user)



    return HttpResponse(json.dumps(users), content_type="application/json")


def hasAcess(request):

    prof =  ProfileUser.objects.get(user=request.user)

    return ''



@login_required()
def geCourses(request):
    cursos = []
    Cursos = Curso.objects.all()


    print "Full Path: ", request.get_full_path()

    for c in Cursos:
        curso = {}
        curso['id'] = c.id
        curso['nome'] = c.nome
        curso['anoGrade'] = c.anoGrade

        cursos.append(curso)

    return HttpResponse(json.dumps(cursos), content_type="application/json")

@login_required()
def listCourses(request):

    context = {}


    return render(request, 'cursoList.html', context)





def listUsuarios(request):

    context = {}

    # Lista de cursos
    cursos = Curso.objects.all()
    context['cursos'] = cursos



    return render(request, 'listagemAlunos.html', context)



@login_required()
def getBairros(request):

    try:
        bairroslist = []
        estado = request.POST['estado']
        cidade = request.POST['cidade']

        if len(cidade)==0:
            return HttpResponse(json.dumps(bairroslist), content_type="application/json")

        print "Estado: ", estado, " Cidade: ", cidade

        UfReg = Uf.objects.get(nome=estado)
        mycity = Cidade.objects.get(uf=UfReg, nome=cidade)
        bairros = Bairro.objects.filter(cidade=mycity)

        print "Tamanho: ", len(bairros)

        for i in bairros:
            bairro = {}
            bairro['id'] = i.id
            bairro['nome'] = i.nome
            bairroslist.append(bairro)
            print "Nome: ", i.nome
            # cidades[i.id] = i.nome
    except:
        print 'Ola mundo!!'

    return HttpResponse(json.dumps(bairroslist), content_type="application/json")

@login_required()
def getRuas(request):
        #estado=request.GET['estado']
    ruaslist = []
    try:
        estado = request.POST['estado']
        cidade = request.POST['cidade']
        bairro = request.POST['bairro']

        print "Estado: ", estado, " Cidade: ", cidade, " Bairro: ", bairro

        # UfReg = Uf.objects.get(nome=estado)
        print "Uf ok"
        UfReg = Uf.objects.get(nome=estado)
        mycity = Cidade.objects.get(uf=UfReg, nome=cidade)
        print "Uf city"
        mybairro = Bairro.objects.get(cidade=mycity, nome=bairro)
        print "Uf bairro"
        ruas = Rua.objects.filter(bairro=mybairro)
        print "Uf ruas"

        for i in ruas:
            rua = {}
            rua['id'] = i.id
            rua['nome'] = i.nome
            rua['cep'] = i.cep
            ruaslist.append(rua)
    except:
        print 'Erro get ruas'

    return HttpResponse(json.dumps(ruaslist), content_type="application/json")


@login_required()
def getCep(request):
        #estado=request.GET['estado']
    ruaslist = {}
    try:
        estado = request.POST['estado']
        cidade = request.POST['cidade']
        bairro = request.POST['bairro']
        rua = request.POST['rua']

        # UfReg = Uf.objects.get(nome=estado)
        print "Uf ok"
        UfReg = Uf.objects.get(nome=estado)
        mycity = Cidade.objects.get(uf=UfReg, nome=cidade)
        print "Uf city"
        mybairro = Bairro.objects.get(cidade=mycity, nome=bairro)
        print "Uf bairro"
        ruas = Rua.objects.get(bairro=mybairro, nome=rua)
        ruaslist['cep'] = ruas.cep

    except:
        print 'Erro get ruas'

    return HttpResponse(json.dumps(ruaslist), content_type="application/json")





@login_required()
def sair(request):
    logout(request)

    return redirect('/')

def cadastrarUser(request):

    mensagem=''
    nome=''
    usuario=''
    senha=''
    email=''

    context = {}


    if request.POST:
        nome = request.POST['nome']
        usuario = request.POST['usuario']
        senha = request.POST['senha']
        cfsenha = request.POST['cfsenha']
        email = request.POST['email']

        # Vou validar pelo javascript
        if cfsenha != senha or len(senha) < 6:

            context['mensagem'] = 'As senhas não conferem!!!'

            aditionscript = ''
            aditionscript += "$('#senha').jqxPasswordInput('val', '"+senha+"'); "
            aditionscript += "$('#cfsenha').jqxPasswordInput('val', ''); "
            aditionscript += "$('#nome').jqxInput('val', '"+nome+"'); "
            aditionscript += "$('#email').jqxInput('val', '"+email+"'); "
            aditionscript += "$('#usuario').jqxInput('val', '"+usuario+"'); "
            context['aditionscript'] = aditionscript

            return render(request, 'cadastraUsuario.html', context)

        else:
            user = User.objects.create_user(usuario, email, senha)
            user.set_password(senha)
            user.is_staff = False
            user.is_superuser = False
            user.save()

            # Profile do Usuario
            profuser = ProfileUser()
            profuser.user = user
            profuser.nome = nome
            profuser.email = email
            profuser.tipo = 'Aluno'
            profuser.save()

            # Authenticate user
            loginUser(request)

            # Redireciona para o profile
            return redirect('/profile')


    context['mensagem'] = mensagem
    context['aditionscript'] = ''


    return render(request, 'cadastraUsuario.html', context)

def gera_senha(tamanho):
    caracters = '0123456789abcdefghijlmnopqrstuwvxzABCEFGHIJKLMNOPQRSTUVXZ'
    senha = ''
    for char in xrange(tamanho):
        senha += choice(caracters)
    mypass=[]
    mypass.append(senha)

    return mypass





def recuperarSenha(request):
    context =  {}

    try:
        if request.POST:
            context['mensagem'] = 'Verifique o seu e-mail!!'

            loginEmail = request.POST['useremail']
            nascimento = request.POST['nascimento']
            rg = request.POST['rg']

            if len(loginEmail.split('@'))>1:
                # Email
                prof = ProfileUser.objects.get(email=loginEmail)
                user = prof.user

                nascMonth = prof.nascimento.month
                nascDay = prof.nascimento.day
                nascYear = prof.nascimento.year

                nascRDay = int(nascimento.split('/')[0])
                nascRMonth = int(nascimento.split('/')[1])
                nascRYear = int(nascimento.split('/')[2])

                if nascMonth==nascRMonth and nascRDay==nascDay and nascYear==nascRYear and rg==prof.rg:
                    newsenha = gera_senha(25)
                    user.set_password(newsenha)
                    user.save()

                    send_mail('Nova Senha sistema', 'Senha: ' + newsenha, settings.EMAIL_HOST_USER,
                              [ prof.email ], fail_silently=False )

                    context['mensagem'] = 'Por favor, verifique seu e-mail!'
                else:
                    context['mensagem'] = 'RG ou Data de nascimento incorretos!'

    except:
        context['mensagem'] = 'Usuario/Email não encontrado em nossa Base de dados!'

    return render(request, 'recuperarSenha.html', context)


def loginUser(request):

    state=''

    if request.POST:
        username = request.POST['usuario']
        senha = request.POST['senha']

        user = authenticate(username=username, password=senha)

        if user is not None:
            if user.is_active:
                login(request, user)

                return redirect('/')
            else:
                state = "Seu usuario nao esta ativo"
        else:
            state = "Voce digitou o usuario e/ou senha incorretamente."

    context = {'mensagem': state}

    return render(request, 'login.html', context)


