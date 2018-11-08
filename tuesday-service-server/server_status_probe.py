#!/usr/bin/python

import main.monitor_server as server

if __name__ == '__main__':
    probe_status = server.Server()
    probe_status.working_status_probe()