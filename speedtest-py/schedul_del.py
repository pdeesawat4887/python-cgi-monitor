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

import smtplib

receivers = []
email = {}

with open('email.txt') as f:
    for line in f:
        key, value = line.strip().split('=')
        if 'receiver' in key:
            receivers.append(value)
        else:
            email[key] = value


gmail_user = email['sender']
print gmail_user
gmail_password = email['sender_pass']
print gmail_password

# from_address = gmail_user
dest_address = ['ipacharapol@gmail.com']
subject = 'Good Morning Teacher ?'
body = 'How are you today ? What Happend to Monday ?'

email_text = ''''From: {}\nTo: {}\nSubject: {}'''.format(gmail_user, dest_address, gmail_password, body)
# To: %s
# Subject: %s
#
# %s
# """ % (from_address, ", ".join(dest_address), subject, body)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # server = smtplib.SMTP_SSL('smtp-mail.outlook.com', '587')
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, dest_address, email_text)
    server.quit()

    print 'Email sent!'
except:
    print 'Something went wrong...'