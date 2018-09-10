#!/usr/bin/python

import __Database__ as mariadb
import socket
import re, uuid


class Probe(mariadb.MySQLDatabase):

    def __init__(self):
        mariadb.MySQLDatabase.__init__(self)
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
        eui64 = self.mac[0:6] + 'fffe' + self.mac[6:]
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
        self.mac = ''.join(re.findall('..', '%012x' % uuid.getnode()))
        self.mac_address = ':'.join(self.mac[i:i + 2] for i in range(0, 12, 2))
