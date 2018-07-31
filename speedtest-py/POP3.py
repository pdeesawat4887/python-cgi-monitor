import poplib
import string
import random
import StringIO
import rfc822

# # def readMail():
# SERVER = "imap.airmail.net"
# # USER = "ipacharapol@gmail.com"
# # PASSWORD = "Thailand4887"
#
# # connect to server
# try:
#     server = poplib.POP3_SSL(SERVER)
# except Exception as e:
#     server = poplib.POP3(SERVER)
# print server.getwelcome()

mail_server = {}
emails = []
with open("email.txt") as f:
    for line in f:
        try:
            key, value = line.strip().split(':')
            mail_server[key] = value
        except:
            email = line.strip()
            emails.append(email)

print mail_server

for i in mail_server:
    try:
        server = poplib.POP3_SSL(i)
    except Exception as e:
        server = poplib.POP3(i)
    check = server.getwelcome()

    if '+OK' in check:
        status = 'OK'
    else:
        status = 'Cannot connect'

    print i, status
#
# for i in mail_server:
#     server = poplib.POP3(i)
#     print i, server.getwelcome()
# # login
# server.user(USER)
# server.pass_(PASSWORD)
#
# # list items on server
# resp, items, octets = server.list()
#
# for i in range(0, 10):
#     id, size = string.split(items[i])
#     resp, text, octets = server.retr(id)
#
# text = string.join(text, "\n")
# file = StringIO.StringIO(text)
#
# message = rfc822.Message(file)
#
# for k, v in message.items():
#     print k, "=", v

# readMail()
