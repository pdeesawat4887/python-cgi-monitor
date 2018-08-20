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
import smtplib
import poplib
import imaplib
import youtube_dl
from pip._vendor.colorama import Fore, Style


class MySQLDatabase:

    def __init__(self):
        self.create_connection()

    # def create_connection(self, user='centos', passwd='root', host='192.168.1.8', database='project'):
    def create_connection(self, user='catma', passwd='root', host='127.0.0.1', database='project'):
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

    def query_service(self, service_id):
        query_sql = "SELECT service_name FROM service WHERE service_id='{}'".format(service_id)
        self.mycursor.execute(query_sql)
        myresult = self.mycursor.fetchone()
        return myresult[0]

    def close_connection(self):
        self.mycursor.close()
        self.connection.disconnect()
        print 'Terminate Connection'


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
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
        except:
            ip_address = '127.0.0.1'
        # return ip_address
        self.ip = ip_address

    def get_name(self):
        self.name = self.setting['node_name']
        # return self.setting['node_name']


class Service(Probe):
    data = {}

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
        try:
            print time
            return round(float(time), 2)
        except:
            return 'NULL'

    def identify_url(self, url):
        return urlparse.urlparse(url)

    def convert_to_mbs(self, number_of_bytes):
        try:
            print number_of_bytes
            return bitmath.MiB(bytes=number_of_bytes)
        except:
            return 'NULL'

    def query_data(self, service_id):
        query_sql = "SELECT * FROM configuration WHERE service_id='{}'".format(service_id)
        self.mycursor.execute(query_sql)
        self.result = self.mycursor.fetchall()

    def availability_service(self, service_id, warning_value=2):
        data_forDB = []
        self.query_data(service_id)

        time_start = self.get_time_format()

        for counter in self.result:
            counter = list(counter)
            destination = self.reformat_counter(counter[2])

            # print "DESTINATION", destination
            # print "PORT", counter[3]

            status, response = self.get_status(destination, counter[3])

            response = self.round_2_decimal(response)

            temp = (self.id, counter[0], status, response, time_start)
            data_forDB.append(temp)

            ##################### Notify by line ###########################

            service_name = self.query_service(service_id)
            self.notify_line(self.name, self.ip, service_name, destination, status, warning_value)

        print data_forDB
        self.insert_availability_service(data_forDB)
        print "SUCCESS INSERT DATA"
        data_forDB = []
        print data_forDB
        print self.result

        # self.close_connection()

    def performance_service(self, service_id, warning_value=2):
        data_forDB = []
        self.query_data(service_id)

        time_start = self.get_time_format()

        for counter in self.result:
            counter = list(counter)
            destination = self.reformat_counter(counter[2])

            ping, download, upload, location = self.get_status(destination, counter[3])

            download = self.round_2_decimal(self.convert_to_mbs(download))
            upload = self.round_2_decimal(self.convert_to_mbs(upload))

            temp = (self.id, counter[0], ping, download, upload, location, time_start)
            print temp
            data_forDB.append(temp)

            # ##################### Notify by line ###########################
            #
            # service_name = self.query_service(service_id)
            # self.notify_line(self.name, self.ip, service_name, destination, status, warning_value)

        print   data_forDB
        self.insert_performance_service(data_forDB)
        print "SUCCESS INSERT DATA"
        data_forDB = []
        print   data_forDB
        print self.result

        # self.close_connection()

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

    def notify_line(self, probe_name, ip, service, destination, status, warning_value):

        if status == warning_value:
            url = 'https://notify-api.line.me/api/notify'
            token = 'pyL4xY6ys303vg0bVnvd0DRco7UyILVo5dOXZGjBWD8'
            headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}

            msg = '\nWARNING !!!\nProbe Name: {}\nIP Address: {}\nService: {}\nDestination: {}\nStatus: {}\nPlease check your service'.format(
                probe_name, ip, service, destination, status)

            request = requests.post(url, headers=headers, data={'message': msg})

            # print request.text


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
        return self.identify_url(destination).netloc


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


class SMTPService(Service):

    def __init__(self):
        Service.__init__(self)

    def get_status(self, destination, port):
        try:
            start = self.get_time()
            connection = smtplib.SMTP()
            connection.connect(destination, port)

            end = self.get_time()

            status = self.check_response_code(connection.helo()[0])
            response = self.get_response_time(start, end)

            connection.close()
            return status, response
        except:
            return 2, 0


class IMAPService(Service):

    def __init__(self):
        Service.__init__(self)

    def get_status(self, destination, port):
        try:
            start = self.get_time()
            connection = imaplib.IMAP4_SSL(destination, port)
            msg = connection.welcome
            end = self.get_time()
            connection.shutdown()

            response = self.get_response_time(start, end)

            if 'ok' and 'ready' in msg.lower():
                return 0, response
        except:
            try:
                start = self.get_time()
                connection = imaplib.IMAP4_SSL(destination, port)
                msg = connection.welcome
                end = self.get_time()
                connection.shutdown()

                response = self.get_response_time(start, end)

                if 'ok' and 'ready' in msg.lower():
                    return 0, response
            except:
                return 2, 0


class POP3Service(Service):

    def __init__(self):
        Service.__init__(self)

    def get_status(self, destination, port):
        try:
            start = self.get_time()
            connection = poplib.POP3(destination, port)
            msg = connection.welcome
            end = self.get_time()
            connection.quit()

            response = self.get_response_time(start, end)

            if 'ok' and 'ready' in msg.lower():
                return 0, response
        except:
            try:
                start = self.get_time()
                connection = poplib.POP3_SSL(destination, port)
                msg = connection.welcome
                end = self.get_time()
                connection.quit()

                response = self.get_response_time(start, end)

                if 'ok' and 'ready' in msg.lower():
                    return 0, response
            except:
                return 2, 0

    # def reformat_counter(self, destination):
    #     return destination


class VideoService(Service):
    data_speed = []

    def __int__(self):
        Service.__init__(self)

    def collect_data(self, result):
        if result['status'] != 'finished':
            speed = result['speed']
            print speed
            # if type(speed) != <type 'NoneType'>:
            if isinstance(speed, float):
                print type(speed)
                self.data_speed.append(speed)
                print self.data_speed

    def get_status(self, destination, port):
        opts = {
            'progress_hooks': [self.collect_data],
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '../video/sample.%(ext)s'
        }

        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download([destination])

            avg = sum(self.data_speed) / float(len(self.data_speed))
            print 'AVG: ', avg

            name = '../video'
            os.system('rm -rf {}'.format(name))

            self.data_speed = []

        return 'NULL', avg, 'NULL', 'NULL'


aaa = ICMPService()
bbb = DNSService()
ccc = WebService()
sss = SpeedtestService()
ddd = SMTPService()
eee = IMAPService()
www = POP3Service()
you = VideoService()

while True:
    # aaa.availability_service('1')
    # bbb.availability_service('2')
    # ccc.availability_service('4')
    # sss.performance_service('5')
    # ddd.availability_service('7')
    # eee.availability_service('8')
    # www.availability_service('9')
    you.performance_service('6')
    time.sleep(60)

# xxx = IMAPService()
# xxx.availability_service('8')
#
# yyy = POP3Service()
# yyy.availability_service('9')

# xxx = ICMPService()
# xxx.availability_service('1')
#
# yyy = WebService()
# yyy.availability_service('4')
#
# zzz = DNSService()
# zzz.availability_service('2')
#
# uuu = SpeedtestService()
# uuu.performance_service('5')
#
# ooo = SMTPService()
# ooo.availability_service('7')
#
# ppp = IMAPService()
# ppp.availability_service('8')
#
# www = POP3Service()
# www.availability_service('9')

# uuu = SpeedtestService()
# uuu.performance_service('5')
