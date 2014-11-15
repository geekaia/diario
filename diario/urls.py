# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'diarioif.views.home', name='home'),

    # Usuarios Manip
    url(r'^login$', 'diarioif.usuarios.loginUser', name='login'),
    url(r'^profile$', 'diarioif.usuarios.changeProfile', name='profile'),
    url(r'^profile/(?P<id>\d[^/]*)$', 'diarioif.usuarios.changeProfile', name='profile'),
    url(r'^cadastro$', 'diarioif.usuarios.cadastrarUser', name='cadastro'),
    url(r'^recuperar$', 'diarioif.usuarios.recuperarSenha', name='recuperar'),
    url(r'^listUsuarios$', 'diarioif.usuarios.listUsuarios', name='listUsuarios'),
    url(r'^cadUsuario', 'diarioif.usuarios.cadUsuario', name='cadUsuario'),
    url(r'^getUsers', 'diarioif.usuarios.getUsers', name='getUsers'),
    url(r'^matriculasAluno', 'diarioif.usuarios.matriculasAluno', name='matriculasAluno'),
    url(r'^matricularAluno', 'diarioif.usuarios.matricularAluno', name='matricularAluno'),
    url(r'^turmasCursoAluno', 'diarioif.usuarios.turmasCursoAluno', name='turmasCursoAluno'),
    url(r'^situacaoMatricula', 'diarioif.usuarios.situacaoMatricula', name='situacaoMatricula'),
    url(r'^changesituacao', 'diarioif.usuarios.changesituacao', name='changesituacao'),
    # Cria varios alunos baseando-se em uma Lista
    url(r'^importarAlunos', 'diarioif.importar.importarAlunos', name='importarAlunos'),
    url(r'^addvarios', 'diarioif.importar.addvarios', name='addvarios'),
    url(r'^fileupload', 'diarioif.importar.fileupload', name='fileupload'),
    url(r'^importXlsNotas', 'diarioif.importar.importXlsNotas', name='importXlsNotas'),


    # Boletim do Aluno
    url(r'^boletim', 'diarioif.boletim.boletim', name='boletim'),
    # Boletim de uma turma
    url(r'^ReportBoletim/(?P<idturma>\d[^/]*)$', 'diarioif.testboletim.gemPdf', name='ReportBoletim'),
    # boletim de um curso
    url(r'^ReportBoletimCurso/(?P<idcurso>\d[^/]*)/(?P<ano>\d[^/]*)/(?P<periodo>\d[^/]*)$', 'diarioif.testboletim.gemPdf', name='ReportBoletimCurso'),
    # Boletim de um aluno em específico
    url(r'^alunoBoletim/(?P<idturma>\d[^/]*)/(?P<idaluno>\d[^/]*)$', 'diarioif.testboletim.gemPdf', name='alunoBoletim'),


    # Cursos
    url(r'^listCourses', 'diarioif.views.listCourses', name='listCourses'),
    url(r'^cursocad/$', 'diarioif.views.cursocad', name='cursocad'),
    url(r'^cursocad/(?P<id>\d[^/]*)$', 'diarioif.views.cursocad', name='cursocad'),

    # Bimestres
    url(r'^bimestrecad/$', 'diarioif.views.bimestrecad', name='bimestrecad'),
    url(r'^bimestrecad/(?P<id>\d[^/]*)$', 'diarioif.views.bimestrecad', name='bimestrecad'),
    url(r'^listBimestres/$', 'diarioif.views.listBimestres', name='listBimestres'),


    # Disciplinas
    url(r'^disciplinas', 'diarioif.views.disciplinas', name='disciplinas'),
    url(r'^cadDisciplinas', 'diarioif.views.cadDisciplinas', name='cadDisciplinas'),
    url(r'^getPeriodos/(?P<idcurso>\d[^/]*)$', 'diarioif.views.getPeriodos', name='getPeriodos'),
    url(r'^removerDisc/(?P<idrem>\d[^/]*)$', 'diarioif.views.removerDisc', name='removerDisc'),
    url(r'^getDisciplinas/(?P<idcurso>\d[^/]*)/(?P<numperiodo>\d[^/]*)$', 'diarioif.views.getDisciplinas', name='getDisciplinas'),

    # Turmas
    url(r'^turmas', 'diarioif.views.turmas', name='turmas'),
    url(r'^cadturmas', 'diarioif.views.cadturmas', name='cadturmas'),
    url(r'^delturma', 'diarioif.views.delturma', name='delturma'),
    url(r'^getAlunosCurso', 'diarioif.views.getAlunosCurso', name='getAlunosCurso'),
    url(r'^listAlunosTurma', 'diarioif.views.listAlunosTurma', name='listAlunosTurma'),
    url(r'^listDiscTurma', 'diarioif.views.listDiscTurma', name='listDiscTurma'),
    url(r'^changeAtrib', 'diarioif.views.changeAtrib', name='changeAtrib'),
    url(r'^getTurmas/(?P<idcurso>\d[^/]*)/(?P<periodo>\d[^/]*)/(?P<ano>\d[^/]*)$', 'diarioif.views.getTurmas', name='getTurmas'),
    url(r'^cadTurmaAlunosDisc', 'diarioif.views.cadTurmaAlunosDisc', name='cadTurmaAlunosDisc'),

    # Lancar notas
    url(r'^lancarnotas', 'diarioif.lancarnotas.notas', name='lancarnotas'),
    url(r'^notasAlunosTurma', 'diarioif.lancarnotas.notasAlunosTurma', name='notasAlunosTurma'),
    url(r'^quantBimestre', 'diarioif.lancarnotas.quantBimestre', name='quantBimestre'),
    url(r'^saveNotas', 'diarioif.lancarnotas.saveNotas', name='saveNotas'),




    url(r'^sair$', 'diarioif.views.sair', name='sair'),

    # Json services provided by the system
    url(r'^cities$', 'diarioif.views.getCities', name='cities'),
    url(r'^bairros$', 'diarioif.views.getBairros', name='bairros'),
    url(r'^ruas', 'diarioif.views.getRuas', name='ruas'),
    url(r'^cep', 'diarioif.views.getCep', name='cep'),
    url(r'^geCourses', 'diarioif.views.geCourses', name='geCourses'),
    url(r'^geBimestres/(?P<ano>\d[^/]*)$', 'diarioif.views.geBimestres', name='geBimestres'),

    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
