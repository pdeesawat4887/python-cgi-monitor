#!/usr/bin/python

import socket
import re
import uuid

import database


class Probe:

    def __init__(self):
        self.mac_address = self.get_mac_address()
        self.db = database.MySQLDatabase()
        self.ip = self.get_ip()
        self.id = self.get_probe_id(self.mac_address)
        # self.set_probe()

    def set_probe(self):
        query_sql = "SELECT * FROM probe WHERE probe_id='{}'".format(self.id)
        result = self.db.select(query_sql)
        if result.__len__() == 1:
            print """UPDATE"""
            sql = "UPDATE probe SET ip_address='{}', mac_address='{}', status='{}', path=NULL, last_change=NOW()".format(
                self.ip, self.mac_address, 0)
        else:
            print """INSERT NEW"""
            sql = "INSERT INTO probe VALUES ('{}', NULL, '{}', '{}', '{}', NULL, NOW())".format(
                self.id, self.ip, self.mac_address, 0)

        self.db.mycursor.execute(sql)
        self.db.connection.commit()

    def get_mac_address(self):
        ''' Get MAC Address '''
        mac = ''.join(re.findall('..', '%012x' % uuid.getnode()))
        mac_address = ':'.join(mac[i:i + 2] for i in range(0, 12, 2))
        return mac_address

    def get_ip(self):
        ''' Get probe ip from source ip contain in socket that connect to 10.255.255.255 '''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def get_probe_id(self, mac):
        ''' Create EUI64 from Mac Address for probe_id to collect in database '''
        mac = mac.replace(':', '')
        eui64 = mac[0:6] + 'fffe' + mac[6:]
        eui64 = hex(int(eui64[0:2], 16) ^ 2)[2:].zfill(2) + eui64[2:]
        return eui64

    def get_active_service(self):
        query_sql = """select service.service_id, service.file_name, service.command 
        from service inner join running_service on service.service_id=running_service.service_id 
        where running_service.running=0 and probe_id='{}'""".format(self.id)
        result = self.db.select(query_sql)
        print result


if __name__ == '__main__':
    probeMac = Probe()
    print probeMac.ip
    print probeMac.mac_address
    print probeMac.id
