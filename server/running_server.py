#!/usr/bin/python

import main.distribution as worker

if __name__ == '__main__':
    server = worker.Server()
    server.check_probe()
    availability, performance = server.get_warning_from_baseline()
    server.notify_me(data=availability, type='availability')
    server.notify_me(data=performance, type='performance')