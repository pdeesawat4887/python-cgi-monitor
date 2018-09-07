#!/usr/bin/python

import main.distribution as worker

print "Content-Type: text/html\n"

if __name__ == '__main__':
    server = worker.Server()
    server.check_if_directory_is_empty()
