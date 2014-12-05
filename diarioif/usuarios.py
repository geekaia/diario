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


def temAcesso(request):
    page = request.path

    id = request.user.id
    user = User.objects.get(pk=id)
    prof = ProfileUser.objects.get(user=user)

    # Usuario
    alunoslist = ['/viewnotas', '/viewpresenca', '/viewtarefas']
    profslist = ['/calendarioano']

    if prof.tipo == 'Aluno':
        if page in alunoslist:
            return False
        else:
            return False

    elif prof.tipo == 'Administrador': # Pode fazer tudo no sistema
        return False
    elif prof.tipo == 'Secretaria':
        return False
    elif prof.tipo == 'Professor':
        if page in profslist:
            return False
        else:
            return True




@login_required()
def changeProfile(request, id=None):
    if temAcesso(request):
        return HttpResponse(status=500)

    showcontrolers = False
    # Vou ter que adicionar alguma coisa
    # para controlar os níveis
    context = {}
    user = User.objects.get(pk=id)
    myprof = ProfileUser.objects.get(user=user)

    # Aqui os alunos e professores só podem ver o próprio profile
    profreq = ProfileUser.objects.get(user=request.user)
    if (profreq.tipo == 'Aluno' or profreq.tipo == 'Professor') and request.user.id != user.id:
        print "Redirecionando ..."
        return redirect('/')

    if profreq.tipo == 'Administrador' or profreq.tipo == 'Secretaria':
        showcontrolers = True


    try:

        if request.POST:
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


            # No caso da secretaria ou de alguém que esteja editando
            # Aqui o usuário que requer tem que ser to tipo secretaria
            if id != None:
                return redirect("/listUsuarios")



    except Exception, e:
        print 'Erro ' + str(e)


    context['actionform'] = '/profile/'+str(myprof.user.id)
    context['prof'] = myprof
    context['showcontrolers'] = showcontrolers

    cursos = Curso.objects.all()
    context['cursos'] = cursos


    context['nascimento'] = datetime.now().strftime("%m/%d/%Y") if type(myprof.nascimento)==type(None) else myprof.nascimento.strftime("%m/%d/%Y")



    return render(request, 'profile.html', context)



def cadastrarUser(request):
    if temAcesso(request):
        return HttpResponse(status=500)

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
            profuser.mae = ''
            profuser.rua = ''
            profuser.pai = ''
            profuser.nacionalidade = ''
            profuser.naturalidade = ''
            profuser.orgaoexp = ''
            profuser.tipo = 'Aluno'


            profuser.save()

            # Authenticate user
            loginUser(request)

            # Redireciona para o profile
            return redirect('/profile/'+profuser.id)


    context['mensagem'] = mensagem
    context['aditionscript'] = ''


    return render(request, 'cadastraUsuario.html', context)


@login_required()
def matriculasAluno(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    matriculas = []

    idaluno = request.POST['id']
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
def matricularAluno(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    try:
        idaluno = request.POST['id']
        idcurso = request.POST['idcurso']
        data = request.POST['dataMatricula']
        date_object = datetime.strptime(data, '%d/%m/%Y')
        curso = Curso.objects.get(pk=idcurso)
        user = User.objects.get(pk=idaluno)

        try:
            idmat = request.POST['idmat'] # Edita uma matrícula
            mat = Matricula.objects.get(pk=idmat)


            print 'Update matricula'
        except:
            mat = Matricula()

            print 'New matricula'

        atual = request.POST['atual']

        dic = {}
        dic['false'] = False
        dic['true'] = True

        mat.atual = dic[atual]
        mat.user = user
        mat.curso = curso
        mat.dataMatricula = date_object
        mat.save()

        print "Mat.atual: ", mat.atual, 'type ', type(mat.atual)

        if mat.atual == True:
            print "Mudando o atual"
            # Procura por todas as matrículas do usuário e seta como atual False
            mats = Matricula.objects.filter(user=mat.user)

            for mt in mats:
                # Todos menos o que eu acabei de salvar
                if mat.id != mt.id:
                    mt.atual = False
                    mt.save()

        return HttpResponse(1)
    except:
        return HttpResponse(-1)
    return ''



@login_required()
def cadUsuario(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    mensagem=''
    nome=''
    usuario=''
    senha=''
    email=''

    if request.POST:
        nome = smart_unicode(request.POST['nome'])
        nomestr = smart_str(nome)
        print "Ok1 nome ", nome
        email = geraUsuario(nomestr)+"@naosei.com" # opcional
        print "Ok2"
        senha = gera_senha(40)[0]
        print "Ok3"

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

        # Redireciona para o profile
        return HttpResponse(user.id)


def geraUsuario(nomecompleto):
    nome = remover_acentos(nomecompleto.lower()).split(' ')
    username = nome[0]+'.'+nome[len(nome)-1]


    for i in range(0, 100):
        # primeira tentativa
        usrs = User.objects.filter(username=username)

        if len(usrs) == 0:
            return username
        elif len(usrs) >= 1:
            username += '.'+str(date.today().year)
            new = User.objects.filter(username=username)

            if len(new) == 0:
                return username
            else:
                username += str(i) # quase impossível de acontecer !!!!
                new = User.objects.filter(username=username)

                if len(new) == 0:
                    return username




def remover_acentos(txt, codif='utf-8'):
    return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')

    if __name__ == '__main__':
        from doctest import testmod
        testmod()




def recuperarSenha(request):
    if temAcesso(request):
        return HttpResponse(status=500)

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


def gera_senha(tamanho):
    caracters = '0123456789abcdefghijlmnopqrstuwvxzABCEFGHIJKLMNOPQRSTUVXZ'
    senha = ''
    for char in xrange(tamanho):
        senha += choice(caracters)
    mypass=[]
    mypass.append(senha)

    return mypass


@login_required()
def listUsuarios(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    context = {}

    # Lista de cursos
    cursos = Curso.objects.all()
    context['cursos'] = cursos


    return render(request, 'listagemAlunos.html', context)


@login_required()
def getUsers(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    users = []

    if request.POST['idcurso'] == 'Todos':
        profs = ProfileUser.objects.filter(nome__contains=request.POST['pesquisar'])[:100]

        for prof in profs:
            user = {}
            user['id'] = prof.user.id
            user['nome'] = prof.nome
            user['username'] = prof.user.username

            try:
                mat = Matricula.objects.get(user=prof.user, atual=True)
                user['matriculado'] = mat.curso.nome + '-' + mat.curso.anoGrade
            except:
                user['matriculado'] = ''

            users.append(user)
    else:
        # Procura para ver se o aluno esta matriculado no curso da pesquisa
        idcurso = request.POST['idcurso']
        curso = Curso.objects.get(pk=idcurso)

        mats = Matricula.objects.filter(curso=curso)

        for mat in mats:
            # pegarei os alunos que estão entre os que podem se cadastrar
            try:
                prof = ProfileUser.objects.get(user=mat.user, nome__contains=request.POST['pesquisar'])

                user = {}
                user['id'] = prof.user.id
                user['nome'] = prof.nome
                user['username'] = prof.user.username
                user['matriculado'] = mat.curso.nome + '-' + mat.curso.anoGrade

                users.append(user)
            except Exception, e:
                print 'Err %s ', e



    return HttpResponse(json.dumps(users), content_type="application/json")


@login_required()
def turmasCursoAluno(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    turmas = []
    try:
        idusuario = request.POST['id']
        idcurso = request.POST['idcurso']
        user = User.objects.get(pk=idusuario)

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
def situacaoMatricula(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    sitmats = []
    try:
        idmatricula = request.POST['idmat']
        matricula = Matricula.objects.get(pk=idmatricula)
        sits = SituacaoMatricula.objects.filter(matricula=matricula)

        for st in sits:
            sit = {}
            sit['id'] = st.id
            sit['situacao'] = st.situacao
            sit['data'] = st.data.strftime("%m/%d/%Y")

            sitmats.append(sit)

        return HttpResponse(json.dumps(sitmats), content_type="application/json")
    except Exception, e:
        print 'Err' , e
    return HttpResponse(json.dumps(sitmats), content_type="application/json")


@login_required()
def changesituacao(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    try:

        sitmatri = request.POST['sitmatri']
        datamud = request.POST['datamud']
        idmatricula = request.POST['idmatricula']

        matri = Matricula.objects.get(pk=idmatricula)

        try:
            sit = SituacaoMatricula.objects.get(pk=request.POST['id'])
        except:
            sit = SituacaoMatricula()

        sit.matricula = matri
        date_object = datetime.strptime(datamud, '%d/%m/%Y')
        sit.data = date_object
        sit.situacao = sitmatri
        sit.save()

        return HttpResponse(1)
    except Exception, e:
        print "Erro: ", e
        return HttpResponse(-1)
