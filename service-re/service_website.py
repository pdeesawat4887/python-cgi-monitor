#!/usr/bin/python

import main.service as service_cl
import time
import socket
import ssl
import sys


class WebRequest(service_cl.Service):

    def get_status(self, destination, port):
        timeout = 1
        ssl_port = [443]
        request = b"GET / HTTP/1.1\nHost: {}\n\n".format(destination)
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)

        if port in ssl_port:
            s_sock = context.wrap_socket(s, server_hostname=destination)
        else:
            s_sock = s
        try:
            start = time.time()
            s_sock.connect((destination, port))
            s_sock.send(request)
            resp = s_sock.recv(1024)
            return 0, (time.time() - start) * 1000, None, None
        except socket.timeout:
            return 1, timeout, None, None
        except socket.error:
            return 2, None, None, None
        except Exception as error:
            print "ERROR:", error
        finally:
            s_sock.close()


if __name__ == '__main__':
    example = WebRequest(sys.argv[1], sys.argv[2], sys.argv[3])
