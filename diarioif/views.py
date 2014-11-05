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


@login_required()
def home(request):
    mensagem = ''

    isAuth = request.user.is_authenticated()

    context = {'mensagem': mensagem, 'isAuth':isAuth}

    return render(request, 'base.html', context)





@login_required()
def changeProfile(request):

    context = {'ola': 1}
    user = User.objects.get(pk=request.user.id)
    myprof = ProfileUser.objects.get(user=user)

    if request.POST:
        # If user == Aluno
        myprof.nome = request.POST['nome']
        myprof.mae = request.POST['mae']
        myprof.pai = request.POST['pai']
        date_object = datetime.strptime(request.POST['nascimento'], '%d/%m/%Y')
        myprof.nascimento = date_object
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
        myprof.cep = request.POST['cep']
        myprof.rua = request.POST['rua']
        myprof.numero = request.POST['numero']
        myprof.complemento = request.POST['complemento']
        myprof.observacoes = request.POST['observacoes']
        myprof.tipo = request.POST['tipo']

        myprof.save()

    # Mostra isso quando acessa o profile
    aditionscript = ''
    aditionscript += "$('#nome').jqxInput('val', '"+toUTF8(myprof.nome)+"'); "
    aditionscript += "$('#pai').jqxInput('val', '"+toUTF8(myprof.pai)+"'); "
    aditionscript += "$('#mae').jqxInput('val', '"+toUTF8(	myprof.mae	)+"'); "
    if myprof.nascimento != None:
        data = myprof.nascimento.day+'/'+myprof.month+"/"+myprof.year
        aditionscript += "$('#nascimento').jqxMaskedInput('val', '"+data+"'); "

    aditionscript += "$('#telefone1').jqxMaskedInput('val', '"+toUTF8(	myprof.telefone1	)+"'); "
    aditionscript += "$('#telefone2').jqxMaskedInput('val', '"+toUTF8(	myprof.telefone2	)+"'); "
    aditionscript += "$('#rg').jqxMaskedInput('val', '"+toUTF8(	myprof.rg	)+"'); "
    aditionscript += "$('#orgaoexp').jqxInput('val', '"+toUTF8(	myprof.orgaoexp	)+"'); "
    aditionscript += "$('#cpfcnpj').jqxMaskedInput('val', '"+toUTF8(	myprof.cpfcnpj	)+"'); "
    aditionscript += "$('#email').jqxInput('val', '"+toUTF8(	myprof.email	)+"'); "
    aditionscript += "$('#nacionalidade').jqxInput('val', '"+toUTF8(	myprof.nacionalidade	)+"'); "
    aditionscript += "$('#naturalidade').jqxInput('val', '"+toUTF8(	myprof.naturalidade	)+"'); "
    aditionscript += "$('#estado').jqxInput('val', '"+toUTF8(	myprof.estado	)+"'); "
    aditionscript += "$('#cep').jqxMaskedInput('val', '"+toUTF8(	myprof.cep	)+"'); "
    aditionscript += "$('#rua').jqxInput('val', '"+toUTF8(	myprof.rua	)+"'); "
    aditionscript += "$('#numero').jqxMaskedInput('val', '"+toUTF8(	myprof.numero	)+"'); "
    aditionscript += "$('#complemento').jqxInput('val', '"+toUTF8(	myprof.complemento	)+"'); "
    aditionscript += "$('#tipo').jqxInput('val', '"+myprof.tipo+"'); "

    context['aditionscript'] = aditionscript

    # Tasks to do here
    # --- Mudar a cidade, estado, rua e bairro de acordo com o que está no profile. Caso seja None, deixar Mato Grosso e Barra do Garças
    # --- Desativar alguns campos de acordo com o tipo de usuário

    toUTF8(	myprof.observacoes	)
    toUTF8(	myprof.tipo	)


    return render(request, 'profile.html', context)


@login_required()
def getCities(request, estado):

    #estado=request.GET['estado']
    cidades = []
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
def getBairros(request):

    try:
        bairroslist = []
        estado = request.POST['estado']
        cidade = request.POST['cidade']

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
        mycity = Cidade.objects.get(pk=cidade)
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

        print "Estado: ", estado, " Cidade: ", cidade, " Bairro: ", bairro, ' Rua: ' + rua

        # UfReg = Uf.objects.get(nome=estado)
        print "Uf ok"
        mycity = Cidade.objects.get(pk=cidade)
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


