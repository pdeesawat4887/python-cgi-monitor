#!/usr/bin/env python

import speedtest
import time
from firebase import firebase
import threading
import Utillity
import mysql_python


connect_mysql = mysql_python.MysqlPython('localhost', 'root', 'root', 'test-catma')

conditional_query = "host like %s "
result = connect_mysql.select('devices', conditional_query, 'download', 'upload', host='%o%')
print result
result2 = connect_mysql.insert('devices', host="BKK", download=99, upload=99, ping=99, runTime=999)

# import cgi

# form = cgi.FieldStorage()

# print 'Content-type: text/html\n\n'
# print '<!DOCTYPE html>'
# print '<html>'
# print '<head>'
# print '<meta charset="utf-8">'
# print '<meta name="viewport" content="width=device-width, initial-scale=1">'
# print '<title>AIT-CATMA</title>'
# print '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.1/css/bulma.min.css">'
# print '<script defer src="https://use.fontawesome.com/releases/v5.1.0/js/all.js"></script>'
# print '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>'
# print '<script defer src="https://use.fontawesome.com/releases/v5.1.0/js/all.js"></script>'
# print '</head>'
# print '<body>'
# print '<section class="section">'
# print '<div class="container">'

# servers = []


# def printit():
#   threading.Timer(5.0, printit).start()
#   print "Hello, World!"

# printit()
# for i in range(1):
#     print tools.gettime_ntp()
#     s = speedtest.Speedtest()
#     s.get_servers([19036])
#     s.get_best_server()
#     s.download()
#     s.upload()
#     res = s.results.dict()
#     print bytes_2_human_readable(res['download']), bytes_2_human_readable(res['upload'])
# print '<h1 class="title">'
# print 'Test SNMP at CATMA'
# print '</h1>'
# print '<p class="subtitle">'
# print 'My first website with <strong>Bulma</strong>!'
# print '</p>'
# print '<br><br>'

# print '''
# 				<button onclick="loadDoc()">Click here</button>
# '''
# print '<br><br>'
# print '<div class="column" id="table"> jjj </div>'
# def mariadb():
#     mariadb_connection = mysql.connector.connect(user='root', password='root', database='test-catma')
#     cursor = mariadb_connection.cursor()
#     cursor.execute("SELECT download, upload FROM devices")
#     for download, upload in cursor:
#     	print "Download: {}  Upload: {}".format(download, upload)

# mariadb()


def bytes_2_human_readable(number_of_bytes):
    if number_of_bytes < 0:
        raise ValueError("!!! number_of_bytes can't be smaller than 0 !!!")

    step_to_greater_unit = 1024.

    number_of_bytes = float(number_of_bytes)
    unit = 'bytes'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'KB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'MB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'GB'

    if (number_of_bytes / step_to_greater_unit) >= 1:
        number_of_bytes /= step_to_greater_unit
        unit = 'TB'

    precision = 1
    number_of_bytes = round(number_of_bytes, precision)

    return str(number_of_bytes) + " " + unit


def test(server, timer):
    start_time = time.time()
    s = speedtest.Speedtest()
    s.get_servers([server])
    s.get_best_server()
    s.download()
    s.upload()
    res = s.results.dict()
    return res["download"], res["upload"], res["ping"], time.time() - start_time, timer


def connection(root, node, data):
    connection = firebase.FirebaseApplication(
        'https://pythonwithfirebase-catma.firebaseio.com')
    connection.put(root, node, data)


def main(node, destination, server, timer):
    # write to csv
    # with open(destination + '.csv', 'a') as f:
    # f.write('download,upload,ping,time\n')
    # print('Making test #{}'.format(1))
    d, u, p, exet, st = test(server, timer)
    # f.write('{},{},{},{},{}\n'.format(timer, d, u, p, exet, st))
    connection('speedtest', node + '/' + destination,
               {'download': bytes_2_human_readable(d), 'upload': bytes_2_human_readable(u), 'ping': p, 'time': exet,
                'ping time': st})
    print '''<script> console.log('finish')</script>'''


tools = Utillity.Utilities()
# print tools.gettime_ntp()
node = 'BKK'
destination = ['Singapore', 'Hong Kong', 'CAT Telecom']
server = [3914, 19036, 4347]
for dest in range(3):
    main(node, destination[dest], server[dest], tools.gettime_ntp())
# print tools.gettime_ntp()
# pretty write to txt file
# with open('file.txt', 'w') as f:
#     for i in range(3):
#         print('Making test #{}'.format(i + 1))
#         d, u, p = test()
#         f.write('Test #{}\n'.format(i + 1))
#         f.write('Download: {:.2f} Kb/s\n'.format(d / 1024))
#         f.write('Upload: {:.2f} Kb/s\n'.format(u / 1024))
#         f.write('Ping: {}\n'.format(p))
# simply print in needed format if you want to use pipe-style: python script.py > file
# for i in range(3):
#     d, u, p = test()
#     print('Test #{}\n'.format(i + 1))
#     print('Download: {:.2f} Kb/s\n'.format(d / 1024))
#     print('Upload: {:.2f} Kb/s\n'.format(u / 1024))
#     print('Ping: {}\n'.format(p))


# main('BKK', 'Singapore', tester.gettime_ntp())


# print '</div>'
# print '</section>'
# print '</body>'
# print '</html>'

# print '''
# <script>
# function loadDoc() {
#   var xhttp = new XMLHttpRequest();
#   xhttp.onreadystatechange = function() {
# 	if (this.readyState == 4 && this.status == 200) {
# 	  document.getElementById("table").innerHTML =
# 	  this.responseText;
# 	}
#   };
#   xhttp.open("GET", "test-back.py", true);
#   xhttp.send();
# }
# </script>
# '''

# threads = []
# for i in range(3):
#   tester = Utillity.Utilities()
#   tester.gettime_ntp()
#     t = threading.Thread(target=main, args=('BKK', 'Singapore', 3914, tester.gettime_ntp(),))
#     threads.append(t)
#     t.start()

# tester = Utillity.Utilities()
# for i in range(3):
#     main(node[i], destination[i], server[i], tester.gettime_ntp())

# print tester.gettime_ntp()

# print 'success'

# if __name__ == '__main__':
#     try:
#         tester = Utillity.Utilities()
#         tester.gettime_ntp()
#         thread.start_new_thread(
#             main, ('BKK', 'Singapore', tester.gettime_ntp()))
#         # thread.start_new_thread(
#         #     main, ('BKK', 'Hong Kong', tester.gettime_ntp()))
#         # thread.start_new_thread(
#         #     main, ('BKK', 'KMITL',  tester.gettime_ntp()))
#     except:
#         print "Error: unable to start thread"
#     while 1:
#         pass

# print 'Content-type: text/html\n\n'
# print '<!DOCTYPE html>'
# print '<html>'
# print '<head>'
# print '<meta charset="utf-8">'
# print '<meta name="viewport" content="width=device-width, initial-scale=1">'
# print '<title>AIT-CATMA</title>'
# print '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.1/css/bulma.min.css">'
# print '<script defer src="https://use.fontawesome.com/releases/v5.1.0/js/all.js"></script>'
# print '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>'
# print '<script defer
# src="https://use.fontawesome.com/releases/v5.1.0/js/all.js"></script>'
# print '</head>'
# print '<body>'
# print '<section class="section">'
# print '<div class="container">'

# servers = []


# def printit():
#   threading.Timer(5.0, printit).start()
#   print "Hello, World!"

# printit()
# for i in range(1):
#     print tools.gettime_ntp()
#     s = speedtest.Speedtest()
#     s.get_servers([19036])
#     s.get_best_server()
#     s.download()
#     s.upload()
#     res = s.results.dict()
#     print bytes_2_human_readable(res['download']), bytes_2_human_readable(res['upload'])
# # print '<h1 class="title">'
# print 'Test SNMP at CATMA'
# print '</h1>'
# print '<p class="subtitle">'
# print 'My first website with <strong>Bulma</strong>!'
# print '</p>'
# print '<br><br>'

# print '''
#                 <button onclick="loadDoc()">Click here</button>
# '''
# print '<br><br>'
# print '<div class="column" id="table"> jjj </div>'

# print '</div>'
# print '</section>'
# print '</body>'
# print '</html>'

# print '''
# <script>
# function loadDoc() {
#   var xhttp = new XMLHttpRequest();
#   xhttp.onreadystatechange = function() {
#     if (this.readyState == 4 && this.status == 200) {
#       document.getElementById("table").innerHTML =
#       this.responseText;
#     }
#   };
#   xhttp.open("GET", "test-back.py", true);
#   xhttp.send();
# }
# </script>
# '''
