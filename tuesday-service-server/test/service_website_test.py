import time
import ssl
import socket


def website(destination, port):
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
        s_sock.sendall(request)
        resp = s_sock.recv(1024)
        print resp
        return 0, (time.time() - start) * 1000
    except socket.timeout:
        return 1, timeout
    except socket.error:
        return 2, None
    except Exception as error:
        print "ERROR:", error
    finally:
        s_sock.close()


HOST = 'www.google.com'
PORT = 80
print website(HOST, PORT)
