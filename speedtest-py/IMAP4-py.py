import imaplib

mail_server = {}
emails = []
with open("conf/email_conf.txt") as f:
    for line in f:
        if not '#' in line:
            try:
                key, smtp, imap, pop3 = line.strip().split(':')
                mail_server[key] = [smtp, imap, pop3]
            except:
                if not '#' or ' ' in line:
                    print "Please check configure file at line", line

print mail_server
print emails

for i in mail_server:
    print i
    print mail_server[i][1]
    try:
        server = imaplib.IMAP4_SSL(i, mail_server[i][1])
    except Exception as e:
        server = imaplib.IMAP4(i, mail_server[i][1])
    check = server.welcome

    if 'OK' in check:
        status = 'Working'
    else:
        status = 'Not Working'

    print "Welcome: {}\nServer: {}\nStatus: {}".format(check, i, status)