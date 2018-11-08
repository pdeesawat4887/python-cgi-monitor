from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas


# def hello(c):
#     c.drawString(100,100,"Hello World")
# c = canvas.Canvas("hello.pdf")
# hello(c)
# c.showPage()
# c.save()

# ================================================ #

# from reportlab.lib.pagesizes import letter, A4
# myCanvas = Canvas('myfile.pdf', pagesize=letter)
# width, height = letter #keep for later


# def hello(c):
#     from reportlab.lib.units import inch
#     # move the origin up and to the left
#     c.translate(inch,inch)
#     # define a large font
#     c.setFont("Helvetica", 14)
#     # choose some colors
#     c.setStrokeColorRGB(0.2,0.5,0.3)
#     c.setFillColorRGB(1,0,1)
#     # draw some lines
#     c.line(0, 0, 0, 1.7 * inch)
#     c.line(0, 0, 5 * inch, 0)
#     # draw a rectangle
#     c.rect(0.2 * inch, 0.2 * inch, 1 * inch, 1.5 * inch, fill=1)
#     # make text go straight up
#     c.rotate(90)
#     # change color
#     c.setFillColorRGB(0, 0, 0.77)
#     # say hello (note after rotate the y coord needs to be negative!)
#     c.drawString(0.3 * inch, -inch, "Hello World")
#
# c = canvas.Canvas("hello.pdf")
# hello(c)
# c.showPage()
# c.save()

def test_report():
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    import time

    start_date = time.strftime('%d-%m-%Y %H:%M:%S')

    canvas = canvas.Canvas("form1.pdf", pagesize=letter)
    canvas.setLineWidth(1)
    canvas.setFont('Helvetica', 12)

    canvas.drawString(30, 750, 'DATE GENERATE')
    canvas.drawString(450, 750, start_date)
    canvas.line(440, 745, 570, 745)
    # canvas.line(420, 730, 600, 730)

    canvas.drawString(30, 730, 'REPORT TOPIC')
    canvas.drawString(450, 730, 'PROBES')
    canvas.line(440, 725, 570, 725)
    # canvas.line(480, 747, 580, 747)
    #
    # canvas.drawString(275, 725, 'AMOUNT OWED:')
    # canvas.drawString(500, 725, "$1,000.00")
    # canvas.line(378, 723, 580, 723)
    #
    # canvas.drawString(30, 703, 'RECEIVED BY:')
    # canvas.line(120, 700, 580, 700)
    # canvas.drawString(120, 703, "JOHN DOE")

    canvas.save()

test_report()

def test_03_draw():
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.units import inch
    c = Canvas('demo.pdf', pagesize=A4)
    c.translate(inch, inch)
    c.setFont("Helvetica", 14)
    c.setStrokeColorRGB(0.2, 0.5, 0.3)
    c.setFillColorRGB(1, 0, 1)
    c.line(0, 0, 0, 1.7 * inch)
    c.line(0, 0, 1 * inch, 0)
    c.rect(0.2 * inch, 0.2 * inch, 1 * inch, 1.5 * inch, fill=1)
    c.rotate(90)
    c.setFillColorRGB(0, 0, 0.77)
    c.drawString(0.3 * inch, -inch, "Hello World")
    c.showPage()
    c.save()

def test_06_fontsize():
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.units import inch
    from reportlab.lib.colors import red, magenta
    c = Canvas('demo.pdf', pagesize=A4)
    c.translate(inch, inch)
    c.setFont("Times-Roman", 20)
    c.setFillColor(red)
    c.saveState()
    c.drawCentredString(2.75 * inch, 2.5 * inch, "Font size excmples")
    c.setFillColor(magenta)
    size = 7
    x = 2.3 * inch
    y = 1.3 * inch
    for line in range(7):
        c.setFont("Helvetica", size)
        c.drawRightString(x, y, "%s points" % size)
        c.drawString(x, y, "test")
        y = y - size * 1.2
        size = size + 1.5
    c.restoreState()
    c.drawString(0, 0, "%s" % c.getAvailableFonts())
    c.showPage()
    c.save()


def test_04_canvasMethods():
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.units import inch
    c = Canvas('demo.pdf', pagesize=A4)
    c.translate(inch, inch)
    c.setFont("Helvetica", 14)
    c.setAuthor("JY.zenist.song")
    c.setTitle("Hello ReportLib")

    # c.drawString(inch,inch, "Hello World inch")

    for i in range(0, 10):
        c.drawString(i * inch, i * inch, "Hello World %s inch" % i)
        # c.drawString(1 * inch, 1 * inch, "Hello World 1 inch")
    c.showPage()
    c.save()

# test_04_canvasMethods()