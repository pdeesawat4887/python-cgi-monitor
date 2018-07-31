import imaplib

mail_server = {}
emails = []
with open("conf/email.txt") as f:
    for line in f:
        try:
            key, value = line.strip().split(':')
            mail_server[key] = value
        except:
            email = line.strip()
            emails.append(email)

print mail_server

for i in mail_server:
    print i
    try:
        server = imaplib.IMAP4_SSL(i, 993)
    except Exception as e:
        server = imaplib.IMAP4_SSL(i, 993)
    check = server.welcome

    if 'OK' in check:
        status = 'OK'
    else:
        status = 'Cannot connect'

    print "Welcome: {}\nServer: {}\nStatus: {}".format(check, i, status)