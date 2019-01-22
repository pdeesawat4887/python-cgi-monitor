#!/usr/bin/python

import socket  # for socket
import sys

class Mum:

    def __init__(self, url, port):
        self.open_tcp_connection(url, port)

    def open_tcp_connection(self, url, port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # print "Socket successfully created"
        except socket.error as err:
            print "socket creation failed with error %s" % (err)

        s.settimeout(1)
        regex = {'http://': '', 'https://': ''}
        url = reduce(lambda a, kv: a.replace(*kv), regex.iteritems(), url)

        try:
            host_ip = socket.gethostbyname(url)
            # host_ip = "8.8.8.8"
        except socket.gaierror:
            # this means could not resolve the host
            print "there was an error resolving the host"
            return None

        # connecting to the server
        try:
            s.connect((host_ip, port))
        except socket.timeout:
            return None

        print "the socket has successfully connected to %s on port == %s" % (host_ip, port)
        s.close()

if __name__ == '__main__':
    iron = Mum('google.com', 443)