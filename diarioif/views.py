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
from usuarios import temAcesso

@login_required()
def home(request):

    mensagem = ''
    isAuth = request.user.is_authenticated()
    context = {'mensagem': mensagem, 'isAuth':isAuth}

    return render(request, 'base.html', context)



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
    if temAcesso(request):
        return HttpResponse(status=500)

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

        return redirect('/listCourses')


    if id != None:
        curso = Curso.objects.get(pk=id)
        context['curso'] = curso


    return render(request, 'cursoCad.html', context)

@login_required()
def bimestrecad(request, id=None):
    if temAcesso(request):
        return HttpResponse(status=500)

    context = {}

    if request.POST:
        try:
            bimestre = Bimestre.objects.get(pk=int(request.POST['id']))
            print 'Peguei o id do Bimestre'
        except:
            bimestre = Bimestre()

        bimestre.ano = request.POST['ano']
        bimestre.bimestreSemestre = request.POST['bimestreSemestre']
        bimestre.numero = request.POST['numero']

        date_manip = datetime.strptime(request.POST['dataInicio'], '%d/%m/%Y')
        bimestre.dataInicio = date_manip

        date_manipF = datetime.strptime(request.POST['dataFim'], '%d/%m/%Y')
        bimestre.dataFim = date_manipF

        bimestre.save()

        return redirect('/listBimestres')

    if id != None:
        bimestre = Bimestre.objects.get(pk=id)
        context['bimestre'] = bimestre

    return render(request, 'cadBimestre.html', context)


@login_required()
def geBimestres(request, ano=None):
    if temAcesso(request):
        return HttpResponse(status=500)

    bimestres = []

    print "Ano ", ano

    try:

        bimestreList = Bimestre.objects.filter(ano=str(ano))

        print "len(bi): ", len(bimestreList)

        for i in bimestreList:
            bimestre = {}
            bimestre['id'] = i.id
            bimestre['ano'] = i.ano
            bimestre['bimestreSemestre'] = i.bimestreSemestre
            bimestre['numero'] = i.numero
            bimestre['dataInicio'] = i.dataInicio.strftime('%d/%m/%Y')
            bimestre['dataFim'] = i.dataFim.strftime('%d/%m/%Y')
            bimestres.append(bimestre)
            # cidades[i.id] = i.nome
    except:
        print 'Erro ao pegar cidades'

    return HttpResponse(json.dumps(bimestres), content_type="application/json")


@login_required()
def listBimestres(request, id=None):
    if temAcesso(request):
        return HttpResponse(status=500)

    context = {}

    return render(request, 'bimestreList.html', context)


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


def hasAcess(request):
    prof =  ProfileUser.objects.get(user=request.user)

    return ''


@login_required()
def geCourses(request):
    if temAcesso(request):
        return HttpResponse(status=500)

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
    if temAcesso(request):
        return HttpResponse(status=500)

    context = {}


    return render(request, 'cursoList.html', context)


@login_required()
def turmas(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    context = {}
    cursos = Curso.objects.all()
    context['cursos'] = cursos

    profs = ProfileUser.objects.filter(tipo='Professor')
    context['profs'] = profs

    return render(request, 'turmas.html', context)

@login_required()
def getTurmas(request, idcurso, periodo, ano ):
    if temAcesso(request):
        return HttpResponse(status=500)

    turmas = []
    curso = Curso.objects.get(pk=idcurso)
    turmasL = Turma.objects.filter(curso=curso, anosemestre=periodo, anoturma=ano)

    for i in turmasL:
        turma = {}
        turma['id'] = i.id
        turma['nome'] = i.nome
        turmas.append(turma)


    return HttpResponse(json.dumps(turmas), content_type="application/json")

@login_required()
def cadturmas(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    try:
        if request.POST:
            # Lembrar de perguntar o periodo da turma caso o curso seja semestral para que possa montar o período inicial e final
            turma = Turma()
            turma.nome = request.POST['nome']
            turma.anosemestre = request.POST['anosemestre']

            # caso o curso seja semestral primeiro ou segundo semestre
            periodo = request.POST['semestre']

            turma.anoturma = request.POST['anoturma']
            courseid = request.POST['curso']
            turma.curso = Curso.objects.get(pk=courseid)
            turma.save()

            discs = Disciplina.objects.filter(curso=turma.curso, periodo=turma.anosemestre)
            for disc in discs:
                atrib = AtribAula()

                # Atribuição de aula.
                atrib.disciplina = disc
                atrib.turma = turma

                quantaV = 0

                # Aqui temos toos os possíveis arranjos de cursos
                # O Ano pode ser Anual
                                # avaliações: Bimestrais ou Semestrais

                # Semestral
                                # Avaliações: Semestrais e Semestrais


                inicio = 0

                # Indez matriz 0, 1, 2, 3
                if turma.curso.periodo == 'Ano' and turma.curso.avaliacaopor == 'Bimestre':
                    print "Cai aqui 1"
                    quantaV = 3
                    bimestresSem = Bimestre.objects.filter(ano=turma.anoturma, bimestreSemestre='bimestre')
                elif turma.curso.periodo == 'Ano' and turma.curso.avaliacaopor == 'Semestre':
                    print "Cai aqui 2"
                    quantaV = 1
                    bimestresSem = Bimestre.objects.filter(ano=turma.anoturma, bimestreSemestre='semestre')

                # Ainda falta determinar o início e fim pelo período
                elif turma.curso.periodo == 'Semestre' and turma.curso.avaliacaopor == 'Bimestre':
                    print "Cai aqui 3"
                    if int(periodo) == 1:
                        quantaV = 1
                    else:
                        inicio = 2
                        quantaV = 3
                    bimestresSem = Bimestre.objects.filter(ano=turma.anoturma, bimestreSemestre='bimestre')
                # Ainda falta determinar o início e fim pelo período
                elif turma.curso.periodo == 'Semestre' and turma.curso.avaliacaopor == 'Semestre':
                    print "Cai aqui 4"
                    if int(periodo) == 1:
                        quantaV = 0
                    else:
                        inicio = 1
                        quantaV = 1

                    bimestresSem = Bimestre.objects.filter(ano=turma.anoturma, bimestreSemestre='semestre')

                first = bimestresSem[inicio]
                last = bimestresSem[quantaV]

                # default 1 ano para cursos anuais e 6 meses para cursos semestrais
                atrib.periodoInicio = first.dataInicio
                atrib.periodoFim = last.dataFim
                atrib.acesso = True
                atrib.save()

            return HttpResponse(1)

    except:

        return HttpResponse(-1)


@login_required()
def delturma(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    try:
        if request.POST:
            idturma = request.POST['idturma']
            t = Turma.objects.get(pk=idturma)
            t.delete()

            return HttpResponse(1)
    except:
        return HttpResponse(-1)



@login_required()
def getAlunosCurso(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    try:
        alunosmatch = []
        nome = request.POST['nome']
        idturma = request.POST['idturma']
        t = Turma.objects.get(pk=int(idturma))


        # Aqui tem que mostrar os alunos que estão matriculados regularmente no curso
        alunos = ProfileUser.objects.filter(tipo='Aluno', nome__icontains=nome)

        for i in alunos:

            # Está matriculado neste curso?
            idmat = Matricula.objects.filter(curso=t.curso, user=i.user)

            # Já foi adicionado na turma?
            nota = Notafalta.objects.filter(aluno=i, turma=t)

            if len(idmat) != 0 and len(nota) == 0:
                aluno = {}
                aluno['id'] = i.id
                aluno['nome'] = i.nome
                alunosmatch.append(aluno)

        return HttpResponse(json.dumps(alunosmatch), content_type="application/json")

    except:
        return HttpResponse(json.dumps(alunosmatch), content_type="application/json")

@login_required()
def cadTurmaAlunosDisc(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    try:
        idturma = request.POST['idturma']
        turma = Turma.objects.get(pk=idturma)
        idaluno = request.POST['aluno']
        aluno = ProfileUser.objects.get(pk=idaluno)

        # Cadastrar todos?
        todos = request.POST['todos']
        print "Todos: ", todos
        vals = {'true': True, 'false': False}
        todasD = vals[str(todos)]

        if todasD:
            # disciplinas
            dics = Disciplina.objects.filter(curso=turma.curso, periodo=turma.anosemestre)

            for disc in dics:
                try:
                    # verifica se já não há nada para esta disciplina  - Isto evita duplicidade
                    print "Aluno ", aluno.id, " Disc: ", disc.id, " Curso: ", turma.curso.id, " Turma: ", turma.id
                    nota =Notafalta.objects.get(disciplina=disc, turma=turma, aluno=aluno)

                    # Pula pq já tem cadastro e não tem problema
                    continue
                except:
                    nota = Notafalta()

                nota.aluno = aluno
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
        else:
            iddisc = int(request.POST['iddisc'])
            atr = AtribAula.objects.get(pk=iddisc)

            try:
                # verifica se já não há nada para esta disciplina  - Isto evita duplicidade
                print "2Aluno ", aluno.id, " Disc: ", atr.disciplina.id, " Curso: ", turma.curso.id, " Turma: ", turma.id
                nota = Notafalta.objects.get(disciplina=atr.disciplina, turma=turma, aluno=aluno)
            except:
                nota = Notafalta()

            nota.aluno = aluno
            nota.disciplina = atr.disciplina
            nota.curso = turma.curso
            nota.turma = turma
            nota.falta1b = 0
            nota.falta2b = 0
            nota.falta3b = 0
            nota.falta4b = 0
            nota.falta5b = 0
            nota.save()

            return HttpResponse(1)
    except Exception, e:
        return HttpResponse(-1)

@login_required()
def remDiscAluno(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    try:
        idant = request.POST['idnt']
        ntf = Notafalta.objects.get(pk=int(idant))
        ntf.delete()

        return HttpResponse(1)
    except:
        return HttpResponse(-1)


@login_required()
def remAlunoTurma(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    try:
        idrem = request.POST['id']
        profrm = ProfileUser.objects.get(pk=int(idrem))
        ntfs = Notafalta.objects.filter(aluno=profrm)

        for nt in ntfs:
            nt.delete()

        return HttpResponse(1)
    except:
        print 'Err '


    return HttpResponse(-1)


@login_required()
def listDiscAluno(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    disc = []

    idaluno = request.POST['id']
    prof = ProfileUser.objects.get(pk=int(idaluno))

    notas = Notafalta.objects.filter(aluno=prof)

    for nt in notas:
        nta = {}
        nta['id'] = nt.id
        nta['nome'] = nt.disciplina.nome
        disc.append(nta)

    return HttpResponse(json.dumps(disc), content_type="application/json")


@login_required()
def listDiscTurma(request):

    if temAcesso(request):
        return HttpResponse(status=500)

    discs = []

    try:
        # profs = ProfileUser.objects.filter(tipo='Professor')
        idturma = request.POST['idturma']
        t = Turma.objects.get(pk=idturma)
        dicsL = Disciplina.objects.filter(curso=t.curso, periodo=t.anosemestre)

        usr = User.objects.get(pk=request.user.id)
        prof = ProfileUser.objects.get(user=usr)

        tudo = False
        if prof.tipo in ['Secretaria', 'Administrador']:
            tudo = True


        for i in dicsL:

            if tudo == True:
                atrib = AtribAula.objects.filter(disciplina=i, turma=t)
            else:
                atrib = AtribAula.objects.filter(disciplina=i, turma=t, professor=prof)



            for at in atrib:
                dic = {}
                dic['id'] = at.id
                dic['nome'] = i.nome
                dic['inicio'] = at.periodoInicio.strftime("%m/%d/%Y") #isoformat()
                dic['fim'] = at.periodoFim.strftime("%m/%d/%Y")       #strftime("%d/%m/%Y")
                dic['acesso'] = at.acesso
                dic['add'] = True

                try:
                    u = ProfileUser.objects.get(pk=at.professor.id)
                    profsel = str(u.id) + '-' + u.nome
                except:
                    print 'err'
                    profsel =''

                dic['profsel'] = profsel

                discs.append(dic)

    except Exception, e:
        print 'Hello exception %s !!!' % e

    return HttpResponse(json.dumps(discs), content_type="application/json")



@login_required()
def changeAtrib(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    try:
        at = AtribAula.objects.get(pk=request.POST['id'])
        prof = ProfileUser.objects.get(pk=request.POST['prof'].split('-')[0])
        at.professor = prof
        inicio = datetime.strptime(request.POST['inicio'], '%d/%m/%Y')
        print "Data inicio: ", inicio
        at.periodoInicio = inicio
        fim = datetime.strptime(request.POST['fim'], '%d/%m/%Y')
        print "Data fim: ", fim
        at.periodoFim = fim
        at.acesso = False if request.POST['acesso'] =='false' else True

        at.save()

        return HttpResponse(1)
    except Exception, e:
        print "Erro: %s " % e
        return HttpResponse(-1)
# id:4
# prof:5-Carlinha Gostosinha
# inicio:25/1/2014
# fim:25/12/2014
# acesso:false




@login_required()
def listAlunosTurma(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    alunos = []

    try:
        turma = Turma.objects.get(pk=request.POST['idturma'])
        data = Notafalta.objects.values_list('aluno').filter(turma=turma).distinct()

        for i in data:
            print "Inteiro: ",  int(i[0])
            aluno = {}
            prof = ProfileUser.objects.get(pk=int(i[0]))
            aluno['id'] = int(i[0])
            aluno['nome'] = prof.nome
            alunos.append(aluno)
    except:
        print 'err'

    return HttpResponse(json.dumps(alunos), content_type="application/json")


@login_required()
def updateRow(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    try:
        id = request.POST['id']
        teacherid = request.POST['teacherid']
        disc = request.POST['disc']

        user = User.objects.get(pk=teacherid)

        Notafalta.objects.filter()

    except:
        print 'erro ao atualizar'


    return HttpResponse(-1)




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
def getPeriodos(request, idcurso=None):

    if temAcesso(request):
        return HttpResponse(status=500)

    cursoNumPs = {}

    try:
        curso = Curso.objects.get(pk=idcurso)
        cursoNumPs['periodos'] = curso.quantPeriodo
        cursoNumPs['periodopor'] = curso.periodo # Ano/Semestre
    except:
        print 'Erro Periodos'

    return HttpResponse(json.dumps(cursoNumPs), content_type="application/json")


@login_required()
def disciplinas(request):

    if temAcesso(request):
        return HttpResponse(status=500)

    context = {}
    cursos = Curso.objects.all()
    context['cursos'] = cursos

    return render(request, 'disciplinas.html', context)


@login_required()
def getDisciplinas(request,idcurso=None, numperiodo=None):

    Disciplinas = []

    try:
        curso = Curso.objects.get(pk=idcurso)
        discL = Disciplina.objects.filter(curso=curso, periodo=numperiodo)


        for i in discL:
            disc = {}
            disc['id'] = i.id
            disc['nome'] = i.nome
            disc['periodo'] = i.periodo
            disc['horaaula'] = i.horaaula
            disc['hora'] = i.hora
            Disciplinas.append(disc)
    except:
        print 'Erro Periodos'

    return HttpResponse(json.dumps(Disciplinas), content_type="application/json")


@login_required()
def cadDisciplinas(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    try:
        if request.POST:

            cursoID = request.POST['curso']
            curso = Curso.objects.get(pk=cursoID)

            id = request.POST['id']

            if int(id) == -1:
                disc = Disciplina()
            else:
                disc = Disciplina.objects.get(pk=id)

            disc.nome = request.POST['nome']
            disc.horaaula = request.POST['horaaula']
            disc.periodo = int(request.POST['periodo'])
            disc.hora = request.POST['hora']
            disc.curso = curso
            disc.save()

            return HttpResponse(1)

    except:
        return HttpResponse(-1)

@login_required()
def removerDisc(request, idrem=None):
    if temAcesso(request):
        return HttpResponse(status=500)

    try:
        disc = Disciplina.objects.get(pk=idrem)
        disc.delete()

        return HttpResponse(1)
    except:
        return HttpResponse(-1)


@login_required()
def sair(request):
    logout(request)

    return redirect('/')











