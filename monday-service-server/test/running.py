import subprocess
import os

import sys
# sys.argv = ['10', 'hello it me']
# execfile('cookie.py')

#
# """
# A simple example of using Python sockets for a client HTTPS connection.
# """
#
# import ssl
# import socket
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(('github.com', 443))
# s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
# s.sendall("GET / HTTP/1.1\r\nHost: github.com\r\nConnection: close\r\n\r\n")
#
# while True:
#
#     new = s.recv(4096)
#     if not new:
#       s.close()
#       break
#     print new
import sys
import time
import subprocess
destination = 'google.com'
param = '-n' if sys.platform.lower() == 'windows' else '-c'
command = ['ping', param, '1', destination]
t_start = time.time()
output = subprocess.check_output(command).split('\n')
t_end = time.time()

print output
print t_end-t_start
print (t_end-t_start)/4
print 8/4