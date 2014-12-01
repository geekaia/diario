# -*- coding: utf-8 -*-
from django.http import HttpResponse

from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from django.contrib.auth.models import User
from reportlab.lib.units import inch
from reportlab.lib import colors

from reportlab.lib.colors import HexColor
import os.path
from reportlab.lib.enums import TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
from diarioif.models import *
import calendar
import datetime
from datetime import timedelta

FONT_PATH = os.path.join(settings.BASE_DIR, 'static/fonts/OpenSans-Regular.ttf')
pdfmetrics.registerFont(TTFont('OpenSans', FONT_PATH))

FONT_PATH = os.path.join(settings.BASE_DIR, 'static/fonts/OpenSans-Bold.ttf')
pdfmetrics.registerFont(TTFont('OpenSans-Bold', FONT_PATH))


class BoletimLayout:
    def __init__(self, buffer):
        # O padrão é sempre A4
        self.pagesize = A4

        self.buffer = buffer
        self.width, self.height = self.pagesize

        # A large collection of style sheets pre-made for us

    @staticmethod
    def __header_footer(canvas, doc):
        canvas.saveState()

        styles = getSampleStyleSheet()
        # Our Custom Style
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))


        stH = ParagraphStyle(
            name='header1',
            fontName='OpenSans-Bold',
            fontSize=7,
        )

        stF = ParagraphStyle(
            name='footer1',
            fontName='OpenSans-Bold',
            fontSize=6,
        )
        styles.add(stH)
        styles.add(stF)

        # Header


        fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo.png')
        logo = Image(fn)
        logo.drawHeight = 0.6*inch
        logo.drawWidth = 0.5*inch

        txtHeader = """
            MINISTÉRIO DA EDUCAÇÃO/ SECRETARIA DE EDUCAÇÃO TECNOLÓGICA <br />
            INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE MATO GROSSO <br />
            PRÓ-REITORIA DE ENSINO - CALENDÁRIO ACADÊMICO ANO_ATUAL <br />
            CAMPUS JUINA
        """

        data = [[logo,Paragraph(txtHeader, styles['header1'])]]
        header=Table(data, colWidths=[40, 350])
        w, h = header.wrap(doc.width, doc.topMargin)

        style = TableStyle([ ('VALIGN',(0, 0),(0,-1),'MIDDLE')])
        header.setStyle(style)

        header.drawOn(canvas, doc.leftMargin-10, doc.height + doc.topMargin+10 - h+70)

        # header =Paragraph('This is a Multi-line header. It goes on every page. '*5, styles['Normal'])
        # w, h = header.wrap(doc.width, doc.topMargin)
        # header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h )


        # footerText = """
        # Por enquanto nada />
        # """
        #
        # # Footer
        # footer = Paragraph(footerText, styles['footer1'])
        #
        # w, h = footer.wrap(doc.width, doc.bottomMargin)
        # footer.drawOn(canvas, doc.leftMargin, h)

        # Release the canvas
        canvas.restoreState()


    def print_users(self, mesesCalendario, mesesLetivos):
        styles = getSampleStyleSheet()

        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch/4,
                                leftMargin=inch/4-10,
                                topMargin=inch/2+17,
                                bottomMargin=inch*1.2,
                                pagesize=self.pagesize)

        # Our container for "Flowable" objects
        elements = []

        stTitulo = ParagraphStyle(
            name='titutulo1',
            fontName='OpenSans-Bold',
            fontSize=10,
            alignment=TA_CENTER,
        )

        stTituloName = ParagraphStyle(
            name='leftName',
            fontName='OpenSans-Bold',
            fontSize=6,
            alignment=TA_LEFT,
        )

        stHeader = ParagraphStyle(
            name='stTituloName',
            fontName='OpenSans-Bold',
            fontSize=6,
            alignment=TA_CENTER,
        )

        sBody = ParagraphStyle(
            name='stBodyBoletim',
            fontName='OpenSans',
            fontSize=6,
            alignment=TA_CENTER,
        )

        sBodyEsq = ParagraphStyle(
            name='stBodyEsq',
            fontName='OpenSans',
            fontSize=6,
            alignment=TA_LEFT,
            leading=9,
        )

        sNomeEsq = ParagraphStyle(
            name='sNomeEsq',
            fontName='OpenSans',
            fontSize=8,
            alignment=TA_LEFT,
        )


        styles.add(stTitulo)
        styles.add(stTituloName)
        styles.add(stHeader)
        styles.add(sBody)
        styles.add(sBodyEsq)
        styles.add(sNomeEsq)


        styles.add(ParagraphStyle(name='centered', alignment=TA_LEFT))


        monthnames= []

        import calendar

        meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']


        def getTable(year, month):
            calendar.setfirstweekday(calendar.SUNDAY)
            l = calendar.monthcalendar(int(year),int(month))
            n = []
            cont1 = 0

            def getCoors(d, l, corIndex):
                # Matriz com todas as coordenadas
                #Dias Letivos
                #Férias Docentes, recesso
                #Feriados
                #Período de Provas Finais
                #Ponto Facultativo
                # SP - Semana Pedagógica
                cores = [HexColor('#00ff00'), HexColor('#00ffff'), HexColor('#ff0000'), HexColor('#ffff00'), HexColor('#ff00ff'), HexColor('#ff9966')]


                listXy = []

                # lista de coordenadas de X
                coordX = [
                    [(0,1), (1,1),  (2,1), (3,1), (4,1), (5,1), (6,1)],
                    [(0,2), (1,2),  (2,2), (3,2), (4,2), (5,2), (6,2)],
                    [(0,3), (1,3),  (2,3), (3,3), (4,3), (5,3), (6,3)],
                    [(0,4), (1,4),  (2,4), (3,4), (4,4), (5,4), (6,4)],
                    [(0,5), (1,5),  (2,5), (3,5), (4,5), (5,5), (6,5)],
                    [(0,6), (1,6),  (2,6), (3,6), (4,6), (5,6), (6,6)],
                ]

                # lista de coordenadas de Y
                coordY = [
                    [(-7,1), (-6,1), (-5,1), (-4,1), (-3,1), (-2,1), (-1,1)],
                    [(-7,2), (-6,2), (-5,2), (-4,2), (-3,2), (-2,2), (-1,2)],
                    [(-7,3), (-6,3), (-5,3), (-4,3), (-3,3), (-2,3), (-1,3)],
                    [(-7,4), (-6,4), (-5,4), (-4,4), (-3,4), (-2,4), (-1,4)],
                    [(-7,5), (-6,5), (-5,5), (-4,5), (-3,5), (-2,5), (-1,5)],
                    [(-7,6), (-6,6), (-5,6), (-4,6), (-3,6), (-2,6), (-1,6)],
                ]

                def findPosition(val, l, matrix):
                    cont1 = 0
                    for i in l:
                        cont2 = 0
                        for j in i:
                            try:
                                # Is Here
                                # print "Cont1: ", cont1, " Cont2: ", cont2

                                if str(j) == str(val) and cont2 != 0: # Não pinta o domingo
                                    if matrix == 0:
                                        position = coordX[cont1][cont2]
                                    else:
                                        position = coordY[cont1][cont2]

                                    return position
                            except Exception, e:
                                print "Error: %s " % e

                            cont2 += 1
                        cont1 += 1

                    return -1

                x = findPosition(d, l, 0)
                y = findPosition(d, l, 1)

                if corIndex == -1:
                    x = -1

                if x != -1:
                    listXy.append(('BACKGROUND', x, y, cores[corIndex]))

                return listXy

            hei = 12
            wid = 18

            styleL = [
                        ('GRID',(0,0),(-1,-1),0.5,colors.black),
                        ('LEFTPADDING',(0,0),(-1,-1), 0),
                        ('RIGHTPADDING',(0,0),(-1,-1), 0),
                        ('TOPPADDING',(0,0),(-1,-1), 0),
                        ('BOTTOMPADDING',(0,0),(-1,-1), -2),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0), (-1, -2),'BOTTOM'),
                ]

            # # Green
            # dias = [1, 10, 27, 13,  8]
            # for myd in dias:
            #     Pintar = getCoors(myd, l, 1)
            #     for p in Pintar:
            #         styleL.append(p)

            rangeM = calendar.monthrange(year, month)
            dtIni = datetime.date(year, month, 1)
            dtFim = datetime.date(year, month, rangeM[1])

            eventos = DiaExcept.objects.filter(dataInicio__range=(dtIni, dtFim)).order_by('dataInicio')

            diasmes = range(1, rangeM[1])

            letivoDias = []
            for mL in mesesLetivos:
                if mL['ano'] == year:
                    letivoDias = mL['dias']

            # print 'ano', year, " Letivo Dias", letivoDias

            for evt in eventos:
                # Range Days
                ini = evt.dataInicio.day
                fim = evt.dataFim.day

                if evt.tipo =='SB':
                    fim = ini

                cor = 0
                if evt.tipo in ['FD', 'RC', 'FDS']:
                    cor = 1
                elif evt.tipo == 'F':
                    cor = 2
                elif evt.tipo == 'PF':
                    cor = 3
                elif evt.tipo == 'PFAC':
                    cor = 4
                elif evt.tipo == 'SP':
                    cor = 5
                else:
                    cor = 0

                tpula = ['FDS', 'O', 'EVT']

                if evt.tipo in tpula:
                    continue


                # Férias Docentes - 1
                # Feriados - 2
                # Período de Provas Finais - 3
                # Ponto Facultativo - 4

                dias = range(ini, fim+1)

                # Tipos que tem uma cor diferente e, por isso devem ser removidos
                tipos = ['FD', 'FDS', 'F', 'PF', 'PFAC', 'RC', 'SP']

                if evt.tipo != 'SB' and evt.tipo in tipos:

                    for dY in dias:
                        i=0
                        while i < len(letivoDias):
                            if letivoDias[i][1] == dY and letivoDias[i][0] == evt.dataInicio.month and letivoDias[i][2] == evt.dataInicio.year:
                                remove = True
                            else:
                                remove = False

                            if remove == True:
                                del letivoDias[i]
                            else:
                                i += 1

                elif evt.tipo == 'SB':
                    letivoDias.append([evt.dataInicio.month, dias[0], evt.dataInicio.year])

                for myd in dias:
                    Pintar = getCoors(myd, l, cor)

                    print "Week d"
                    DayT = datetime.date(evt.dataInicio.year, evt.dataInicio.month, myd)
                    wd = DayT.weekday()
                    if wd > 4:
                        # print "É maioree ", DayT, ' Week Day: ', wd
                        continue


                    for p in Pintar:
                        styleL.append(p)

            # Pinta tudo de Verde
            for lDay in letivoDias:
                if lDay[0] == month and lDay[2] == year:
                    cor = 0
                    Pintar = getCoors(lDay[1], l, cor)
                    for p in Pintar:
                        styleL.append(p)

            # print "Dias Finais: ", letivoDias




            l.insert(0, ['D', 'S', 'T', 'Q', 'Q', 'S', 'S'])


            for i in l:
                cont2 = 0
                for j in i:
                    if j == 0:
                        l[cont1][cont2] = ''

                    l[cont1][cont2] = Paragraph(str(l[cont1][cont2]), styles['stBodyBoletim'])

                    cont2 += 1
                cont1 += 1



            tb =Table(l,
                colWidths=[wid, wid, wid, wid, wid, wid, wid],
                rowHeights=[hei, hei, hei, hei, hei, hei] if len(l)==6 else [hei, hei, hei, hei, hei, hei, hei],
                style=styleL
            )

            return tb

        def getQuatro(t, actual):
            m = []
            mNum = []
            initial = actual
            contnull = 0
            for i in range(initial, initial+4):
                try:
                    m.append(meses[t[i]-1])
                    mNum.append(t[i])
                    actual = i
                except:
                    contnull += 1
                    m.append('')

            return m, (actual+1), contnull, mNum

        for Ano in mesesCalendario:



            actual = 0
            while actual < len(Ano['meses']):
                l, actual, contnull, mNum = getQuatro(Ano['meses'], actual)

                print "Vars:"
                print "L ", l
                print "actual ", actual
                print "contnull ", contnull
                print "mNum ", mNum

                # Só tem fazios
                if contnull == 4:
                    continue

                monthnames.append(l)

                l = []
                for i in mNum:
                    try:
                        l.append(getTable(Ano['ano'], i)) # Acredito que seja isso
                    except:
                        l.append('')

                monthnames.append(l)

                paras = []

                tipos = {
                    'SB': u'Sábado Letivo',
                    'FD': u'Férias Docentes',
                    'F': u'Feriado',
                    'PF': u'Período de Provas Finais',
                    'PFAC': u'Ponto Facultativo',
                    'O': u'Outro',
                    'EVT': u'Eventos',
                    'RC': u'Recesso',
                }

                def whatDate(dtI, dtF, t):
                    if evt.dataInicio.day == evt.dataFim.day and evt.dataInicio.month == evt.dataFim.month:
                        return str(evt.dataInicio.day)
                    elif t in ['SB']:
                        return str(evt.dataInicio.day)
                    elif evt.dataInicio.month == evt.dataFim.month:
                        return str(evt.dataInicio.day) + " a " + str(evt.dataFim.day)
                    else:
                        rangeM = calendar.monthrange(evt.dataFim.year, evt.dataFim.month)
                        return str(evt.dataInicio.day) + " a " + str(rangeM[1]) # Tipo de evento que ultrapasa os limites do mês

                for i in mNum:
                    try:
                        # Data Inicial e final da query
                        rangeM = calendar.monthrange(Ano['ano'],i)
                        dtIni = datetime.date(Ano['ano'], i, 1)
                        dtFim = datetime.date(Ano['ano'], i, rangeM[1])

                        print "dtIni: ", dtIni
                        print "dtFim: ", dtFim

                        eventos = DiaExcept.objects.filter(dataInicio__range=(dtIni, dtFim))
                        print "Len(eventos): ", len(eventos)
                        p =''
                        for evt in eventos:
                            if evt.tipo in ['FD']:
                                p += whatDate(evt.dataInicio, evt.dataFim, evt.tipo) + ' - ' + tipos[evt.tipo] +"<br />"
                            else:
                                p += whatDate(evt.dataInicio, evt.dataFim, evt.tipo) + ' - ' + evt.descricao +"<br />"

                            print evt.descricao, "evt id: ", evt.id

                        # Falta verificar o que pode ser adicionado para efentos que começam em um mês e terminam em outro
                        # Verificar se há algum efento que termina neste mês
                        paras.append(Paragraph(p, styles['stBodyEsq']))
                    except Exception, e:
                        print "Ocorreu um excessão: %s" % e
                        paras.append('')

                monthnames.append(paras)

        tableNotas =Table(monthnames,
                         colWidths=[140, 140, 140, 140],
                         style=[('GRID',(0,0),(-1,-1),0.5,colors.black),
                                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey), # First
                                ('BACKGROUND', (0, 3), (-1, 3), colors.lightgrey),
                                ('BACKGROUND', (0, 6), (-1, 6), colors.lightgrey),
                                # ('VALIGN',(0,0), (-1, -1),'BOTTOM'),
                                # ('LEFTPADDING',(0,0),(-1,-1), 1),
                                # ('RIGHTPADDING',(0,0),(-1,-1), 1),
                                # ('TOPPADDING',(0,0),(-1,-1), 8),
                                # ('BOTTOMPADDING',(0,0),(-1,-1), 1)

                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('VALIGN',(0,0), (-1, -1),'TOP'),
                                ]
        )

        elements.append(tableNotas)
        elements.append(PageBreak())


        doc.build(elements, onFirstPage=self.__header_footer, onLaterPages=self.__header_footer)

        # Get the value of the BytesIO buffer and write it to the response
        pdf = buffer.getvalue()
        buffer.close()

        return pdf

def getDias(dtInc, dataFinal, year):
    # A secretaria deve definir bimestres como período inicial e final letivo
    bims = Bimestre.objects.filter(dataInicio__range=(dtInc, dataFinal), bimestreSemestre='bimestre', ano=year)
    # Dia dos anos
    anoDays =[]

    print "Quant bimestres", len(bims)
    # datasAnos
    for b in bims:
        initiald = b.dataInicio
        print "Bimestre: ", b.numero

        while initiald <= b.dataFim:

            # Exclui os sábados e domingos
            if initiald.weekday() < 5:
                # print "Atual: ", initiald, ' week day: ', initiald.weekday()
                anoDays.append([initiald.month, initiald.day, initiald.year])

            initiald += timedelta(days=1)
        print "  "

    return anoDays


def getAnosMeses(dataInicial, dataFinal, cod=1):
    anos = []

    dtInc = dataInicial
    # anos desta data
    for year in range(dataInicial.year, dataFinal.year+1):
      ano = {}
      ano['ano'] = year

      if cod != -1:
        ano['dias'] = getDias(dtInc, dataFinal, year)

      if dtInc.year == dataFinal.year:
        ano['meses'] = range(dtInc.month, dataFinal.month+1)
      else:
        while dtInc.year == year:
          ano['meses'] = range(dataInicial.month, dtInc.month+1)
          dtInc += timedelta(days=1)

        dataInicial = dtInc
      anos.append(ano)

    return anos




from django.contrib.auth.decorators import login_required
from io import BytesIO
# @login_required()
def gemPdf(request, ano=None):

    lista = []

        # Pega os dias Letivos
    ano = 2014 #request.POST['ano']
    bimestreFirst = Bimestre.objects.filter(ano=ano)

    # Aqui só contam os dias letivos
    initialB = bimestreFirst[0].dataInicio
    finalB = bimestreFirst[len(bimestreFirst)-1].dataFim

    for bim in bimestreFirst:
        if bim.dataInicio < initialB:
            initialB = bim.dataInicio
        if bim.dataFim > finalB:
            finalB = bim.dataFim

    anosMesesLetivos = getAnosMeses(initialB, finalB)
    # print "Anos Meses Letivos: ", anosMesesLetivos


    # Com todos os anos, meses, dias letivos, não letivos e datas comemorativas
    calendario = []

    diaEx = DiaExcept.objects.filter(ano=int(ano))
    initialA = diaEx[0].dataInicio
    finalA = diaEx[0].dataFim

    for d in diaEx:
        if d.dataInicio < initialA:
            initialA = d.dataInicio
        if d.dataFim > finalA:
            finalA = d.dataFim

    # print "DataIni: ", initialA, " Final: ", finalA
    if finalB > finalA:
        finalA = finalB

    if initialB < initialA:
        initialA = initialB


    # print "DataIni: ", initialA, " Final: ", finalA

    anosMesesCalendario = getAnosMeses(initialA, finalA, -1)

    # print "Anosmeses calendario: ", anosMesesCalendario

    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    report = BoletimLayout(buffer)
    pdf = report.print_users(anosMesesCalendario, anosMesesLetivos)
    # print "Anos Meses Letivos: ", anosMesesLetivos
    response.write(pdf)

    return response
