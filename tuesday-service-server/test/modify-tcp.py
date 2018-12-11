import socket
import time

def tcp_work(destination, destination_port):
    stdout = "status={status_final}"

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print "socket creation failed with error %s" % (err)
        status_final = 3

    regex = {'http://': '', 'https://': ''}
    destination = reduce(lambda a, kv: a.replace(*kv), regex.iteritems(), destination)

    try:
        host_ip = socket.gethostbyname(destination)
    except socket.gaierror:
        status_final = 3

    s.settimeout(1)

    try:
        start_time = time.time()
        s.connect((host_ip, destination_port))
        end_time = time.time()
        status_final = 1
        stdout += ", rtt={rtt}".format(rtt=(end_time - start_time) * 1000)
    except socket.timeout:
        status_final = 2
    except Exception:
        status_final = 3
    finally:
        s.close()
        return stdout.format(status_final=status_final)

print tcp_work('www.hotmil.com', 443)