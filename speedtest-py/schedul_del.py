import sched, time


def do_something():
    print time.ctime(time.time())
    # s.enter(300, 1, do_something, ())


# s.enter(10, 1, do_something, (s,))

# if __name__ == '__main__':
#     s = sched.scheduler(time.time, time.sleep)
#     do_something()
#     s.run()

# try:
#     while True:
#         do_something()
#         time.sleep(60)
# except KeyboardInterrupt:
#     print('Manual break by user')

# def loadFile(file):
#         typeList = []
#         with open(file) as f:
#             for line in f:
#                 key = line.strip().split(',')
#                 typeList.append(key)
#             return typeList

# print loadFile('portstatus.csv')
# serverList = []
# setting = {}
#
# def loadFile(file):
#     with open(file) as f:
#         for line in f:
#             key, value = line.strip().split('=')
#             if 'server' in key:
#                 serverList.append(value)
#             else:
#                 setting[key] = value
#
# loadFile('setting.txt')
# print len(serverList)
# print len(setting)
#
# print setting
# print serverList


def read(file='hosts.txt'):
    with open(file, 'r') as temp_file:
        text = temp_file.read()
        host_list = text.split()
        temp_file.close()
    return host_list


# print read()

# import socket
# import os
#
# url = 'facebook.com'
#
# ip_address = socket.gethostbyname(url)
# ping_value = os.system("ping -c 1 -i 0.1 " + ip_address)
# if ping_value == 0:
#     ping_status = 'Active'
# else:
#     ping_status = 'Check server first'
#
# print ping_status

# dict = {"a":"apple", "b":"banana"}
#
# dict['facebook.com'] = [200, 'OK', 'Active']
#
# word = 'facebook.com'
#
# word = word.split('.')
#
# print word[0]

# import requests
# protocol = ''
# url = 'linkedin.com'
# print protocol+url
#
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36 OPR/53.0.2907.99'}
# res_https = requests.get(protocol + url, headers=headers)
# status = res_https.status_code
# reason = res_https.reason
# res_https.close()
#
# print status
# print reason

import httplib
# import urllib
#
# response = urllib.urlopen('http://www.linkedin.com')
# print 'RESPONSE:', response.getcode()
# # print 'REASON: ', httplib.responses[response.getcode()]
# # print 'URL     :', response.geturl()
# #
# # headers = response.info()
# # print 'DATE    :', headers['date']
# # print 'HEADERS :'
# # print '---------'
# # print headers
#
# data = response.read()
# print 'LENGTH  :', len(data)
# print 'DATA    :'
# print '---------'
# # print data

# import smtplib
#
# receivers = []
# email = {}
#
# with open('email.txt') as f:
#     for line in f:
#         key, value = line.strip().split('=')
#         if 'receiver' in key:
#             receivers.append(value)
#         else:
#             email[key] = value
#
#
# gmail_user = email['sender']
# print gmail_user
# gmail_password = email['sender_pass']
# print gmail_password
#
# # from_address = gmail_user
# dest_address = ['ipacharapol@gmail.com']
# subject = 'Good Morning Teacher ?'
# body = 'How are you today ? What Happend to Monday ?'
#
# email_text = ''''From: {}\nTo: {}\nSubject: {}'''.format(gmail_user, dest_address, gmail_password, body)
# # To: %s
# # Subject: %s
# #
# # %s
# # """ % (from_address, ", ".join(dest_address), subject, body)
#
# try:
#     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#     # server = smtplib.SMTP_SSL('smtp-mail.outlook.com', '587')
#     server.ehlo()
#     server.login(gmail_user, gmail_password)
#     server.sendmail(gmail_user, dest_address, email_text)
#     server.quit()
#
#     print 'Email sent!'
# except:
#     print 'Something went wrong...'


import re
import smtplib
import dns.resolver

# Address used for SMTP MAIL FROM command
fromAddress = 'corn@bt.com'

# Simple Regex for syntax checking
regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

# Email address to verify
inputAddress = raw_input('Please enter the emailAddress to verify:')
addressToVerify = str(inputAddress)

# Syntax check
match = re.match(regex, addressToVerify)
if match == None:
    print('Bad Syntax')
    raise ValueError('Bad Syntax')

# Get domain for DNS lookup
splitAddress = addressToVerify.split('@')
domain = str(splitAddress[1])
print('Domain:', domain)

# MX record lookup
records = dns.resolver.query(domain, 'MX')
mxRecord = records[0].exchange
mxRecord = str(mxRecord)
print 'mxRecord :', mxRecord

# SMTP lib setup (use debug level for full output)
server = smtplib.SMTP()
server.set_debuglevel(0)

# SMTP Conversation
server.connect(mxRecord)
server.helo(server.local_hostname)  ### server.local_hostname(Get local server hostname)
server.mail(fromAddress)
code, message = server.rcpt(str(addressToVerify))
server.quit()

# print(code)
# print(message)

# Assume SMTP response 250 is success
if code == 250:
    print('Success')
else:
    print('Bad')

# """The first step is to create an SMTP object, each object is used for connection
# with one server."""
#
# import smtplib
# server = smtplib.SMTP('smtp-mail.outlook.com', 587)
# server2 = smtplib.SMTP('smtp-mail.outlook.com', 587)
#
# #Next, log in to the server
# code = server.helo('Pacharapol')
# server.close()
# server.quit()
#
# code2 = int(server2.helo()[0])
# server2.close()
#
# # if code == 250:
# #     print 'Success'
# #     print code
# # else:
# #     print 'Bad'
# print code
#
# if code2 == 250:
#     print 'Success'
#     print code2
# else:
#     print 'Bad'

# server.login("ipacharapol@gmail.com", "T")
#
# #Send the mail
# msg = "Hello!" # The /n separates the message from the headers
# server.sendmail("ipacharapol@gmail.com", "dololess72@gmail.com", msg)


import socket
def hostname_resolves(hostname):
    try:
        socket.gethostbyname(hostname)
        return 1
    except socket.error:
        return 0
