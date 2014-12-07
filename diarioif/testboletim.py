# -*- coding: utf-8 -*-
from django.http import HttpResponse

from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from django.contrib.auth.models import User
from reportlab.lib.units import inch
from reportlab.lib import colors


import os.path
from reportlab.lib.enums import TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
from diarioif.models import *

FONT_PATH = os.path.join(settings.BASE_DIR, 'static/fonts/OpenSans-Regular.ttf')
pdfmetrics.registerFont(TTFont('OpenSans', FONT_PATH))

FONT_PATH = os.path.join(settings.BASE_DIR, 'static/fonts/OpenSans-Bold.ttf')
pdfmetrics.registerFont(TTFont('OpenSans-Bold', FONT_PATH))

from usuarios import temAcesso

class BoletimLayout:
    def __init__(self, buffer):
        # O padrão é sempre A4
        self.pagesize = landscape(A4)

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
        logo.drawHeight = 0.5*inch
        logo.drawWidth = 0.4*inch

        txtHeader = """
        INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE MATO GROSSO <br />
        CAMPUS BARRA DO GARÇAS <br />
        DEPARTAMENTO DE ENSINO
        """

        data = [[logo,Paragraph(txtHeader, styles['header1'])]]

        header=Table(data, colWidths=[35, 350])
        w, h = header.wrap(doc.width, doc.topMargin)

        style = TableStyle([ ('VALIGN',(0, 0),(0,-1),'MIDDLE')])
        header.setStyle(style)

        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h+70)

        # header =Paragraph('This is a Multi-line header. It goes on every page. '*5, styles['Normal'])
        # w, h = header.wrap(doc.width, doc.topMargin)
        # header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h )


        footerText = """
        Endereço: Estrada de Acesso a BR-158, s/n - CEP: 78.600-00 -- Barra do Garças-MT <br />
        Telefone: (66) 3402-0100 <br />
        """

        # Footer
        footer = Paragraph(footerText, styles['footer1'])

        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)

        # Release the canvas
        canvas.restoreState()


    def print_users(self, lista):
        styles = getSampleStyleSheet()

        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch/4,
                                leftMargin=inch/4,
                                topMargin=inch/2+40,
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
            fontSize=8,
            alignment=TA_CENTER,
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
        styles.add(sNomeEsq)


        styles.add(ParagraphStyle(name='centered', alignment=TA_LEFT))


        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality


        for aluno in lista:
            # aluno['id'] = int(i[0])
            # aluno['nome'] = prof.nome
            # alunos.append(aluno)


            elements.append(Paragraph("<b>BOLETIM</b>", styles['titutulo1']))
            elements.append(Paragraph("<br /><br />NOME: "+aluno['nome'], styles['leftName']))
            elements.append(Paragraph("CURSO: "+aluno['curso']+" Ano: "+str(+aluno['anosemestre'])+" Turma: "+aluno['turma.nome']+"<br/><br/>", styles['leftName']))




            cabecalhoT = []
            cabecalhoT.append(Paragraph('DISCIPLINA', styles['stTituloName']))
            cabecalhoT.append(Paragraph('MÉDIA 1ºB', styles['stTituloName']))
            cabecalhoT.append(Paragraph('FALTAS', styles['stTituloName']))
            cabecalhoT.append(Paragraph('MÉDIA 2°B', styles['stTituloName']))
            cabecalhoT.append(Paragraph('FALTAS', styles['stTituloName']))
            cabecalhoT.append(Paragraph('MÉDIA 3ºB', styles['stTituloName']))
            cabecalhoT.append(Paragraph('FALTAS', styles['stTituloName']))
            cabecalhoT.append(Paragraph('MÉDIA 4ºB', styles['stTituloName']))
            cabecalhoT.append(Paragraph('FALTAS', styles['stTituloName']))
            cabecalhoT.append(Paragraph('MÉDIA\nANUAL', styles['stTituloName']))
            cabecalhoT.append(Paragraph('PROVA\nFINAL', styles['stTituloName']))
            cabecalhoT.append(Paragraph('MÉDIA PÓS\nPROVA FINAL', styles['stTituloName']))
            cabecalhoT.append(Paragraph('MÉDIA\nANUAL\nFINAL', styles['stTituloName']))
            cabecalhoT.append(Paragraph('SITUAÇÃO', styles['stTituloName']))

            data = []
            data.append(cabecalhoT)


            for al in aluno['disciplinas']:
                row = []
                row.append(Paragraph(str(al['nome']), styles['sNomeEsq']))
                row.append(Paragraph(str(al['nota1b']), styles['stBodyBoletim']))
                row.append(Paragraph(str(al['falta1b']), styles['stBodyBoletim']))
                row.append(Paragraph(str(al['nota2b']), styles['stBodyBoletim']))
                row.append(Paragraph(str(al['falta2b']), styles['stBodyBoletim']))
                row.append(Paragraph(str(al['nota3b']), styles['stBodyBoletim']))
                row.append(Paragraph(str(al['falta3b']), styles['stBodyBoletim']))
                row.append(Paragraph(str(al['nota4b']), styles['stBodyBoletim']))
                row.append(Paragraph(str(al['falta4b']), styles['stBodyBoletim']))
                row.append(Paragraph(str(al['mediaanual']), styles['stBodyBoletim']))
                row.append(Paragraph(str(al['recuperacao']), styles['stBodyBoletim']))
                row.append(Paragraph(str(al['mediapospf']), styles['stBodyBoletim']))
                row.append(Paragraph(str(al['mediapospf']), styles['stBodyBoletim']))
                row.append(Paragraph(str(al['situacaofinal']), styles['stBodyBoletim']))

                data.append(row)

            tableNotas=Table(data,
                             colWidths=[250, 43, 35,44,35,43,35,43,35,43,33,53,35,50],
                             hAlign='LEFT',
                             style=[('GRID',(0,0),(-1,-1),0.5,colors.black),
                                    #('VALIGN', (0,0), (0,-1), 'MIDDLE'),
                                    ('VALIGN', (0,0), (-1,0), 'MIDDLE'),
                                    ('ALIGN',(0,0),(-1,0),'CENTER'),
                                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                    ('ALIGN', (1, 1), (-1, -1), 'CENTER')
                                    ]
            )

            elements.append(tableNotas)
            elements.append(PageBreak())


        doc.build(elements, onFirstPage=self.__header_footer, onLaterPages=self.__header_footer)

        # Get the value of the BytesIO buffer and write it to the response
        pdf = buffer.getvalue()
        buffer.close()

        return pdf

from django.contrib.auth.decorators import login_required
from io import BytesIO
# @login_required()
def gemPdf(request, idcurso=None, idturma=None, ano=None, periodo=None, idaluno=None):
    # curso=None, ano bimestre=None, turma=None
    # Para o ano
    if temAcesso(request):
        return HttpResponse(status=500)

    print "Argumento  idcurso: ", idcurso, " idturma: ", idturma, " ano: ", ano, " periodo: ", periodo, ' idaluno: ', idaluno

    lista = []

    # Pesquisa com os argumentos curso, periodo e ano

    if ano != None and periodo != None and idcurso!=None:
        print "Boletim por curso "
        curso = Curso.objects.get(pk=idcurso)
        turmasL = Turma.objects.filter(curso=curso, anosemestre=periodo, anoturma=ano) # Aqui dará somente uma linha
    else:
        print "Boletim por turma"
        # Para o caso de for por turma
        turmasL = Turma.objects.filter(pk=idturma)


    for turma in turmasL:
        data = Notafalta.objects.values_list('aluno').filter(turma=turma).distinct()
        for i in data:

                aluno = {}
                prof = ProfileUser.objects.get(pk=int(i[0])) # i[0] é o id do usuario

                # Aqui eu poderei pegar o boletim de um aluno em específico como ID
                if idaluno != None and idturma != None and prof.user.id != int(idaluno):
                    continue

                dicsL = Disciplina.objects.filter(curso=turma.curso, periodo=turma.anosemestre)
                aluno['nome'] = prof.nome.upper()
                aluno['curso'] = prof.nome.upper()
                aluno['anosemestre'] = turma.anosemestre
                aluno['turma.nome'] = turma.nome

                disciplinas = []
                for i in dicsL:
                    atrib = AtribAula.objects.filter(disciplina=i, turma=turma)

                    for at in atrib:
                        try:
                            disciplina = {}
                            notasAno = Notafalta.objects.filter(turma=turma, disciplina=at.disciplina,aluno=prof)[0]
                            disciplina['nome'] = notasAno.disciplina.nome.upper().encode('utf-8')
                            disciplina['nota1b'] = str(notasAno.nota1b if type(notasAno.nota1b)!=type(None) else '')
                            disciplina['falta1b'] = str(notasAno.falta1b if type(notasAno.falta1b)!=type(None) else '')
                            # disciplina['falta1b'] = str(notasAno.nota1b if type(notasAno.nota1b)!=type(None) else '')
                            disciplina['nota2b'] = str(notasAno.nota2b if type(notasAno.nota2b)!=type(None) else '')
                            disciplina['falta2b'] = str(notasAno.falta2b if type(notasAno.falta2b)!=type(None) else '')
                            disciplina['nota3b'] = str(notasAno.nota3b if type(notasAno.nota3b)!=type(None) else '')
                            disciplina['falta3b'] = str(notasAno.falta3b if type(notasAno.falta3b)!=type(None) else '')
                            disciplina['nota4b'] = str(notasAno.nota4b if type(notasAno.nota4b)!=type(None) else '')
                            disciplina['falta4b'] = str(notasAno.falta4b if type(notasAno.falta4b)!=type(None) else '')
                            disciplina['mediaanual'] = str(notasAno.mediaanual if type(notasAno.mediaanual)!=type(None) else '')
                            disciplina['recuperacao'] = str(notasAno.recuperacao if type(notasAno.recuperacao)!=type(None) else '')
                            disciplina['mediapospf'] = str(notasAno.mediapospf if type(notasAno.mediapospf)!=type(None) else '')
                            disciplina['situacaofinal'] = str(notasAno.situacaofinal if type(notasAno.situacaofinal)!=type(None) else '')

                            disciplinas.append(disciplina)
                        except:
                            print 'Disc inexistnete'

                aluno['disciplinas'] = disciplinas
                lista.append(aluno)

        for i in lista:
            print i['nome']
            for d in i['disciplinas']:
                print d['nome']



    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    report = BoletimLayout(buffer)
    pdf = report.print_users(lista)
    response.write(pdf)

    return response
