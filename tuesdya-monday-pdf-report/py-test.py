from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors

# bodytext  style used for wrapping  data on flowables
styles = getSampleStyleSheet()
styleN = styles["BodyText"]
#used alignment if required
styleN.alignment = TA_LEFT

styleBH = styles["Normal"]
styleBH.alignment = TA_CENTER


hdescrpcion = Paragraph('''<b>descrpcion</b>''', styleBH)
hpartida = Paragraph('''<b>partida</b>''', styleBH)


descrpcion = Paragraph('long long long long long long long long long long long long long long long long long long long long line ', styleN)
partida = Paragraph('1', styleN)

data= [[hdescrpcion, hpartida],
       [partida ,descrpcion]]

table = Table(data)

table.setStyle(TableStyle([
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ]))

c = canvas.Canvas("a.pdf", pagesize=A4)
table.wrapOn(c, 50, 50)
table.drawOn(c, 100,600)
c.save()