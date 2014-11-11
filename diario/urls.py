from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'diarioif.views.home', name='home'),

    # User Info
    url(r'^login$', 'diarioif.views.loginUser', name='login'),
    url(r'^profile$', 'diarioif.views.changeProfile', name='profile'),
    url(r'^profile/(?P<id>\d[^/]*)$', 'diarioif.views.changeProfile', name='profile'),

    url(r'^cadastro$', 'diarioif.views.cadastrarUser', name='cadastro'),

    url(r'^recuperar$', 'diarioif.views.recuperarSenha', name='recuperar'),


    url(r'^listUsuarios$', 'diarioif.views.listUsuarios', name='listUsuarios'),
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


    url(r'^sair$', 'diarioif.views.sair', name='sair'),

    # Json services provided by the system
    url(r'^cities$', 'diarioif.views.getCities', name='cities'),
    url(r'^bairros$', 'diarioif.views.getBairros', name='bairros'),
    url(r'^ruas', 'diarioif.views.getRuas', name='ruas'),
    url(r'^cep', 'diarioif.views.getCep', name='cep'),
    url(r'^getUsers', 'diarioif.views.getUsers', name='getUsers'),
    url(r'^geCourses', 'diarioif.views.geCourses', name='geCourses'),
    url(r'^geBimestres/(?P<ano>\d[^/]*)$', 'diarioif.views.geBimestres', name='geBimestres'),

    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
