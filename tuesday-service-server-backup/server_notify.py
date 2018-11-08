#!/usr/bin/python

import main.monitor_server as server

if __name__ == '__main__':
    notify_server = server.Server()
    notify_server.working_notify()