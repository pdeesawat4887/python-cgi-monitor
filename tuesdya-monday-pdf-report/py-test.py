# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.platypus import Paragraph, Table, TableStyle
# from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
# from reportlab.lib import colors
#
# # bodytext  style used for wrapping  data on flowables
# styles = getSampleStyleSheet()
# styleN = styles["BodyText"]
# #used alignment if required
# styleN.alignment = TA_LEFT
#
# styleBH = styles["Normal"]
# styleBH.alignment = TA_CENTER
#
#
# hdescrpcion = Paragraph('''<b>descrpcion</b>''', styleBH)
# hpartida = Paragraph('''<b>partida</b>''', styleBH)
#
#
# descrpcion = Paragraph('long long long long long long long long long long long long long long long long long long long long line ', styleN)
# partida = Paragraph('1', styleN)
#
# data= [[hdescrpcion, hpartida],
#        [partida ,descrpcion]]
#
# table = Table(data)
#
# table.setStyle(TableStyle([
#                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
#                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
#                        ]))
#
# c = canvas.Canvas("a.pdf", pagesize=A4)
# table.wrapOn(c, 50, 50)
# table.drawOn(c, 100,600)
# c.save()
#
# import datetime
# import time
#
# date_string = '2018-10-29 16:00:00'
# format1 = '%Y-%m-%d %H:%M:%S'
# format2 = '%d-%b'
# print datetime.datetime.strptime(date_string, format1).strftime(format2)
#
# # import re
# #
# # shop="hello paswword"
# # # print list1
# # if re.findall(r'\b\w+\b', shop):
# #     print 'hello welcome'
#
# some_list = ["cond_ex[svc]", "cond_ex[isvc]", "select[]"]
# if any("cond_ex" in s for s in some_list):
#     print 'hello'


# log_table = {'PROBES': 'PROBE',
#                      'SERVICES': 'SERVICE',
#                      'DESTINATIONS': 'DEDSTINATION',
#                      'RUNNING_SERVICES': 'STATUS SERVICE',
#                      'RUNNING_DESTINATIONS': 'STATUS DESTINATION',
#                      'NOTIFY_TOKEN': 'LINE TOKEN',
#                      'NOTIFICATIONS': ' NOTIFICATION',
#                      'DASHBOARD': 'DASHBOARD'
#                      }
#
# hello = [i for i in range(1, len(log_table)+1)]
# print hello

# import sys
#
# class Python:
#
#     def __init__(self, fname, lname):
#         self.create_name(fname, lname)
#
#     def create_name(self,f, l):
#         print 'Hello {} {}'.format(l, f)
#
# if __name__ == '__main__':
#     exmaple = Python(sys.argv[1], sys.argv[2])

# probe_status = {
#             'Active':'Ready to work and still working now.',
#             'Idle':'Ready to work, but NOT working until change status to ACTIVE.',
#             'Inactive':'Cannot connected to probe longer than 1 hour.'}
#
# # print len(max(probe_status))
# probe_color = ['green', 'gray', 'red']
#
# tab = "    "
# flowables = []
# # self.flowables.append(Paragraph("<strong>COLLECT PROBE INFORMATION WITH STATUS:</strong>", style=self.sp_left))
# # map(lambda stat, val: flowables.append("{val}. {status}{tab}{desc}".format(val=val, status=str(stat).upper(), tab=tab, desc=probe_status[stat])), probe_status, [i for i in range(1, len(probe_status)+2)])
# # print [i for i in range(1, len(probe_status)+1)]
# # print flowables
#
#
# print '{message:{fill}{align}{width}}'.format(
#    message='Hi',
#    fill='*',
#    align='<',
#    width=16,
# )

import main.database as maria

db = maria.MySQLDatabase()

sql_svc = "SELECT `service_name` FROM SERVICES"

all_svc = map(lambda item: str(item[0]), db.select(sql_svc))

print all_svc

sql_start = "SELECT "