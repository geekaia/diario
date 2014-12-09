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

from usuarios import temAcesso

def boletim(request):
    if temAcesso(request):
        return HttpResponse(status=500)

    context = {}
    cursos = Curso.objects.all()
    context['cursos'] = cursos

    profs = ProfileUser.objects.filter(tipo='Professor')
    context['profs'] = profs
    # context['form'] = FileUploadedForm



    return render(request, 'boletim.html', context)