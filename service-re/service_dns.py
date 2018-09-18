#!/usr/bin/python

import main.service as service_cl
import dns.resolver
import time
import sys


class DnsSolution(service_cl.Service):

    def get_record(self, dns_server):
        DOMAIN = 'stackoverflow.com'
        TIMEOUT = 1
        LIFETIME = 1

        list_record = []

        resolver = dns.resolver.Resolver()
        resolver.timeout = TIMEOUT
        resolver.lifetime = LIFETIME
        resolver.nameservers = [dns_server]
        time_start = time.time()
        result = resolver.query(DOMAIN, 'A')
        time_end = time.time()

        for item in result:
            list_record.append(item.to_text())

        return list_record, (time_end - time_start) * 1000

    def get_status(self, destination, port):
        try:
            master, time_master = self.get_record('8.8.8.8')
            tester, time_tester = self.get_record(destination)
        except:
            return 2, None, None, None

        check = set(master).intersection(tester).__len__()

        if (master.__len__() - 1) <= check and time_tester <= 100:
            return 0, time_tester, None, None
        elif (master.__len__() - 1) <= check and time_tester > 100 and time_tester <= 1000:
            return 1, time_tester, None, None
        else:
            return 2, None, None, None

if __name__ == '__main__':
    example = DnsSolution(sys.argv[1], sys.argv[2], sys.argv[3])
