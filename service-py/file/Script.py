#!/Applications/XAMPP/xamppfiles/htdocs/python/python-cgi-monitor/venv/bin/python

import socket
import mysql.connector
import re, uuid
import time
import os
import sys
import subprocess
import urlparse
import requests
import bitmath
import speedtest
from pip._vendor.colorama import Fore, Style


class MySQLDatabase:

    def __init__(self):
        self.create_connection()

    def create_connection(self, user='centos', passwd='root', host='192.168.1.8', database='project'):
        try:
            self.connection = mysql.connector.connect(user=user, password=passwd, host=host, database=database)
            self.mycursor = self.connection.cursor()
        except Exception as error:
            print 'Error database: ', Fore.RED, error, Style.RESET_ALL

    def query_probe(self, id, name, ip, mac_address):
        query_sql = "SELECT probe_id FROM probe WHERE probe_id='{}'".format(id)
        self.mycursor.execute(query_sql)
        myresult = self.mycursor.fetchall()
        if self.mycursor.rowcount == 1:
            probe_id = myresult[0][0]
        else:
            self.insert_new_probe(id=id, name=name, ip=ip, mac_address=mac_address)
            probe_id = id
        return probe_id

    def insert_new_probe(self, id, name, ip, mac_address):
        insert_sql = "INSERT INTO probe VALUES ('{}', '{}', '{}', '{}', '0')".format(id, name, ip, mac_address)
        self.mycursor.execute(insert_sql)
        self.connection.commit()

    def insert_availability_service(self, list_data):
        insert_sql = "INSERT INTO availability_service VALUES (NULL, %s, %s, %s, %s, %s)"
        self.mycursor.executemany(insert_sql, list_data)
        self.connection.commit()

    def insert_performance_service(self, list_data):
        insert_sql = "INSERT INTO performance_service VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)"
        self.mycursor.executemany(insert_sql, list_data)
        self.connection.commit()

    def close_connection(self):
        self.connection.disconnect()


class Probe(MySQLDatabase):
    setting = {}

    def __init__(self):
        MySQLDatabase.__init__(self)
        self.prepare_setting()
        self.prepare_node()

    def prepare_setting(self, file='../conf/configure'):
        infile = open(file, "r")
        for line in infile:
            if not line.strip():
                continue
            else:
                if not '#' in line:
                    key, value = line.strip().split('=')
                    self.setting[key] = value
        infile.close()

    def prepare_node(self):
        self.get_mac_address()
        self.get_ip()
        self.get_name()
        self.query_probe(id=self.id, name=self.name, ip=self.ip, mac_address=self.mac_address)

    def get_mac_address(self):
        mac = ''.join(re.findall('..', '%012x' % uuid.getnode()))
        eui64 = mac[0:6] + 'fffe' + mac[6:]
        eui64 = hex(int(eui64[0:2], 16) ^ 2)[2:].zfill(2) + eui64[2:]
        # return eui64, mac
        self.mac_address = mac
        self.id = eui64

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        # return ip_address
        self.ip = ip_address

    def get_name(self):
        self.name = self.setting['node_name']
        # return self.setting['node_name']


class Service(Probe):
    data = {}
    data_forDB = []

    def __init__(self):
        Probe.__init__(self)

    def check_response_code(self, response_code):
        try:
            if (200 <= int(response_code) <= 299):
                result = 0
            else:
                result = 2
        except Exception as error:
            result = 1
            print 'Error: ', Fore.RED, error, Style.RESET_ALL
        return result

    def get_time_format(self):
        return time.strftime('%Y-%m-%d %H:%M:%S')

    def get_time(self):
        return time.time()

    def get_response_time(self, start, end):
        return (end - start) * 1000

    def round_2_decimal(self, time):
        return round(float(time), 2)

    # def get_platform(self):
    #     platforms = {
    #         'linux1': '-c',
    #         'linux2': '-c',
    #         'darwin': '-c',
    #         'win32': '-n'
    #     }
    #     # timeout = {
    #     #     'linux1': '-t',
    #     #     'linux2': '-t',
    #     #     'darwin': '-t',
    #     #     'win32': '-w'
    #     # }
    #     if sys.platform not in platforms:
    #         return sys.platform
    #
    #     # return platforms[sys.platform], timeout[sys.platform]
    #     return platforms[sys.platform]

    def identify_url(self, url):
        return urlparse.urlparse(url)

    def convert_to_mbs(self, number_of_bytes):
        return bitmath.MiB(bytes=number_of_bytes)

    # def convert_byte(self, number_of_bytes):
    #     if number_of_bytes < 0:
    #         raise ValueError("!!! number_of_bytes can't be smaller than 0 !!!")
    #
    #     step_to_greater_unit = 1024.
    #
    #     number_of_bytes = float(number_of_bytes)
    #     unit = 'bytes'
    #
    #     if (number_of_bytes / step_to_greater_unit) >= 1:
    #         number_of_bytes /= step_to_greater_unit
    #         unit = 'KB'
    #
    #     if (number_of_bytes / step_to_greater_unit) >= 1:
    #         number_of_bytes /= step_to_greater_unit
    #         unit = 'MB'
    #
    #     if (number_of_bytes / step_to_greater_unit) >= 1:
    #         number_of_bytes /= step_to_greater_unit
    #         unit = 'GB'
    #
    #     if (number_of_bytes / step_to_greater_unit) >= 1:
    #         number_of_bytes /= step_to_greater_unit
    #         unit = 'TB'
    #
    #     precision = 1
    #     number_of_bytes = round(number_of_bytes, precision)
    #
    #     return number_of_bytes

    def query_data(self, service_id):
        query_sql = "SELECT * FROM configuration WHERE service_id='{}'".format(service_id)
        self.mycursor.execute(query_sql)
        self.result = self.mycursor.fetchall()

    def availability_service(self, service_id):
        self.query_data(service_id)

        time_start = self.get_time_format()

        for counter in self.result:
            counter = list(counter)
            destination = self.reformat_counter(counter[2])

            status, response = self.get_status(destination, counter[3])

            response = self.round_2_decimal(response)

            temp = (self.id, counter[0], status, response, time_start)
            self.data_forDB.append(temp)

        self.insert_availability_service(self.data_forDB)
        print "SUCCESS INSERT DATA"
        self.data_forDB = []

    def performance_service(self, service_id):
        self.query_data(service_id)

        time_start = self.get_time_format()

        for counter in self.result:
            counter = list(counter)
            destination = self.reformat_counter(counter[2])

            ping, download, upload, location = self.get_status(destination, counter[3])

            download = self.round_2_decimal(self.convert_to_mbs(download))
            upload = self.round_2_decimal(self.convert_to_mbs(upload))

            temp = (self.id, counter[0], ping, download, upload, location, time_start)
            self.data_forDB.append(temp)

        self.insert_performance_service(self.data_forDB)
        print "SUCCESS INSERT DATA"
        self.data_forDB = []

    # def test_output(self, service_id):
    #     self.query_data(service_id)
    #     for i in self.result:
    #         i = list(i)
    #         dest = self.reformat_counter(i[2])
    #         self.get_status(dest, i[3])

    def get_status(self, destination, port):
        pass

    def reformat_counter(self, destination):
        return destination


class ICMPService(Service):

    def __init__(self):
        Service.__init__(self)
        # self.main()

    def get_status(self, destination, port):

        param = '-n' if sys.platform.lower() == 'windows' else '-c'
        command = ['ping', param, '1', '-t', '1', destination]
        status = 1
        response = 0

        try:
            output = subprocess.check_output(command).split()
            for element in output:
                if 'time' in element.lower():
                    status = 0
                    response = element.split('=')[1]

        except:
            status = 2
            response = 0

        return status, response

    def reformat_counter(self, destination):
        return urlparse.urlparse(destination).netloc


class DNSService(Service):

    def __init__(self):
        Service.__init__(self)

    def get_status(self, destination, port):

        command = ['dig', '@' + destination, 'www.google.com']
        status = 1
        response = 0

        try:
            output = subprocess.check_output(command).split('\n')
            for element in output:
                if 'query time' in element.lower():
                    status = 0
                    response = element.split()[3]
        except:
            status = 2
            response = 0

        return status, response

    # def reformat_counter(self, destination):
    #     return destination


class WebService(Service):

    def __init__(self):
        Service.__init__(self)

    def get_status(self, destination, port):
        header = {'User-Agent': self.setting['User-Agent']}
        try:
            res_http = requests.get(destination, headers=header)
            status_code = res_http.status_code
            timer = res_http.elapsed.total_seconds() * 1000
            res_http.close()
            status = self.check_response_code(status_code)
            return status, timer
        except:
            return 2, 0

    # def reformat_counter(self, destination):
    #     return destination


class SpeedtestService(Service):

    def __init__(self):
        Service.__init__(self)

    def get_status(self, destination, port):
        try:
            clinet = speedtest.Speedtest()
            clinet.get_servers([destination])
            clinet.get_best_server()
            clinet.download()
            clinet.upload()
            result = clinet.results.dict()
            return result['ping'], result['download'], result['upload'], result['server']['name']
        except:
            print "Error"
            return 0, 0, 0, 'NULL'

    # def reformat_counter(self, destination):
    #     return destination

# example = ICMPService()
# hello = DNSService()
# world = WebService()
# speed = SpeedtestService()
# while True:
#     # example.test_output('1')
#     # example.availability_service('1')
#     # hello.availability_service('2')
#     # world.availability_service('4')
#     speed.performance_service('5')
#     time.sleep(120)
