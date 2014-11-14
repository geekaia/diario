# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Image, Paragraph, Table


class LetterMaker(object):

    # Initial configuration
    def __init__(self, pdf_file, org, seconds):
        self.c = canvas.Canvas(pdf_file, pagesize=letter)
        self.styles = getSampleStyleSheet()
        self.width, self.height = letter
        self.organization = org
        self.seconds = seconds

    def createDocument(self):
        voffset = 65

        # create a return address
        address = """<font size="9">
         Jack Spratt
         22 Ioway Blvd, Suite 100
         Galls, TX 75081-4016</font>
         """

        p = Paragraph(address, self.styles['Normal'])

        logo = Image('logo.png')
        logo.drawHeight = 2*inch
        logo.drawWidth = 2*inch

        data = [[p, logo]]

        table = Table(data, colWidths=4*inch)
        table.setStyle([('VALIGN', (0,0), (0,0), 'TOP')])
        table.wrapOn(self.c, self.width, self.height)
        table.drawOn(self.c, *self.coord(18, 60, mm))

        # Body of leter
        ptext = "Dear Sir or Madam: "
        self.createParagraph(ptext, 20, voffset+35)

        ptext = """
        The document you are holding is a set of requirements for you next mission, should you choose to accept it.
        In any event, this document will self-destruct <b> %s </b>
        sedonds after you read it. Yes, <b> %s </b> can tell when you're done... Usually.
        """ % (self.seconds, self.organization)

        p = Paragraph(ptext, self.organization)
        p.wrapOn(self.c, self.width - 70, self.height)
        p.drawOn(self.c, *self.coord(20, voffset+48, mm))

    def coord(self, x, y, unit=1):
        x, y = x * unit, self.height - y*unit

        return x, y

    def createParagraph(self, ptext, x, y, style=None):

        if not style:
            style = self.styles['Normal']

        p = Paragraph(ptext, self.styles['Normal'])
        p.wrapOn(self.c, self.width, self.height)
        p.drawOn(self.c, *self.coord(x, y, mm))


    def savePDF(self):
        self.c.save()



if __name__ == '__main__':
    doc = LetterMaker('example.pdf', 'The MVP', 10)
    doc.createDocument()
    doc.savePDF()









