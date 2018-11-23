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
import uuid
import time


class Probe:

    def __init__(self, path):
        self.path = path
        self.db = database.MySQLDatabase()
        self.mac_address = self.get_mac_address()
        self.ip_address = self.get_ip_address()
        self.probe_id = self.get_probe_id()
        self.setup_probe()
        self.find_my_status()
        # self.workday()

    def get_probe_id(self):
        mac = self.mac_address.replace(':', '')
        eui64 = mac[0:6] + 'fffe' + mac[6:]
        return (hex(int(eui64[0:2], 16) ^ 2)[2:].zfill(2) + eui64[2:]).upper()

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
        return ':'.join(mac[i:i + 2] for i in range(0, 12, 2))

    def setup_probe(self):
        sql = "INSERT INTO PROBES VALUES ('{ipd}', '{nom}', '{iadr}', '{madr}', '{stat}', NOW(), NOW()) ON DUPLICATE KEY UPDATE `ip_address`='{iadr}', `mac_address`='{madr}', `last_updated`=NOW();".format(
            ipd=self.probe_id, nom=self.probe_id, iadr=self.ip_address, madr=self.mac_address, stat=3)
        self.db.execute_sql(sql)

    def get_active_services(self):
        sql = "SELECT `service_id`, `transport_protocol`, `file_command`, `file_name`, `udp_command` FROM SERVICES WHERE `service_id` IN (SELECT `service_id` FROM RUNNING_SERVICES WHERE `cluster_id`='{iclus}' AND `running_svc_status`='{status}');".format(
            iclus=self.cluster_id, status='Active')
        return self.db.select(sql)

    # def workday(self):
    #     state, collection_id = self.details()
    #     if state.lower() == 'active' and collection_id != None:
    #         print 'Ready to work. {time}'.format(time=time.strftime('%Y-%m-%d %H:%M:%S'))
    #         active_services = self.get_active_services(collection_id)
    #         for svc in active_services:
    #             # print svc
    #             tester = service.Service(service_id=svc[0], probe_id=self.probe_id, collection_id=collection_id,
    #                                      transport_protocol=svc[1], file_cmd=svc[2], file_name=svc[3], udp_cmd=svc[4], path=self.path)
    #     else:
    #         print 'Probe fall as sleep ({state})'.format(state=state)

    def working_day(self):
        print 'PROBE ready to work, {time}'.format(time=time.strftime('%Y-%m-%d %H:%M:%S'))
        active_services = self.get_active_services()
        for svc in active_services:
            worker = service.Service(service_id=svc[0], probe_id=self.probe_id, cluster_id=self.cluster_id,
                                     transport_protocol=svc[1], file_cmd=svc[2], file_name=svc[3], udp_cmd=svc[4],
                                     path=self.path)

    def find_my_cluster(self):
        cluster_id = self.db.select(
            "SELECT `cluster_id` FROM `CLUSTERS` WHERE `probe_id`='{ipb}'".format(ipb=self.probe_id))
        if cluster_id:
            self.cluster_id = cluster_id[0][0]
        else:
            print "PLEASE REGISTER CLUSTER ID with PROBE ID {ipb}".format(ipb=self.probe_id)
            exit()

    def find_my_status(self):
        status = \
        self.db.select("SELECT `probe_status` FROM `PROBES` WHERE `probe_id`='{ipb}'".format(ipb=self.probe_id))[0][0]
        if status == 'Idle':
            print "PROBE STATUS: {status} be inactive or not working at a job.".format(status=status)
            exit()
        elif status == 'Active':
            self.find_my_cluster()
            self.working_day()
        else:
            print "PROBE STATUS: {status}.".format(status=status)
            exit()
