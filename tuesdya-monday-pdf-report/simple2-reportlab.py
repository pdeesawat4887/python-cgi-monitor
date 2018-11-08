import datetime

from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

import main.database as mariadb
import time


def hello():
    doc = SimpleDocTemplate("hello_platypus72.pdf",
                            pagesize=A4,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=18,)
    # styles = getSampleStyleSheet()

    flowables = []

    sp_header = ParagraphStyle('parrafos',
                               alignment=TA_LEFT,
                               fontSize=18,
                               fontName="Times-Roman",
                               leading=50)

    sp_left = ParagraphStyle('parrafos',
                             alignment=TA_LEFT,
                             fontSize=12,
                             fontName="Times-Roman",
                             leading=20)

    # text = "Hello, I'm a Paragraph, alignment=TA_LEFT"
    # para = Paragraph(text, style=styles["Normal"])
    # para2 = Paragraph("How are you today ?", style=sp)

    # styles['small'] = ParagraphStyle(
    #     'small',
    #     parent=styles['default'],
    #     fontSize=8,
    #     leading=8,
    # )

    flowables.append(Paragraph("NETWORK ACTIVE MONITORING SYSTEM REPORT", style=sp_header))
    flowables.append(Paragraph("<strong>DATE:</strong>&nbsp;&nbsp;&nbsp;&nbsp;{date}".format(date=time.strftime('%d-%m-%Y %H:%M:%S')), style=sp_left))
    flowables.append(Paragraph("<strong>REPORT TOPIC:</strong>&nbsp;&nbsp;&nbsp;&nbsp;{topic}".format(topic='PROBE'), style=sp_left))
    # flowables.append(Paragraph('Text with default style', styles['default']))
    # flowables.append(Paragraph('Text with small style', styles['small']))

    doc.build(flowables)


def create_table():
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

    doc = SimpleDocTemplate("simple_table.pdf", pagesize=letter)
    # container for the 'Flowable' objects
    elements = []

    data = [['00', '01', '02', '03', '04'],
            ['10', '11', '12', '13', '14'],
            ['20', '21', '22', '23', '24'],
            ['30', '31', '32', '33', '34']]
    t = Table(data)
    t.setStyle(TableStyle([('BACKGROUND', (1, 1), (-2, -2), colors.green),
                           ('TEXTCOLOR', (0, 0), (1, -1), colors.red)]))
    elements.append(t)
    # write the document to disk
    doc.build(elements)

def get_probe():
    db = mariadb.MySQLDatabase()
    result = map(lambda item: list(item), db.select("SELECT `probe_name`, `ip_address`, `mac_address`,`last_updated`, `date_added`, DATEDIFF(`last_updated`,`date_added`) as uptime FROM PROBES WHERE `probe_status`=1 order by `probe_name` ASC;"))
    option = {
        'probe_name':'Probe Name',
        'ip_address': 'IP Address',
        'mac_address': 'MAC Address',
        'last_updated': 'Last Activity',
        'date_added': 'Installed Date',
        'uptime': 'Up time day(s)'
    }

    restict = [
        'uptime'
    ]

    description = [field[0] for field in db.mycursor.description]

    #### generate header table ####
    probe_description = [option[field] for field in description]
    result.insert(0, probe_description)
    ###############################

    #### generate table max column ####
    sql_max = "SELECT MAX(LENGTH(`{attribute}`)) FROM PROBES;"
    output = map(lambda item: (db.select(sql_max.format(attribute=item))[0][0])*5 if item not in restict else len(option[item])*4, description)

    return output, result



def table_2():
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

    doc = SimpleDocTemplate("simple_table.pdf", pagesize=letter)
    # container for the 'Flowable' objects
    elements = []

    # data = [['020C29FFFE612DDD', 'GNS3-Probe1', '192.168.10.100', '00:0c:29:61:2d:dd', 'Active'],
    #         ['A2999BFFFE046CED', 'MacOS', '192.168.51.102', 'a0:99:9b:04:6c:ed', 'Active'],
    #         ['A2999BFFFE046CED', 'MacOS', '192.168.51.102', 'a0:99:9b:04:6c:ed', 'Active']]

    length, data = get_probe()
    # colWidths = [column_width1, column_width2, None, column_width3, column_width4, None]
    t = Table(data, colWidths=length, rowHeights=19)
    # t.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
    #                        ('FONTSIZE', (0, 0), (-1, -1), 10),
    #                        ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
    #                        ('VALIGN', (0, 0), (0, -1), 'TOP'),
    #                        ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
    #                        ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
    #                        ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
    #                        ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
    #                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    #                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    #                        ]))
    row = len(data) - 1
    column = len(data[0]) - 1

    t.setStyle(TableStyle([('ALIGN', (0, 0), (column, row), 'CENTER'),
                           ('VALIGN', (0, 0), (column, row), 'MIDDLE'),
                           ('FONTSIZE', (0, 0), (column, row), 8),
                           ('INNERGRID', (0, 0), (column, row), 0.25, colors.black),
                           ('BOX', (0, 0), (column, row), 0.25, colors.black),
                           ('TEXTCOLOR', (0, 0), (column, row), colors.green)]))

    elements.append(t)
    # write the document to disk
    doc.build(elements)


def table_3():
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, inch
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table
    from reportlab.lib.styles import getSampleStyleSheet

    doc = SimpleDocTemplate("complex_cell_values.pdf", pagesize=letter)
    # container for the 'Flowable' objects
    elements = []

    styleSheet = getSampleStyleSheet()

    I = Image('replogo.gif')
    I.drawHeight = 1.25 * inch * I.drawHeight / I.drawWidth
    I.drawWidth = 1.25 * inch
    P0 = Paragraph('''
                   <b>A pa<font color=red>r</font>a<i>graph</i></b>
                   <super><font color=yellow>1</font></super>''',
                   styleSheet["BodyText"])
    P = Paragraph('''
        <para align=center spaceb=3>The <b>ReportLab Left
        <font color=red>Logo</font></b>
        Image</para>''',
                  styleSheet["BodyText"])
    data = [['A', 'B', 'C', P0, 'D'],
            ['00', '01', '02', [I, P], '04'],
            ['10', '11', '12', [P, I], '14'],
            ['20', '21', '22', '23', '24'],
            ['30', '31', '32', '33', '34']]

    t = Table(data, style=[('GRID', (1, 1), (-2, -2), 1, colors.green),
                           ('BOX', (0, 0), (1, -1), 2, colors.red),
                           ('LINEABOVE', (1, 2), (-2, 2), 1, colors.blue),
                           ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
                           ('BACKGROUND', (0, 0), (0, 1), colors.pink),
                           ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
                           ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                           ('BOX', (0, 0), (-1, -1), 2, colors.black),
                           ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                           ('VALIGN', (3, 0), (3, 0), 'BOTTOM'),
                           ('BACKGROUND', (3, 0), (3, 0), colors.limegreen),
                           ('BACKGROUND', (3, 1), (3, 1), colors.khaki),
                           ('ALIGN', (3, 1), (3, 1), 'CENTER'),
                           ('BACKGROUND', (3, 2), (3, 2), colors.beige),
                           ('ALIGN', (3, 2), (3, 2), 'LEFT'),
                           ])
    t._argW[3] = 1.5 * inch

    elements.append(t)
    # write the document to disk
    doc.build(elements)

class Report:

    def __init__(self):
        pass

    def get_probes(self, status):
        sql = "SELECT "

def timezone():
    from datetime import datetime
    ts = int("1541491064")
    # if you encounter a "year is out of range" error the timestamp
    # may be in milliseconds, try `ts /= 1000` in that case
    print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

def static_time(ms):
    # s = ms / 1000
    # m, s = divmod(s, 60)
    # h, m = divmod(m, 60)
    # d, h = divmod(h, 24)
    # return d, h, m, s
    return ms/60/1000

if __name__ == '__main__':
    # table_2()

    # timezone()

    # print static_time(3972121)

    # table_3()
    hello()
    # create_table()
    # get_probe()
