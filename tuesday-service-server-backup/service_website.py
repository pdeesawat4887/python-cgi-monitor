#!/usr/bin/python

import time
import socket
import sys


class WebRequest:

    def __init__(self, destination, destination_port):
        self.get_status(destination, int(destination_port))

    def get_status(self, destination, destination_port):
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
        except Exception as error:
            print error
        finally:
            s.close()
            print stdout.format(status_final=status_final)


if __name__ == '__main__':
    example = WebRequest(sys.argv[1], sys.argv[2])
    # example = WebRequest('www.google.com', 80)
