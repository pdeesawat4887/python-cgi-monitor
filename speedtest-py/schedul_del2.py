#!/Applications/XAMPP/xamppfiles/htdocs/python/python-cgi-monitor/venv/bin/python
# -*- coding: utf-8 -*-
# import json
# import sched, time
#
#
# def do_something():
#     print time.ctime(time.time())
#     # s.enter(300, 1, do_something, ())
#
#
# # s.enter(10, 1, do_something, (s,))
#
# # if __name__ == '__main__':
# #     s = sched.scheduler(time.time, time.sleep)
# #     do_something()
# #     s.run()
#
# # try:
# #     while True:
# #         do_something()
# #         time.sleep(60)
# # except KeyboardInterrupt:
# #     print('Manual break by user')
#
# # def loadFile(file):
# #         typeList = []
# #         with open(file) as f:
# #             for line in f:
# #                 key = line.strip().split(',')
# #                 typeList.append(key)
# #             return typeList
#
# # print loadFile('portstatus.csv')
# # serverList = []
# # setting = {}
# #
# # def loadFile(file):
# #     with open(file) as f:
# #         for line in f:
# #             key, value = line.strip().split('=')
# #             if 'server' in key:
# #                 serverList.append(value)
# #             else:
# #                 setting[key] = value
# #
# # loadFile('setting.txt')
# # print len(serverList)
# # print len(setting)
# #
# # print setting
# # print serverList
#
#
# def read(file='hosts.txt'):
#     with open(file, 'r') as temp_file:
#         text = temp_file.read()
#         host_list = text.split()
#         temp_file.close()
#     return host_list
#
#
# # print read()
#
# # import socket
# # import os
# #
# # url = 'facebook.com'
# #
# # ip_address = socket.gethostbyname(url)
# # ping_value = os.system("ping -c 1 -i 0.1 " + ip_address)
# # if ping_value == 0:
# #     ping_status = 'Active'
# # else:
# #     ping_status = 'Check server first'
# #
# # print ping_status
#
# # dict = {"a":"apple", "b":"banana"}
# #
# # dict['facebook.com'] = [200, 'OK', 'Active']
# #
# # word = 'facebook.com'
# #
# # word = word.split('.')
# #
# # print word[0]
#
# # import requests
# # protocol = ''
# # url = 'linkedin.com'
# # print protocol+url
# #
# # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36 OPR/53.0.2907.99'}
# # res_https = requests.get(protocol + url, headers=headers)
# # status = res_https.status_code
# # reason = res_https.reason
# # res_https.close()
# #
# # print status
# # print reason
#
# import httplib
# # import urllib
# #
# # response = urllib.urlopen('http://www.linkedin.com')
# # print 'RESPONSE:', response.getcode()
# # # print 'REASON: ', httplib.responses[response.getcode()]
# # # print 'URL     :', response.geturl()
# # #
# # # headers = response.info()
# # # print 'DATE    :', headers['date']
# # # print 'HEADERS :'
# # # print '---------'
# # # print headers
# #
# # data = response.read()
# # print 'LENGTH  :', len(data)
# # print 'DATA    :'
# # print '---------'
# # # print data
#
# # import smtplib
# #
# # receivers = []
# # email = {}
# #
# # with open('email.txt') as f:
# #     for line in f:
# #         key, value = line.strip().split('=')
# #         if 'receiver' in key:
# #             receivers.append(value)
# #         else:
# #             email[key] = value
# #
# #
# # gmail_user = email['sender']
# # print gmail_user
# # gmail_password = email['sender_pass']
# # print gmail_password
# #
# # # from_address = gmail_user
# # dest_address = ['ipacharapol@gmail.com']
# # subject = 'Good Morning Teacher ?'
# # body = 'How are you today ? What Happend to Monday ?'
# #
# # email_text = ''''From: {}\nTo: {}\nSubject: {}'''.format(gmail_user, dest_address, gmail_password, body)
# # # To: %s
# # # Subject: %s
# # #
# # # %s
# # # """ % (from_address, ", ".join(dest_address), subject, body)
# #
# # try:
# #     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
# #     # server = smtplib.SMTP_SSL('smtp-mail.outlook.com', '587')
# #     server.ehlo()
# #     server.login(gmail_user, gmail_password)
# #     server.sendmail(gmail_user, dest_address, email_text)
# #     server.quit()
# #
# #     print 'Email sent!'
# # except:
# #     print 'Something went wrong...'
#
# #
# # import re
# # import smtplib
# # import dns.resolver
# #
# # # Address used for SMTP MAIL FROM command
# # fromAddress = 'corn@bt.com'
# #
# # # Simple Regex for syntax checking
# # regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
# #
# # # Email address to verify
# # inputAddress = raw_input('Please enter the emailAddress to verify:')
# # addressToVerify = str(inputAddress)
# #
# # # Syntax check
# # match = re.match(regex, addressToVerify)
# # if match == None:
# #     print('Bad Syntax')
# #     raise ValueError('Bad Syntax')
# #
# # # Get domain for DNS lookup
# # splitAddress = addressToVerify.split('@')
# # domain = str(splitAddress[1])
# # print('Domain:', domain)
# #
# # # MX record lookup
# # records = dns.resolver.query(domain, 'MX')
# # mxRecord = records[0].exchange
# # mxRecord = str(mxRecord)
# # print 'mxRecord :', mxRecord
# #
# # # SMTP lib setup (use debug level for full output)
# # server = smtplib.SMTP()
# # server.set_debuglevel(0)
# #
# # # SMTP Conversation
# # server.connect(mxRecord)
# # server.helo(server.local_hostname)  ### server.local_hostname(Get local server hostname)
# # server.mail(fromAddress)
# # code, message = server.rcpt(str(addressToVerify))
# # server.quit()
# #
# # # print(code)
# # # print(message)
# #
# # # Assume SMTP response 250 is success
# # if code == 250:
# #     print('Success')
# # else:
# #     print('Bad')
#
# # """The first step is to create an SMTP object, each object is used for connection
# # with one server."""
# #
# # import smtplib
# # # server = smtplib.SMTP('smtp-mail.outlook.com', 587)
# # # server2 = smtplib.SMTP('smtp-mail.outlook.com', 587)
# #
# # server = smtplib.SMTP()
# # server.connect('mailhost.det.ameritech.net', 465)
# # # server.connect('smtp-mail.outlook.com', 587)
# #
# # #Next, log in to the server
# # code = server.helo()
# # server.close()
# # print code
#
# # server.quit()
#
# # code2 = int(server2.helo()[0])
# # server2.close()
#
# # if code == 250:
# #     print 'Success'
# #     print code
# # else:
# #     print 'Bad'
#
# # if code2 == 250:
# #     print 'Success'
# #     print code2
# # else:
# #     print 'Bad'
#
# # server.login("ipacharapol@gmail.com", "T")
# #
# # #Send the mail
# # msg = "Hello!" # The /n separates the message from the headers
# # server.sendmail("ipacharapol@gmail.com", "dololess72@gmail.com", msg)
#
#
# # import socket
# # def hostname_resolves(hostname):
# #     try:
# #         socket.gethostbyname(hostname)
# #         return 1
# #     except socket.error:
# #         return 0
#
# import smtplib
#
# # mail_server = {}
# # email = []
# # # with open('email.txt') as f:
# # #     for line in f:
# # #         key, value = line.strip().split(':')
# # #         email[key] = value
# #
# # with open('email.txt') as f:
# #     for line in f:
# #         try:
# #             key, value = line.strip().split(':')
# #             mail_server[key] = value
# #         except:
# #             emails = line.strip()
# #             email.append(emails)
# #
# # print email
# # print mail_server
#
# # server = smtplib.SMTP()
# # server.connect('smtp-mail.outlook.com', 587)
# # code = server.helo()
# # server.quit()
# #
# # if int(code[0]) == 250:
# #     result = 'Working'
# # else:
# #     result = 'Not Working'
# #
# # print result
# import smtplib
# import socket
#
#
# class SmtpService:
#     mail_server = {}
#     emails = []
#
#     def __init__(self):
#         self.read_server()
#         self.server = smtplib.SMTP(timeout=20)
#
#
#     def read_server(self, file="email.txt"):
#         with open(file) as f:
#             for line in f:
#                 try:
#                     key, value = line.strip().split(':')
#                     self.mail_server[key] = value
#                 except:
#                     email = line.strip()
#                     self.emails.append(email)
#
#     def connect_smtp_server(self, hostServer, port):
#         try:
#             self.server.connect(hostServer, port)
#             self.code = self.server.helo()
#         except Exception as e:
#             print e
#             print "\nCouldn't connect."
#
#     # def get_smtp_hello(self):
#     #     self.code = self.server.helo()
#
#     def get_smtp_code(self):
#
#         check = int(self.code[0])
#
#         if (200 <= check <= 299):
#             self.status = 'Working'
#         else:
#             self.status = 'Not Working'
#
#     def reset_smtp_connection(self):
#         self.server.quit()
#
#
# def main():
#     mail_test = SmtpService()
#     for server in mail_test.mail_server:
#         port = mail_test.mail_server[server]
#         jsonObj = json.dumps(mail_test.server.__dict__)
#         print(jsonObj)
#         try:
#             mail_test.connect_smtp_server(server, port)
#             mail_test.get_smtp_code()
#             mail_test.reset_smtp_connection()
#             print server, mail_test.status, mail_test.code
#         except Exception as e:
#             print e
#             print "\nCouldn't connect."
#
#
# if __name__ == '__main__':
#     main()
#
# # word = 'smtp.gmail.com'
# # word = word.replace('.', '-')
# #
# # print word
# # try:
# #     mylib = smtplib.SMTP('smtp-mail.outlook.com', 456)
# # except socket.error as e:
# #     print "could not connect"
#
# import json
#
# class Student:
#     def __init__(self, id, name, password):
#         self.id = id
#         self.name = name
#         self.password = password
#
# pythonObj = Student(1,'ashley','123456')
#
# # Convert Python object to JSON object
# jsonObj = json.dumps(pythonObj.__dict__)
# print(jsonObj)

# import NodeScript
#
# mail_server = {'smtp.airmail.net': ['587', '143', ''], 'smtp-mail.outlook.com': ['587', '993', '995'],
#                'smtp.live.com': ['587', '993', '995'], 'smtp.hughes.net': ['587', '993', '110'],
#                'smtp.gmail.com': ['587', '993', '995']}
#
# dict_data = {}
#
# email = NodeScript.EmailService()
#
# for i in mail_server:
#     print i


# import imaplib
# import poplib
# import smtplib
#
#
# class EmailService:
#     mail_server = {}
#     emails = []
#
#     # def __init__(self):
#     #     self.read_server()
#
#     def read_server(self, file="conf/email.txt"):
#         with open(file) as f:
#             for line in f:
#                 if not '#' in line:
#                     try:
#                         key, smtp, imap, pop3 = line.strip().split(':')
#                         self.mail_server[key] = [smtp, imap, pop3]
#                     except:
#                         if not '#' or ' ' in line:
#                             print "Please check configure file at line", line
#
#     def connect_smtp_server(self, hostServer, port):
#         try:
#             self.server = smtplib.SMTP()
#             self.server.connect(hostServer, port)
#             self.code = self.server.helo()
#         except Exception as e:
#             print e
#             print "\nCouldn't connect."
#
#     # def get_smtp_hello(self):
#     #     self.code = self.server.helo()
#
#     def get_smtp_status(self):
#
#         check = int(self.code[0])
#
#         if (200 <= check <= 299):
#             status = 'Working'
#         else:
#             status = 'Not Working'
#
#         return status
#
#     def connect_imap_server(self, hostServer, port):
#         try:
#             self.server = imaplib.IMAP4_SSL(hostServer, port)
#         except Exception as e:
#             self.server = imaplib.IMAP4(hostServer, port)
#
#     def get_imap_status(self):
#
#         check = self.server.welcome
#
#         if 'OK' in check:
#             status = 'Working'
#         else:
#             status = 'Not Working'
#
#         return status
#
#     def connect_pop_server(self, hostServer, port):
#         try:
#             self.server = poplib.POP3_SSL(hostServer)
#         except Exception as e:
#             self.server = poplib.POP3(hostServer)
#
#     def get_pop_status(self):
#
#         check = self.server.getwelcome()
#         self.server.quit()
#
#         if 'OK' in check:
#             status = 'Working'
#         else:
#             status = 'Not Working'
#
#         return status
#
#     def quit_smtp_connection(self):
#         self.server.quit()
#
#     def quit_pop_connection(self):
#         self.server.quit()
#
#     def quit_imap_connection(self):
#         self.server.close()
#
#     def connect_both(self, hostServer, port):
#         self.connect_smtp_server(hostServer, port)
#         self.connect_pop_server(hostServer)
#         self.connect_imap_server(hostServer, port)
#
#     def quit_both(self):
#         self.quit_smtp_connection()
#         self.quit_pop_connection()
#         self.quit_imap_connection()
#
#     ################## Special Function ######################
#
#     def choice_connection(self, func, hostServer, port):
#         connect_dict = {'smtp': self.connect_smtp_server, 'imap': self.connect_imap_server,
#                         'pop3': self.connect_pop_server}
#         get_data = {'smtp': self.get_smtp_status, 'imap': self.get_imap_status, 'pop3': self.get_pop_status}
#
#         connect_dict[func](hostServer, port)
#         data = get_data[func]()
#
#         return data
#
#     def choice_close(self, func):
#         close_dict = {'smtp': self.quit_smtp_connection, 'imap': self.quit_imap_connection,
#                       'pop3': self.quit_pop_connection}
#
#         close_dict[func]()
#
#
# import NodeScript
#
# firebase_con = NodeScript.FirebaseDatabase(url='https://pythontestcode.firebaseio.com/')
#
# mail_server = {'smtp.airmail.net': ['587', '143', ''], 'smtp-mail.outlook.com': ['587', '993', '995'],
#                'smtp.live.com': ['587', '993', '995'], 'smtp.hughes.net': ['587', '993', '110'],
#                'smtp.gmail.com': ['587', '993', '995']}
#
# protocols = ['smtp', 'imap', 'pop3']
#
# mail = EmailService()
#
# data = {}
#
# for i in range(len(protocols)):
#     for server in mail_server:
#         temp_server = str(server).replace('.', '-')
#         data[temp_server] = mail.choice_connection(protocols[i], server, mail_server[server][i])
#     firebase_con.put_data('test', 'mailServer/' + protocols[i], data)
#     data = {}


#### get file
# import urllib2
# response = urllib2.urlopen('https://firebasestorage.googleapis.com/v0/b/pythonwithfirebase-catma.appspot.com/o/ftp_talent.txt?alt=media&token=becbbd00-6492-426a-b964-1be4d1ce7336')
# html = response.read()

# import platform
# import sys
#
#
# def linux_distribution():
#     try:
#         return platform.linux_distribution()
#     except:
#         return "N/A"
#
#
# print("""Python version: %s
# dist: %s
# linux_distribution: %s
# system: %s
# machine: %s
# platform: %s
# uname: %s
# version: %s
# mac_ver: %s
# """ % (
#     sys.version.split('\n'),
#     str(platform.dist()),
#     linux_distribution(),
#     platform.system(),
#     platform.machine(),
#     platform.platform(),
#     platform.uname(),
#     platform.version(),
#     platform.mac_ver(),
# ))

# import sys
# #
# #
# # def get_platform():
# #     platforms = {
# #         'linux1': 'Linux',
# #         'linux2': 'Linux',
# #         'darwin': 'OS X',
# #         'win32': 'Windows'
# #     }
# #     if sys.platform not in platforms:
# #         return sys.platform
# #
# #     return platforms[sys.platform]
# #
# # print get_platform()

# import dns.name
#
# n = dns.name.from_text('www.dnspython.org')
# o = dns.name.from_text('dnspython.org')
# print n.is_subdomain(o)         # True
# print n.is_superdomain(o)       # False
# print n > o                     # True
# rel = n.relativize(o)           # rel is the relative name 'www'
# n2 = rel + o
# print n2 == n                   # True
# print n.labels                  # ('www', 'dnspython', 'org', '')

# import socket
# print socket.gethostbyname('localhost')
# print socket.gethostbyname('google.com')
#
# import subprocess
# try:
#     proc = (subprocess.check_output(['nslookup', 'google.com', '115.178.58.28']))
# except subprocess.CalledProcessError as err:
#     print(err)
#
# if 'google' in proc:
#     print('Yes')
# elif 'timed out' in proc:
#     print "Timeout"
#
# print proc
#
# ans = 'google.com'
# temp = ans.split('.')
# print temp[1]

import os
import time

# while True:
#     os.system('nslookup -ty=SOA google.com 110.78.191.20')
#     print '---------------------------------------------------------------------'
#     time.sleep(1)

# import time
# import subprocess
#
# while True:
#     try:
#         result = (subprocess.check_output(['nslookup', '-ty=SOA', 'google.com', '1.1.1.1']))
#     except subprocess.CalledProcessError as err:
#         result = err
#     print result
#     time.sleep(5)

# dict = {'win': {'a': 1234, 'b': 234}, 'loss': {'a': 'alpha', 'b': 'beta'}}
#
# for i in dict:
#     temp = dict[i]
#     print temp['a']

import firebase

# url='https://pythontestcode.firebaseio.com'
# connection = firebase.FirebaseApplication(url)
# connection.put('coding', '/', 'python')

# import urllib
# import httplib
# import socket
# import sys
# import struct
# import time
# import datetime
#
# now = datetime.datetime()
# print now

import time

time_cu = time.strftime('%H:%M:%S')
date_cu = time.strftime('%Y-%m-%d')
# print "Now:", now
# print "Time:", timee

# try:
#     con = MySQLdb.connect('hostname', 'username', 'userpass', \
#                           'tablename')
#     cur = con.cursor()
#     cur.execute("INSERT INTO foo (foo_name, foo_date) \
# 		VALUES (%s, %s)", (name_string, date_string))
#     cur.commit()

import mysql.connector

# sql = "INSERT INTO speedtestService VALUES (NULL, '"+node+"', '"+estination+"', '"+download+"', '"+upload+"', '"+ping+"', '"+date+"', '"+time"');'

# try:
#     connection = mysql.connector.connect(user='catma', password='root', host='localhost', database='service_db')
#     mycursor = connection.cursor()
# except Exception as error:
#     print 'Error:', error
#
#
# def __insert_data(node, destination, download, upload, ping, date, time):
#     sql = "INSERT INTO speedtestService VALUES (NULL, '" + node + "', '" + destination + "', '" + download + "', '" + upload + "', '" + ping + "', '" + date + "', '" + time + "');"
#     mycursor.execute(sql)
#     connection.commit()
#     print(mycursor.rowcount, "record inserted.")
#
#
# def __close_connection():
#     connection.close()
#
#
# def __sensor():
#     sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
#     val = [
#         ('Peter', 'Lowstreet 4'),
#         ('Amy', 'Apple st 652'),
#         ('Hannah', 'Mountain 21'),
#         ('Michael', 'Valley 345'),
#         ('Sandy', 'Ocean blvd 2'),
#         ('Betty', 'Green Grass 1'),
#         ('Richard', 'Sky st 331'),
#         ('Susan', 'One way 98'),
#         ('Vicky', 'Yellow Garden 2'),
#         ('Ben', 'Park Lane 38'),
#         ('William', 'Central st 954'),
#         ('Chuck', 'Main Road 989'),
#         ('Viola', 'Sideway 1633')
#     ]
#
#     mycursor.executemany(sql, val)
#
#     connection.commit()
#
#     print(mycursor.rowcount, "was inserted.")


# __insert_data('BKK', 'BKK', '999.99', '0.9999', '99.909', date_cu, time_cu)
# __sensor()
#
# value = []
#
#
# def insert(host, address):
#     data = (host, address)
#     value.append(data)
#
#
# insert('helloe', 'welcome')
# insert('applee', 'banana')
# insert('aaae', 'bbb')
# insert('leoe', 'tiger')
#

# print value

# def helper(list):
#     sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
#     mycursor.executemany(sql, list)
#     connection.commit()
#
#
# # helper(value)
#
#
# class MySQLDatabase:
#
#     def __init__(self):
#         self.create_connection()
#
#     def create_connection(self, user='catma', passwd='root', host='localhost', database='service_db'):
#         try:
#             self.connection = mysql.connector.connect(user=user, password=passwd, host=host, database=database)
#             self.mycursor = self.connection.cursor()
#         except Exception as error:
#             print 'Error:', error
#
#     def insert_data_dns_mail(self, table, node, destination, pp, status, date, time):
#         sql_syntax = "INSERT INTO {} VALUES (NULL, %s, %s, %s, %s, %s, %s)".format(table)
#         data = (node, destination, pp, status, date, time)
#         self.mycursor.execute(sql_syntax, data)
#         self.connection.commit()
#
#     def insert_data_speedtest(self, table, list_data):
#         sql_syntax = "INSERT INTO {} VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)".format(table)
#         self.mycursor.executemany(sql_syntax, list_data)
#         self.connection.commit()


#
# sqlDatabase = MySQLDatabase()
# time_cu = time.strftime('%H:%M:%S')
# date_cu = time.strftime('%Y-%m-%d')
# sqlDatabase.insert_data_dns_mail('dnsService', 'BKK_test', '127.0.0.1', '99.99', 'Working', date_cu, time_cu)
# sqlDatabase.insert_data_dns_mail('mailService', 'BKK_test', '127.0.0.1', 'pop3', 'Working', date_cu, time_cu)

# dee = ('hello', 'gohome'), ('banana')
# list= []
#
# list.extend(dee)
#
# print list

# fff = []
# with open('NodeScript.py') as f:
#     for line in f:
#         if not '#' in line:
#             fff.append(line)
# print fff.__len__()

# fight = 'a:a:a b:b:b'
# fight = fight.split()
# print fight[0]
# import requests


# def checkStatusHTTPS(self, url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36 OPR/53.0.2907.99'}
#     try:
#         res_https = requests.get(url, headers=headers)
#         self.status = res_https.status_code
#         self.reason = res_https.reason
#         res_https.close()
#     except Exception as ex:
#         self.status = 'Could not connect to page.'
#         self.reason = 'Could not connect to page.'

# from contextlib import contextmanager
# import sys, os
#
#
# @contextmanager
# def suppress_stdout():
#     with open(os.devnull, "w") as devnull:
#         old_stdout = sys.stdout
#         sys.stdout = devnull
#         try:
#             yield
#         finally:
#             sys.stdout = old_stdout
#
#
# print "You can see this"
# with suppress_stdout():
#     print "You cannot see this"
# print "And you can see this again"


# import os
# import subprocess
#
# with open(os.devnull, 'w') as DEVNULL:
#     try:
#         subprocess.check_call(
#             ['ping', '-c', '4', '192.168.91.41'],
#             stdout=DEVNULL,  # suppress output
#             stderr=DEVNULL
#         )
#         is_up = True
#     except subprocess.CalledProcessError:
#         is_up = False
#
# print is_up
# data = {}
#
# infile = open("conf/setting.txt", "r+")
#
# for line in infile:
#     if not line.strip():
#         continue
#     else:
#         key, value = line.strip().split('=')
#         data[key] = value
#
# infile.close()
#
# for num, i in enumerate(data):
#     print num,':', i , ':', data[i]
# line = "My name is Robin."
# with open('conf/speedtest_list.txt', 'r+') as f:
# file_data = f.read()
# for line in file_data:
#     f.write('#'+ line)

# infile = open("conf/speedtest_list.txt", 'r') # open file for reading
# outfile = open("conf/speedtest_list_re.txt","a") # open file for appending
#
# line = infile.readline()    # Invokes readline() method on file
# while line:
#    outfile.write("#"+line),    # trailing ',' omits newline character
#    line = infile.readline()
#
# infile.close()
# outfile.close()

# import socket
#
# ip_add = socket.gethostbyname("www.aliexpress.com")
# print ip_add

# import socket
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# print(s.getsockname()[0])
# s.close()

### get ip address

# import socket
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# print(s.getsockname()[0])
# s.close()

# import subprocess
# subprocess.call(['./example1.sh'])
import os
import time
from uuid import getnode as get_mac
import re

# import re, uuid
# mac = ''.join(re.findall('..', '%012x' % uuid.getnode()))
# # new_mac = mac.replace(':', '')
# eui64 = mac[0:6] + 'fffe' + mac[6:]
# print eui64
# eui64 = hex(int(eui64[0:2], 16) ^ 2)[2:].zfill(2) + eui64[2:]
# print eui64

import urlparse
import sys
import subprocess

# def my_platform():
#     platforms = {
#         'linux1': '-c',
#         'linux2': '-c',
#         'darwin': '-c',
#         'win32': '-n'
#     }
#     timeout = {
#         'linux1': '-t',
#         'linux2': '-t',
#         'darwin': '-t',
#         'win32': '-w'
#     }
#     if sys.platform not in platforms:
#         return sys.platform
#
#     return platforms[sys.platform], timeout[sys.platform]
#
#
# platform, timeout = my_platform()
# dest = 'google.com'
#
# with open(os.devnull, 'w') as DEVNULL:
#     try:
#         subprocess.check_call(
#             ['ping', platform, '1', timeout, '1',  dest],
#             # stdout=DEVNULL,
#             # stderr=DEVNULL
#         )
#         is_up = 0
#     except subprocess.CalledProcessError:
#         is_up = 1
#
# print is_up

# import subprocess
# import time
#
# uuu = '1.1.1.1'
#
# start = time.time()
# temp = ["ping", '-c', '1', 'google.com']
# # out = subprocess.check_output(temp)
# with open(os.devnull, 'w') as DEVNULL:
#     out = subprocess.check_output(temp)
#     print out
# end = time.time()
#
# # out = out.split('\n')
# #
# # for xxx in out:
# #     if 'time' in xxx:
# #         vvv = xxx.split()
# #         print vvv[6].split('=')[1]
# #
# # out = out.split('\n')
# # for i in out:
# #     if 'query time' in i.lower():
# #         print i
#
# print (end - start) * 1000

from platform import system as system_name  # Returns the system/OS name
from subprocess import call   as system_call  # Execute a shell command


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Ping command count option as function of OS
    param = '-n' if system_name().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', '-t', '1', host]

    # output = subprocess.check_output(command)
    result = 1
    response = 0
    try:
        output = subprocess.check_output(command).split()
        for element in output:
            if 'time' in element.lower():
                print element
                response = element.split('=')[1]
                result = 0
    except:
        result = 2
        response = 0

    return result, response

    # Pinging
    # return system_call(command) == 0

# print ping('google.com')

def dns(host, destination='https://google.com'):

    command = ['dig', '@'+host, destination]

    try:
        output = subprocess.check_output(command).split('\n')
        for i in output:
            if 'query time' in i.lower():
                print i.split()
    except:
        print "Error"

# dns('1.1.1.1')

def speedtest(server):
    import speedtest
    clinet = speedtest.Speedtest()
    # clinet.get_servers([server])
    clinet.get_best_server()
    clinet.download()
    clinet.upload()
    result = clinet.results.dict()
    return result
    # return result['ping'], result['download'], result['upload'], result['server']['name']

#
# test1111 = speedtest('19036')
#
# for i in test1111:
#     print 'Key :', i
#     print 'Value :', test1111[i]

# han = test1111['download']

def convert_byte(number_of_bytes):
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

    return number_of_bytes, unit



import bitmath
#
han = 2424708.6729394053
#
# print convert_byte(han)
#
# # test = bitmath.kb(bytes=han)
# # test2 = bitmath.kB(bits=han)
test1 = bitmath.MiB(bytes=han)
# test2 = bitmath.MiB(bits=han)
# test3 = bitmath.Mib(bytes=han)
# test4 = bitmath.Mib(bits=han)
# # test5 = bitmath.Kib(bits=han)
#
#
# # print test
# # print test2
# # print test3
# # print test4
# # print test5
print test1
# print test2
# print test3
# print test4
#
# import socket
# s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
# s.connect( ( "imap.gmail.com", 993) )
# s.send("EHLO") # GET??
# response = s.recv(8048)
# print response

import smtplib
import poplib
import imaplib

# connection = imaplib.IMAP4_SSL('smtp-mail.outlookf.com', 993)
# if 'ok' and 'ready' in connection.welcome:
#     print "YeSSSSSSSSSSSSSSSSSSS"


# import requests
#
# url = 'https://notify-api.line.me/api/notify'
# token = 'pyL4xY6ys303vg0bVnvd0DRco7UyILVo5dOXZGjBWD8'
# headers = {'content-type':'application/x-www-form-urlencoded', 'Authorization':'Bearer '+token}
#
# msg = '@บดินดุ๊ก testing time line notify working'
# r = requests.post(url, headers=headers, data= {'message':msg})
# print r.text

text = 'Minimum = 97ms, Maximum = 97ms, Average = 111197ms'
text = text.split()[-1][:-2:]
print text