# -*- coding: utf-8 -*-
from django.http import HttpResponse

from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle, PageBreak, Spacer
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


from usuarios import temAcesso

FONT_PATH = os.path.join(settings.BASE_DIR, 'static/fonts/OpenSans-Regular.ttf')
pdfmetrics.registerFont(TTFont('OpenSans', FONT_PATH))

FONT_PATH = os.path.join(settings.BASE_DIR, 'static/fonts/OpenSans-Bold.ttf')
pdfmetrics.registerFont(TTFont('OpenSans-Bold', FONT_PATH))

cores = [HexColor('#00ff00'), HexColor('#00ffff'), HexColor('#ff0000'), HexColor('#ffff00'), HexColor('#ff00ff'), HexColor('#ff9966')]

class BoletimLayout:
    ano = ''
    def __init__(self, buffer):
        # O padrão é sempre A4
        self.pagesize = A4

        self.buffer = buffer
        self.width, self.height = self.pagesize

        # A large collection of style sheets pre-made for us


    # @classmethod
    @staticmethod
    def __header_footer(canvas, doc):
        canvas.saveState()
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', align=TA_RIGHT))

        stH = ParagraphStyle(
            name='header1',
            fontName='OpenSans-Bold',
            fontSize=7,
            leading=8,
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
        logo.drawHeight = 0.45*inch
        logo.drawWidth = 0.35*inch

        txtHeader = """
            MINISTÉRIO DA EDUCAÇÃO/ SECRETARIA DE EDUCAÇÃO TECNOLÓGICA <br />
            INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE MATO GROSSO <br />
            PRÓ-REITORIA DE ENSINO - CALENDÁRIO ACADÊMICO  <br />
            CAMPUS JUINA
        """

        # print "Ano ", ano

        data = [[logo, Paragraph(txtHeader, styles['header1'])]]
        header=Table(data, colWidths=[45, 350])
        w, h = header.wrap(doc.width, doc.topMargin)

        style = TableStyle([
            ('VALIGN',(0, 0),(0,-1),'MIDDLE'),
            ('ALIGN', (0, 0), (-2, 0), 'RIGHT')
        ])


        header.setStyle(style)

        header.drawOn(canvas, doc.leftMargin-10, doc.height + doc.topMargin+10 - h+25)

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


    def print_users(self, mesesCalendario, mesesLetivos, firstS, secondS, year):
        styles = getSampleStyleSheet()

        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch/4,
                                leftMargin=inch/4-10,
                                topMargin=inch/2+5,
                                bottomMargin=inch/2+5,#   inch*1,
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
        sBody2 = ParagraphStyle(
            name='sBody2',
            fontName='OpenSans',
            fontSize=8,
            alignment=TA_CENTER,
        )
        sBody2t = ParagraphStyle(
            name='sBody2t',
            fontName='OpenSans-Bold',
            fontSize=8,
            alignment=TA_CENTER,
        )

        sBody2l = ParagraphStyle(
            name='sBody2l',
            fontName='OpenSans',
            fontSize=8,
            alignment=TA_LEFT,
            leading=7,
        )
        sBody2l2 = ParagraphStyle(
            name='sBody2l2',
            fontName='OpenSans',
            fontSize=7,
            alignment=TA_LEFT,
            leading=7,
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
        styles.add(sBody2)
        styles.add(sBody2t)
        styles.add(sBody2l)
        styles.add(sBody2l2)
        styles.add(sBodyEsq)
        styles.add(sNomeEsq)


        styles.add(ParagraphStyle(name='centered', alignment=TA_LEFT))


        monthnames= []

        import calendar
        def ParaMonths(val):
            return Paragraph(str(val), styles['sBody2t'])

        meses = [ParaMonths('Janeiro'), ParaMonths('Fevereiro'), ParaMonths('Março'), ParaMonths('Abril'), ParaMonths('Maio'), ParaMonths('Junho'), ParaMonths('Julho'), ParaMonths('Agosto'), ParaMonths('Setembro'), ParaMonths('Outubro'), ParaMonths('Novembro'), ParaMonths('Dezembro')]


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


            def getInicioMesclar(d, l):

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

                                if str(j) == str(val): # Não pinta o domingo
                                    if matrix == 0: # x
                                        position = coordX[cont1][cont2+1]

                                    return position, cont1, (cont2+1)
                            except Exception, e:
                                print "Error: %s " % e

                            cont2 += 1
                        cont1 += 1

                    return -1, -1

                x, linhax, yadd = findPosition(d, l, 0)
                #y = findPosition(d, l, 1)

                # lastLine = coordX[len(coordX)-1]
                # xlast = lastLine[len(lastLine)-1]

                lastLine = coordY[linhax]
                ylast = lastLine[len(lastLine)-1]


                return x, ylast, linhax, yadd




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


            wd = dtFim.weekday()
            if wd <= 2 or wd == 6:
                xMx, yMy, xAdd, yAdd = getInicioMesclar(dtFim.day, l)
                # print ('SPAN', xMx, (-1, -1))
                styleL.append(('SPAN', xMx, yMy)) # tudo certo

                try:
                    num = ContaDiasMonth(dtFim.year, dtFim.month, firstS, secondS)
                    if num != 0:
                        # l[xAdd][yAdd] = Paragraph(str(num) +' Dias Letivos', styles['sBody2l2'])
                        l[xAdd][yAdd] = str(num) +' Dias Letivos'
                except Exception, e:
                    print " Erro %s " % e


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

                        p = getTable(Ano['ano'], i)
                        l2 = []
                        l2.append([p])

                        # Aqui pega as estatísticas de cada mês

                        if mNum != '':
                            lastDayM = calendar.monthrange(Ano['ano'], i)[1]
                            dateLastM = datetime.date(Ano['ano'], i, lastDayM)

                            wd = dateLastM.weekday()
                            if wd != 6 and wd > 2:
                                try:
                                    num = ContaDiasMonth(Ano['ano'], i, firstS, secondS)
                                    if num != 0:
                                        l2.append([Paragraph(str(num) +' Dias Letivos', styles['sBody2l2'])])
                                except Exception, e:
                                    print " Erro %s " % e

                        tbLeg = Table(l2,
                                      colWidths=[135],
                                      style= [
                                          ('LEFTPADDING',(0,0),(-1,-1), 0),
                                          ('RIGHTPADDING',(0,0),(-1,-1), 0),
                                          ('TOPPADDING',(0,0),(-1,-1), 0),
                                          ('BOTTOMPADDING',(0,0),(-1,-1), 0)
                                      ]
                        )

                        l.append(tbLeg) # Acredito que seja isso
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


                        eventos = DiaExcept.objects.filter(dataInicio__range=(dtIni, dtFim))

                        # Initializa algum bimestre?
                        bimestreInit = Bimestre.objects.filter(dataInicio__range=(dtIni, dtFim), bimestreSemestre='bimestre')
                        bimestreFim = Bimestre.objects.filter(dataFim__range=(dtIni, dtFim), bimestreSemestre='bimestre')

                        semestreInit = Bimestre.objects.filter(dataInicio__range=(dtIni, dtFim), bimestreSemestre='semestre')
                        semestreFim = Bimestre.objects.filter(dataFim__range=(dtIni, dtFim), bimestreSemestre='semestre')


                        p =''
                        listParas = []

                        for evt in eventos:
                            if evt.tipo in ['FD']:
                                pA = [whatDate(evt.dataInicio, evt.dataFim, evt.tipo), tipos[evt.tipo]]
                            else:
                                pA = [whatDate(evt.dataInicio, evt.dataFim, evt.tipo), evt.descricao]

                            listParas.append({evt.dataInicio.day: pA })

                        for bimI in bimestreInit:
                            pA = [str(bimI.dataInicio.day), u'início do '+ str(bimI.numero)+u"º Bimestre"]
                            print pA

                            listParas.append({bimI.dataInicio.day: pA })

                        for bimI in bimestreFim:
                            pA = [str(bimI.dataFim.day), u'fim do '+ str(bimI.numero)+u"º Bimestre" + ' - ' + str(ContaDiasRange(firstS, secondS, bimI.dataInicio, bimI.dataFim)) + ' dias letivos']
                            print pA
                            listParas.append({bimI.dataFim.day: pA })


                        for bimI in semestreInit:
                            pA = [str(bimI.dataInicio.day), u'início do '+str(bimI.numero)+u"º Semestre"]
                            print pA

                            listParas.append({bimI.dataInicio.day: pA })

                        for bimI in semestreFim:
                            pA = [str(bimI.dataFim.day), u'fim do '+ str(bimI.numero)+u"º Semestre" + ' - ' + str(ContaDiasRange(firstS, secondS, bimI.dataInicio, bimI.dataFim)) + ' dias letivos']
                            print pA
                            listParas.append({bimI.dataFim.day: pA })

                        listParas.sort()

                        print "ListParas: ", listParas


                        cont = 0
                        blackList = []
                        while len(listParas) > cont:
                            key = listParas[cont].keys()[0]
                            listAdd = []
                            index = 0
                            for pars in listParas:
                                if key == pars.keys()[0] and index not in blackList:
                                    listAdd.append(pars)
                                    blackList.append(index)

                                index += 1

                            if len(listAdd) == 1:
                                p += listAdd[0][listAdd[0].keys()[0]][0] + ' - ' + listAdd[0][listAdd[0].keys()[0]][1] + '<br/>'
                            else:
                                index = 0

                                hasprint = False
                                for vad in listAdd:
                                    print "Val: ", vad[vad.keys()[0]][0], ' ', vad[vad.keys()[0]][1]
                                    if len(listAdd) != (index+1):
                                        initP = '' if hasprint != False else (vad[vad.keys()[0]][0] +' - ')
                                        p += initP + vad[vad.keys()[0]][1] + ' / '
                                        hasprint = True
                                    else:
                                        p += vad[vad.keys()[0]][1] + '<br />'

                                    index += 1
                            cont += 1

                        #
                        # for ParaL in listParas:
                        #     p += ParaL[ParaL.keys()[0]] + '<br/>'


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
                                # First Line
                                ('TOPPADDING', (0, 0), (-1, 0), 1),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), -1),

                                # Second line
                                ('TOPPADDING', (0, 3), (-1, 3), 1),
                                ('BOTTOMPADDING', (0, 3), (-1, 3), -1),

                                # Third line
                                ('TOPPADDING', (0, 6), (-1, 6), 1),
                                ('BOTTOMPADDING', (0, 6), (-1, 6), -1),




                                ('VALIGN', (0, 0), (-1, 0),'MIDDLE'),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('VALIGN',(0,0), (-1, -1),'TOP'),
                                ]
        )


        def Conta(l, d):
            c = 0
            for dy in l:
                # print "Day: ", dy, ' Weekday: ', dy.weekday(), ' D: ', d
                if dy.weekday() == d:
                    c += 1

            return MyP(c)

        listaStatis1 = []
        listaStatis2 = []

        def MyP(val):
            return Paragraph(str(val), styles['sBody2t'])

        def MyPl(val):
            return Paragraph(str(val), styles['sBody2l'])

        listaStatis1.append([MyP('D'), MyP('S'), MyP('T'), MyP('Q'), MyP('Q'), MyP('S'), MyP('S')])
        listaStatis2.append([MyP('D'), MyP('S'), MyP('T'), MyP('Q'), MyP('Q'), MyP('S'), MyP('S')])


        # print "Conta firsts 1: ", Conta(firstS, 1)
        # print "Conta firsts 1: ", Conta(firstS, 2)
        # print "Conta firsts 1: ", Conta(firstS, 3)
        # print "Conta firsts 1: ", Conta(firstS, 4)
        # print "Conta firsts 1: ", Conta(firstS, 5)
        # print "Conta firsts 1: ", Conta(firstS, 6)

        listaStatis1.append([MyP(0), Conta(firstS, 0), Conta(firstS, 1), Conta(firstS, 2), Conta(firstS, 3), Conta(firstS, 4), Conta(firstS, 5)])
        listaStatis2.append([MyP(0), Conta(secondS, 0), Conta(secondS, 1), Conta(secondS, 2), Conta(secondS, 3), Conta(secondS, 4), Conta(secondS, 5)])

        l1 = []
        l1.append([MyP('DIAS LETIVOS '+str(year)+'.1')])
        tbStais = Table(listaStatis1,  colWidths=[22, 22, 22, 22, 22, 22, 22], style=[('GRID',(0,0),(-1,-1), 0.5,colors.black), ('BACKGROUND', (0, 0), (-1, 0), colors.grey)])
        l1.append([tbStais])
        l1.append([MyPl('TOTAL = '+str(len(firstS)))])

        tb1F = Table(l1, colWidths=[165],  style=[('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey)])

        l2 =  []
        l2.append([MyP('DIAS LETIVOS '+str(year)+'.2')])
        tbStais2 = Table(listaStatis2,  colWidths=[22, 22, 22, 22, 22, 22, 22], style=[
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ])
        l2.append([tbStais2])
        l2.append([MyPl('TOTAL = '+str(len(secondS)))])
        tb2F = Table(l2,  colWidths=[165], style=[('GRID',(0,0),(-1,-1),0.5,colors.black), ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey)])


        # mesesLetivos
        elements.append(tableNotas)
        # elements.append( Paragraph("<br />", styles['stBodyBoletim']))
        s = Spacer(width=0, height=2)
        elements.append(s)

        llegenda = [['', MyPl('Dias Letivos')], ['', MyPl('Férias Docentes')], ['', MyPl('Feriados')], ['', MyPl('Período de Provas Finais')], ['', MyPl('Ponto Facultativo')]]
        lLeg = []
        lLeg.append([MyP('LEGENDA')])
        tbLegL = Table(llegenda,  colWidths=[12, 105], style=[
            ('GRID',(0,0),(-1,-1),0,colors.black),

            ('TOPPADDING', (0, 0), (-1, -1), -3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),

            ('BACKGROUND', (0, 0), (-2, 0), cores[0]),
            ('BACKGROUND', (0, 1), (-2, 1), cores[1]),
            ('BACKGROUND', (0, 2), (-2, 2), cores[2]),
            ('BACKGROUND', (0, 3), (-2, 3), cores[3]),
            ('BACKGROUND', (0, 4), (-2, 4), cores[4]),

        ])



        lLeg.append([tbLegL])
        tbLeg = Table(lLeg,  colWidths=[125], style=[
            ('GRID',(0,0),(-1,-1),0.5,colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TOPPADDING', (0, 0), (-1, 0), 1),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 1),
        ])



        lTables = [[tb1F , tb2F, tbLeg]]
        tBstat = Table(lTables,  colWidths=[175, 175, 155])

        elements.append(tBstat)
        elements.append(PageBreak())

        doc.build(elements, onFirstPage=self.__header_footer, onLaterPages=self.__header_footer)

        # Get the value of the BytesIO buffer and write it to the response
        pdf = buffer.getvalue()
        buffer.close()

        return pdf

def ContaDiasMonth(ano, mes, firstS, secondS):
    dateIni = datetime.date(ano, mes, 1)
    rangeM = calendar.monthrange(ano, mes)
    dateFim = datetime.date(ano, mes, rangeM[1])

    c = 0
    for dy in firstS:
        if dateIni <= dy and dy <=  dateFim:
            c += 1

    for dy in secondS:
        if dateIni <= dy and dy <=  dateFim:
            c += 1

    return c


def ContaDiasRange(firstS, secondS, inicio, fim):
    dateIni = datetime.date(inicio.year, inicio.month, inicio.day)
    dateFim = datetime.date(fim.year, fim.month, fim.day)

    c = 0
    for dy in firstS:
        if dateIni <= dy and dy <=  dateFim:
            # if dy.month >= 7:
            #     print "Dia excessão: ", dy
            c += 1
    # print "Firsts: ", c, 'inicio: ', inicio, ' Fim: ', fim
    for dy in secondS:
        if dateIni <= dy and dy <=  dateFim:
            c += 1
    # print "SecondS: ", c, 'inicio: ', inicio, ' Fim: ', fim
    return c



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

def getStatis(listdays, ano):
    firstSemester = []
    secondSemester = []

    tiposCan = ['O', 'EVT']
    semestre1 = Bimestre.objects.get(ano=str(ano), numero='1', bimestreSemestre='semestre')
    semestre2 = Bimestre.objects.get(ano=str(ano), numero='2', bimestreSemestre='semestre')
    # Não precisa do segundo, pois se não for o primeiro é o segundo rsrs

    for listD in listdays:
        daysAno = listD['dias']

        # Aqui adiciona somente os sábados
        evtsSb = DiaExcept.objects.filter(dataInicio__lte=semestre1.dataInicio, dataFim__gte=semestre2.dataFim)
        for evts in evtsSb:
            if evts.tipo=='SB' and evts.dataInicio.weekday()==5:
                daysAno.append([evts.dataInicio.month, evts.dataInicio.day, evts.dataInicio.year])

        for day in daysAno:
            # print day
            d = datetime.date(day[2], day[0], day[1])
            if semestre1.dataInicio <= d and d <= semestre1.dataFim:
                # print "Dia ", d
                wd = d.weekday()
                if wd != 6: # Nao e permitido aulas aos domingos
                    eventos = DiaExcept.objects.filter(dataInicio__gte=d, dataFim__lte=d)

                    if len(eventos) ==0:
                        eventos = DiaExcept.objects.filter(dataInicio=d) # para dias em que não é range



                    if len(eventos) == 0:
                        if wd != 5: # Não é permitido o sábado se não for por evento
                            firstSemester.append(d)
                    else:
                        for evt in eventos:

                            if d.month == 3:
                                print "Day", d, 'evts: ', len(eventos), evt.tipo, 'vt ini', evt.dataInicio, ' evt.f', evt.dataFim

                            if evt.tipo in tiposCan:
                                if wd != 5:
                                    firstSemester.append(d)
                                    break
                            else:
                                if evt.tipo == 'SB':
                                    firstSemester.append(d)
                                    break

            else:
                wd = d.weekday()
                # print "Dia ", d, ' week day', wd
                if wd != 6: # Nao e permitido aulas aos domingos
                    # Há qualquer dia em que não se registra aula?
                    eventos = DiaExcept.objects.filter(dataInicio__gte=d, dataFim__lte=d)

                    if len(eventos) == 0:
                        eventos = DiaExcept.objects.filter(dataInicio=d) # para dias em que não é range

                    if len(eventos) == 0:
                        if wd != 6: # Não é permitido o sábado se não for por evento
                            secondSemester.append(d)
                    else:
                        for evt in eventos:
                            if evt.tipo in tiposCan:
                                if wd != 5:
                                    secondSemester.append(d)
                                    break
                            else:
                                if evt.tipo == 'SB':
                                    secondSemester.append(d)
                                    break

    return firstSemester, secondSemester




from django.contrib.auth.decorators import login_required
from io import BytesIO
# @login_required()
def gemPdf(request, ano=None):

    if temAcesso(request):
        return HttpResponse(status=500)

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

    firstS, secondS = getStatis(anosMesesLetivos, ano)
    # Devo passar aqui para a função para estatísticas



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
    # print "AnosMesesCalendarios"


    # print "Anosmeses calendario: ", anosMesesCalendario

    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    report = BoletimLayout(buffer)
    pdf = report.print_users(anosMesesCalendario, anosMesesLetivos, firstS, secondS, ano)
    # print "Anos Meses Letivos: ", anosMesesLetivos
    response.write(pdf)

    return response
