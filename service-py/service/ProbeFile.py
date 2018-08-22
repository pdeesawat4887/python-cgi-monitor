#!/usr/bin/python

import Database
import socket
import re, uuid

class Probe(Database.MySQLDatabase):
    setting = {}

    def __init__(self):
        Database.MySQLDatabase.__init__(self)
        self.prepare_setting()
        self.prepare_probe()

    def prepare_setting(self, file='python-cgi-monitor/service-py/conf/configure'):
        ''' Open and read configure file to prepare for probe and service test '''
        infile = open(file, "r")
        for line in infile:
            if not line.strip():
                continue
            else:
                if not '#' in line:
                    key, value = line.strip().split('=')
                    self.setting[key] = value
        infile.close()

    def prepare_probe(self):
        ''' Set probe configure use for store in database '''
        self.get_mac_address()
        self.get_ip()
        self.get_name()
        self.query_probe(id=self.id, name=self.name, ip=self.ip, mac_address=self.mac_address)

    def get_mac_address(self):
        ''' Get MAC Address and create EUI64 for probe_id to collect in database '''
        mac = ''.join(re.findall('..', '%012x' % uuid.getnode()))
        eui64 = mac[0:6] + 'fffe' + mac[6:]
        eui64 = hex(int(eui64[0:2], 16) ^ 2)[2:].zfill(2) + eui64[2:]
        self.mac_address = mac
        self.id = eui64

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

    def get_name(self):
        ''' Set probe_name from configuration file store at /conf/configure '''
        self.name = self.setting['probe_name']
        # return self.setting['node_name']

    # def query_start_service(self, probe_id, service_id):
    #     query_sql = "SELECT setting FROM setting WHERE probe_id='{}' and service_id='{}'".format(self.id, service_id)
    #     self.mycursor.execute(query_sql)
    #     my_result = self.mycursor.fetchone()
    #     print my_result
    #     return my_result[0]

if __name__ == '__main__':
    probe = Probe()