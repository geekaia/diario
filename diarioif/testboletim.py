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


    def print_users(self, idturma):
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

        turma = Turma.objects.get(pk=idturma)
        data = Notafalta.objects.values_list('aluno').filter(turma=turma).distinct()

        for i in data:
            prof = ProfileUser.objects.get(pk=int(i[0])) # i[0] é o id do usuario
            # aluno['id'] = int(i[0])
            # aluno['nome'] = prof.nome
            # alunos.append(aluno)


            elements.append(Paragraph("<b>BOLETIM</b>", styles['titutulo1']))
            elements.append(Paragraph("<br /><br />NOME: "+prof.nome.upper(), styles['leftName']))
            elements.append(Paragraph("CURSO: "+turma.curso.nome.upper()+" Ano: "+str(turma.anosemestre)+" Turma: "+turma.nome+"<br/><br/>", styles['leftName']))

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

            dicsL = Disciplina.objects.filter(curso=turma.curso, periodo=turma.anosemestre)

            def testNone(val):

                if val=='None':
                    return ''
                else:
                    return ''


            for i in dicsL:
                atrib = AtribAula.objects.filter(disciplina=i, turma=turma)

                for at in atrib:

                    notasAno = Notafalta.objects.filter(turma=turma, disciplina=at.disciplina,aluno=prof)[0]


                    row = []
                    row.append(Paragraph(at.disciplina.nome, styles['sNomeEsq']))
                    row.append(Paragraph(str(notasAno.nota1b if type(notasAno.nota1b)!=type(None) else ''), styles['stBodyBoletim']))
                    row.append(Paragraph(str(notasAno.falta1b), styles['stBodyBoletim']))
                    row.append(Paragraph(str(notasAno.nota2b if type(notasAno.nota2b)!=type(None) else ''), styles['stBodyBoletim']))
                    row.append(Paragraph(str(notasAno.falta2b), styles['stBodyBoletim']))
                    row.append(Paragraph(str(notasAno.nota3b if type(notasAno.nota3b)!=type(None) else ''), styles['stBodyBoletim']))
                    row.append(Paragraph(str(notasAno.falta3b), styles['stBodyBoletim']))
                    row.append(Paragraph(str(notasAno.nota4b if type(notasAno.nota4b)!=type(None) else ''), styles['stBodyBoletim']))
                    row.append(Paragraph(str(notasAno.falta4b), styles['stBodyBoletim']))
                    row.append(Paragraph(str(notasAno.mediaanual if type(notasAno.mediaanual)!=type(None) else ''), styles['stBodyBoletim']))
                    row.append(Paragraph(str(notasAno.recuperacao if type(notasAno.recuperacao)!=type(None) else ''), styles['stBodyBoletim']))
                    row.append(Paragraph(str(notasAno.mediapospf if type(notasAno.mediapospf)!=type(None) else ''), styles['stBodyBoletim']))
                    row.append(Paragraph(str(notasAno.mediapospf if type(notasAno.mediapospf)!=type(None) else ''), styles['stBodyBoletim']))
                    row.append(Paragraph(str(notasAno.situacaofinal if type(notasAno.situacaofinal)!=type(None) else ''), styles['stBodyBoletim']))

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


            # for user in users:
            #     elements.append(Paragraph(user.username, styles['centered']))


        doc.build(elements, onFirstPage=self.__header_footer, onLaterPages=self.__header_footer)

        # Get the value of the BytesIO buffer and write it to the response
        pdf = buffer.getvalue()
        buffer.close()

        return pdf

from django.contrib.auth.decorators import login_required
from io import BytesIO
# @login_required()
def gemPdf(request):
    # curso=None, ano bimestre=None, turma=None
    # Para o ano

    lista = []

    idturma = 24
    # turma = Turma.objects.get(pk=idturma)
    # data = Notafalta.objects.values_list('aluno').filter(turma=turma).distinct()
    # for i in data:
    #
    #         aluno = {}
    #         prof = ProfileUser.objects.get(pk=int(i[0])) # i[0] é o id do usuario
    #         dicsL = Disciplina.objects.filter(curso=turma.curso, periodo=turma.anosemestre)
    #         aluno['nome'] = prof.nome.upper()
    #         aluno['curso'] = prof.nome.upper()
    #
    #         disciplinas = []
    #
    #         for i in dicsL:
    #             atrib = AtribAula.objects.filter(disciplina=i, turma=turma)
    #
    #             for at in atrib:
    #                 disciplina = {}
    #                 notasAno = Notafalta.objects.filter(turma=turma, disciplina=at.disciplina,aluno=prof)[0]
    #                 disciplina['nome'] = notasAno.disciplina.nome.upper()
    #                 disciplina['nota1b'] = notasAno.disciplina.nome.upper()


    # com todos os dados do usuários da turma, grupo ou de um único usuário








    # if bimestre == None and turma == None:

    response = HttpResponse(content_type='application/pdf')
    buffer = BytesIO()
    report = BoletimLayout(buffer)
    pdf = report.print_users(24)
    response.write(pdf)

    return response
