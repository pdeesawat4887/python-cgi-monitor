#!/usr/bin/python

import socket
import re
import uuid
import database
import service
import paramiko
from stat import S_ISDIR
import base64
import os
import random
import string
import time


class Probe:

    def __init__(self, path):
        self.path = path
        self.db = database.MySQLDatabase()
        self.probe_id = self.get_probe_id()
        self.ip_address = self.get_ip_address()
        self.mac_address = self.get_mac_address()
        self.setup_probe()
        self.workday()

    def get_probe_id(self):
        ID_FILE = self.path + '/' + 'ipb.reg'
        if os.path.isfile(ID_FILE) and os.access(ID_FILE, os.R_OK):
            probe_id = open(ID_FILE, "r").readline()
        else:
            probe_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(16))
            open(ID_FILE, "wb").write(probe_id)
        return probe_id

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def get_mac_address(self):
        mac = ''.join(re.findall('..', '%012x' % uuid.getnode()))
        mac_address = ':'.join(mac[i:i + 2] for i in range(0, 12, 2))
        return mac_address

    def setup_probe(self):
        sql = "INSERT INTO PROBES VALUES ('{ipd}', {nom}, '{iadr}', '{madr}', '{stat}', NOW(), NOW(), {coll}) ON DUPLICATE KEY UPDATE `ip_address`='{iadr}', `mac_address`='{madr}', `last_updated`=NOW();".format(
            ipd=self.probe_id, nom='NULL', iadr=self.ip_address, madr=self.mac_address, stat=3, coll='NULL'
        )
        self.db.commit_sql_statement(sql)

    def details(self):
        sql = "SELECT `probe_status`, `collection_id` FROM PROBES WHERE `probe_id`='{ipb}';".format(ipb=self.probe_id)
        information = self.db.select(sql)
        current_status = information[0][0]
        current_collection = information[0][1]
        return current_status, current_collection

    def get_active_services(self, collection_id):
        sql = "SELECT `service_id`, `transport_protocol`, `file_command`, `file_name`, `udp_command` FROM SERVICES WHERE `service_id` in (SELECT `service_id` FROM RUNNING_SERVICES WHERE `collection_id`='{coll}' AND `running_svc_status`={status})".format(
            coll=collection_id, status=1)
        return self.db.select(sql)

    def workday(self):
        state, collection_id = self.details()
        if state.lower() == 'active' and collection_id != None:
            print 'Ready to work. {time}'.format(time=time.strftime('%Y-%m-%d %H:%M:%S'))
            active_services = self.get_active_services(collection_id)
            for svc in active_services:
                # print svc
                tester = service.Service(service_id=svc[0], probe_id=self.probe_id, collection_id=collection_id,
                                         transport_protocol=svc[1], file_cmd=svc[2], file_name=svc[3], udp_cmd=svc[4])
        else:
            print 'Probe fall as sleep ({state})'.format(state=state)


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    print path
    helloProbe = Probe(path)
