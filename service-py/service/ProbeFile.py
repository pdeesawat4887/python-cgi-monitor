#!/usr/bin/python

import Database
import socket
import re, uuid
import threading
import os


class Probe(Database.MySQLDatabase):

    def __init__(self):
        Database.MySQLDatabase.__init__(self)
        self.prepare_probe()

    def prepare_probe(self):
        ''' Set probe configure use for store in database '''
        self.get_mac_address()
        self.get_probe_id()
        self.get_ip()
        self.get_probe_name()
        self.set_probe(id=self.id, name=self.name, ip=self.ip, mac_address=self.mac_address)

    def get_probe_id(self):
        ''' Create EUI64 from Mac Address for probe_id to collect in database '''
        eui64 = self.mac_address[0:6] + 'fffe' + self.mac_address[6:]
        eui64 = hex(int(eui64[0:2], 16) ^ 2)[2:].zfill(2) + eui64[2:]
        self.id = eui64

    def get_probe_name(self):
        ''' Set probe_name from configuration file store at conf/configure '''
        self.name = self.setting['probe_name']

    def get_ip(self):
        ''' Get probe ip from source ip contain in socket that connect to 8.8.8.8 '''
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
        except:
            ip_address = '127.0.0.1'
        self.ip = ip_address

    def get_mac_address(self):
        ''' Get MAC Address from probe '''
        mac = ''.join(re.findall('..', '%012x' % uuid.getnode()))
        self.mac_address = mac


class Command(Probe):
    def __init__(self):
        Probe.__init__(self)
        self.read_file_dictionary()
        self.workon()

    def read_file_dictionary(self):
        line = open(self.path + '/conf/dictionary', 'r').read()
        # line = open('conf/dictionary', 'r').read()
        self.mapping_service = eval(line)

    def get_service_active(self):
        list_service = []
        temp_service = self.query_active_service(probe_id=self.id)

        for service_id in temp_service:
            list_service.append(service_id[0])
        return list_service

    def workon(self):
        outlock = threading.Lock()

        list_service = self.get_service_active()

        threads = []
        for service in list_service:
            t = threading.Thread(target=self.work_service, args=(service,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    def work_service(self, service_id):
        outlock = threading.Lock()

        command = "python " + self.path + '/' + self.mapping_service[int(service_id)]

        print command

        os.system(command)


if __name__ == '__main__':
    running = Command()
