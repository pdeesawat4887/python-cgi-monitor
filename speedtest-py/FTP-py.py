import ftplib
import os
import socket

HOST = 'ftp.mozilla.org'
DIRN = 'pub/mozilla.org/webtools'
FILE = 'bugzilla-LATEST.tar.gz'

try:
    f = ftplib.FTP(HOST)
except (socket.error, socket.gaierror), e:
    print 'ERROR: cannot reach "%s"' % HOST
print '*** Connected to host "%s"' % HOST

try:
    f.login()
except ftplib.error_perm:
    print 'ERROR: cannot login anonymously'
    f.quit()
print '*** Logged in as "anonymous"'

try:
    f.cwd(DIRN)
except ftplib.error_perm:
    print 'ERROR: cannot CD to "%s"' % DIRN
    f.quit()
print '*** Changed to "%s" folder' % DIRN

try:
    f.retrbinary('RETR %s' % FILE,
                 open(FILE, 'wb').write)
except ftplib.error_perm:
    print 'ERROR: cannot read file "%s"' % FILE
    os.unlink(FILE)
else:
    print '*** Downloaded "%s" to CWD' % FILE
f.quit()
