from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'diarioif.views.home', name='home'),

    # User Info
    url(r'^login$', 'diarioif.views.loginUser', name='login'),
    url(r'^profile$', 'diarioif.views.changeProfile', name='profile'),
    url(r'^cadastro$', 'diarioif.views.cadastrarUser', name='cadastro'),
    url(r'^recuperar$', 'diarioif.views.recuperarSenha', name='recuperar'),
    url(r'^getUsers', 'diarioif.views.getUsers', name='getUsers'),

    url(r'^listUsuarios$', 'diarioif.views.listUsuarios', name='listUsuarios'),



    url(r'^cursocad/$', 'diarioif.views.cursocad', name='cursocad'),
    url(r'^cursocad/(?P<id>\d[^/]*)$', 'diarioif.views.cursocad', name='cursocad'),



    url(r'^sair$', 'diarioif.views.sair', name='sair'),

    # Json services
    url(r'^cities$', 'diarioif.views.getCities', name='cities'),
    url(r'^bairros$', 'diarioif.views.getBairros', name='bairros'),
    url(r'^ruas', 'diarioif.views.getRuas', name='ruas'),
    url(r'^cep', 'diarioif.views.getCep', name='cep'),

    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
