#!/usr/bin/python

import main.service as service
import socket
import time


class Imap(service):

    def get_status(self, destination, port):
        timeout = 1
        request = "tag logout"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        start = time.time()
        s.settimeout(timeout)
        try:
            s.connect((destination, port))
            s.send(request)
            # resp = s.recv(1024)
            # print resp
            return 0, (time.time() - start) * 1000
        except socket.timeout:
            return 1, timeout
        except Exception as e:
            return 2, timeout
        finally:
            s.close()

if __name__ == '__main__':
    dest = 'imap.gmail.com'
    port = 993
    xxx = Imap()
    result = xxx.get_status(dest, port)
    print result