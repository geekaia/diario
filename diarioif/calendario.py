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

from lancarnotas import defaultencode



@login_required()
def diasexcept(request):
    context = {}

    return render(request, 'diasexcept.html', context)


def calendarioano(request):

    from gencalendario import *


    return gemPdf(request)


@login_required()
def addDiaExcept(request):
    try:
        dataInicioB = request.POST['dataInicio']
        dataInicio = datetime.strptime(dataInicioB, '%d/%m/%Y')
        dataFimB = request.POST['dataFim']
        dataFim = datetime.strptime(dataFimB, '%d/%m/%Y')
        tipo = request.POST['tipo']
        descricao = request.POST['descricao']
        ano = request.POST['ano']

        d = DiaExcept()

        d.dataInicio = dataInicio

        if tipo in ['SB']:
            d.dataFim = dataInicio
        else:
            d.dataFim = dataFim
        d.tipo = tipo
        d.descricao = descricao
        d.ano = ano
        d.save()

        return HttpResponse(1)
    except:
        return HttpResponse(-1)

@login_required()
def listDiasExcept(request):

    daysL = []
    ano = request.POST['ano']
    diasex = DiaExcept.objects.filter(ano=ano).order_by('-dataInicio')


    tipos = {'FD': 'Férias Docentes', 'FDS': 'Férias Discentes', 'F': 'Feriado', 'PF':'Período de Provas Finais', 'PFAC': 'Ponto Facultativo', 'SB':'Sábado Letivo', 'O': 'Outro', 'EVT': 'Eventos', 'RC': 'Recesso',  'SP': 'Semana Pedagógica' }

    for i in diasex:
        d = {}
        d['id'] = i.id
        d['ano'] = i.ano
        d['dataInicio'] = i.dataInicio.strftime("%d/%m/%Y")
        d['dataFim'] = '' if i.tipo in ['SB'] else i.dataFim.strftime("%d/%m/%Y")
        d['tipo'] = i.tipo
        d['tipod'] = tipos[i.tipo]
        d['descricao'] = i.descricao

        daysL.append(d)

    return HttpResponse(json.dumps(daysL), content_type="application/json")


@login_required()
def removeDayE(request):
    try:
        id = request.POST['id']

        d = DiaExcept.objects.get(pk=int(id))
        d.delete()

        return HttpResponse(1)
    except:
        return HttpResponse(-1)