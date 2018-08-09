import speedtest
import time
import os
import smtplib
import poplib
import imaplib
import sys
import subprocess
import mysql.connector
import pythonwhois
import urlparse
import requests

# Extra for Exception
from pip._vendor.colorama import Fore, Style


### return 0: active, working
### return 1: Inactive, Not working
### return 2: Error
### return 3: Unknow

class MySQLDatabase:

    def __init__(self):
        self.create_connection()

    def create_connection(self, user='catma', passwd='root', host='localhost', database='service_db'):
        try:
            self.connection = mysql.connector.connect(user=user, password=passwd, host=host, database=database)
            self.mycursor = self.connection.cursor()
        except Exception as error:
            print 'Error database: ', Fore.RED, error, Style.RESET_ALL

    def insert_speedtest(self, list_data):
        sql = "INSERT INTO speedtestService VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)"
        self.mycursor.executemany(sql, list_data)
        self.connection.commit()

    def insert_webtest(self, list_data):
        sql = "INSERT INTO webService VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.mycursor.executemany(sql, list_data)
        self.connection.commit()

    def insert_mail_dns(self, table, list_data):
        sql = "INSERT INTO {} VALUES (NULL, %s, %s, %s, %s, %s, %s)".format(table)
        self.mycursor.executemany(sql, list_data)
        self.connection.commit()


class Service:
    setting = {}

    def __init__(self):
        self.configure_setting()

    def configure_setting(self, file='conf/setting.txt'):
        infile = open(file, "r")
        for line in infile:
            if not line.strip():
                continue
            else:
                key, value = line.strip().split('=')
                self.setting[key] = value
        infile.close()

    def convert_byte(self, number_of_bytes):
        if number_of_bytes < 0:
            raise ValueError("!!! number_of_bytes can't be smaller than 0 !!!")

        step_to_greater_unit = 1024.

        number_of_bytes = float(number_of_bytes)
        unit = 'bytes'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'KB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'MB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'GB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'TB'

        precision = 1
        number_of_bytes = round(number_of_bytes, precision)

        return number_of_bytes

    def my_platform(self):
        platforms = {
            'linux1': '-c',
            'linux2': '-c',
            'darwin': '-c',
            'win32': '-n'
        }
        if sys.platform not in platforms:
            return sys.platform

        return platforms[sys.platform]

    def check_response_code(self, response_code):
        try:
            if (200 <= int(response_code) <= 299):
                result = 0
            else:
                result = 1
        except Exception as error:
            result = 2
            print 'Error: ', Fore.RED, error, Style.RESET_ALL  ########################################
        return result

    def check_respone_text(self, response_txt):
        try:
            if 'OK' or 'ready' in response_txt:
                result = 0
            else:
                result = 1
        except Exception as error:
            result = 2
            print 'Error: ', Fore.RED, error, Style.RESET_ALL  ########################################
        return result

    def ping_once(self, destination):
        platform_count = self.my_platform()
        with open(os.devnull, 'w') as DEVNULL:
            try:
                subprocess.check_call(
                    ['ping', platform_count, '1', destination],
                    stdout=DEVNULL,
                    stderr=DEVNULL
                )
                is_up = 0
            except subprocess.CalledProcessError:
                is_up = 1
        return is_up

    def identify_url(self, url):
        return urlparse.urlparse(url)

    def current_date_time(self):
        current_date = time.strftime('%Y-%m-%d')
        current_time = time.strftime('%H:%M:%S')
        return current_date, current_time

    def read_file(self, file='conf/speedtest_list_re.txt'):
        file_read = []
        infile = open(file, "r")
        for line in infile:
            if not line.strip():
                continue
            else:
                if not '#' in line:
                    file_read.append(line.rstrip())
        infile.close()
        return file_read


class Speedtest(Service):
    server = []

    def __init__(self):
        Service.__init__(self)
        self.temp_server = self.read_file('conf/speedtest_list_re.txt')
        self.get_server()

    def get_server(self):
        for server_num in self.temp_server:
            self.server.append(server_num.split(')')[0].replace(' ', ''))

    def test_speed(self, server):
        speed = speedtest.Speedtest()
        speed.get_servers([server])
        name = speed.get_servers([server]).values()[0][0]['name']
        speed.get_best_server()
        speed.download()
        speed.upload()
        result = speed.results.dict()
        return name, result['download'], result['upload'], result['ping']


class Website(Service):
    host = []

    def __init__(self):
        Service.__init__(self)
        self.get_host()

    def get_host(self):
        origin_host = self.read_file(file='conf/website_conf.txt')
        for host in origin_host:
            self.host.append(self.identify_url(host))

    def get_website_status_whois(self, url):
        temp_url = url.replace('www.', '')
        result_whois = pythonwhois.get_whois(temp_url)

        try:
            checker = result_whois['status'][0].lower()
            if 'active' in checker:
                result_status = 0
            elif 'prohibited' in checker:
                result_status = 3
            else:
                result_status = 2
        except Exception as error:
            result_status = 2
            print 'Error: ', Fore.RED, error, Style.RESET_ALL
        return result_status

    def get_website_request(self, url):
        header = {'User-Agent': self.setting['User-Agent']}
        try:
            res_http = requests.get(url, headers=header)
            checker = res_http.status_code
            res_http.close()
            return self.check_response_code(checker)
        except Exception as error:
            print 'Error: ', Fore.GREEN, error, Style.RESET_ALL
            return 2


class Email(Service):
    mail_server = {}

    def __init__(self):
        Service.__init__(self)
        self.get_mail_server()

    def get_mail_server(self, file='conf/email_conf.txt'):
        temp_server = self.read_file(file=file)
        for server in temp_server:
            host, smtp, imap, pop3 = server.split(':')
            self.mail_server[host] = [smtp, imap, pop3]

    def connect_smtp(self, server, port):
        try:
            self.connection_smtp = smtplib.SMTP()
            self.connection_smtp.connect(server, port)
        except Exception as error:
            print 'Error create mail : smtp : ', Fore.RED, error, Style.RESET_ALL

    def connect_imap(self, server, port):
        try:
            self.connection_imap = imaplib.IMAP4_SSL(server, port)
        except Exception as error:
            self.connection_imap = imaplib.IMAP4(server, port)
            print 'Connected IMAP without SSL'

    def connect_pop3(self, server):
        try:
            self.connection_pop3 = poplib.POP3_SSL(server)
        except Exception as error:
            self.connection_pop3 = poplib.POP3(server)
            print 'Connected POP3 without SSL'

    def get_smtp_status(self):
        res_code = self.connection_smtp.helo()[0]
        return self.check_response_code(res_code)

    def get_imap_status(self):
        res_txt = self.connection_imap.welcome
        return self.check_respone_text(res_txt)

    def get_pop3_status(self):
        res_txt = self.connection_pop3.welcome
        return self.check_respone_text(res_txt)

    def terminate_smtp_connection(self):
        self.connection_smtp.quit()
        self.connection_smtp.close()

    def terminate_imap_connection(self):
        # self.connection_imap.close()
        # self.connection_imap.close()
        # self.connection_imap.close()
        pass

    def terminate_pop3_connection(self):
        self.connection_pop3.quit()

    def connect_all_once(self, server, port_smtp, port_imap):
        self.connect_smtp(server=server, port=port_smtp)
        self.connect_imap(server=server, port=port_imap)
        self.connect_pop3(server=server)

    def get_all_status(self):
        smtp = self.get_smtp_status()
        imap = self.get_imap_status()
        pop3 = self.get_pop3_status()
        return smtp, imap, pop3

    def terminate_all(self):
        self.terminate_smtp_connection()
        self.terminate_imap_connection()
        self.terminate_pop3_connection()



class DomainNameServer(Service):
    dns_server = []

    def __init__(self):
        Service.__init__(self)
        self.get_dns_server()

    def get_dns_server(self, file='conf/dns_conf.txt'):
        self.dns_server = self.read_file(file)

    def nslookup_soa(self, server):
        try:
            result = subprocess.check_output(['nslookup', '-ty=SOA', 'google.com', server])
        except Exception as error:
            result = error
            print 'Error: ', Fore.GREEN, error, Style.RESET_ALL

        if 'origin' in result:
            status = 0
        else:
            status = 1
        return status


class Monitor(Service):

    def __init__(self):
        Service.__init__(self)
        self.create_database_connection()
        self.node = self.setting['node']
        self.current_date, self.current_time = self.current_date_time()

    def create_database_connection(self):
        self.database = MySQLDatabase()

    def test_speedtest(self):
        data = []
        test = Speedtest()
        for server in test.server:
            name, download, upload, ping = test.test_speed(server)
            download = test.convert_byte(download)
            upload = test.convert_byte(upload)
            temp_data = (self.node, name, self.current_date, self.current_time, download, upload, ping)
            data.append(temp_data)
        self.database.insert_speedtest(data)
        print '----------- INSERT SPEEDTEST SUCCESS ---------'

    def test_website(self):
        data = []
        website_test = Website()
        for url in website_test.host:
            ping = website_test.ping_once(url.netloc)
            status_whois = website_test.get_website_status_whois(url.netloc)
            status_req = website_test.get_website_request(url.scheme + '://' + url.netloc)
            temp_data = (
                self.node, url.netloc, self.current_date, self.current_time, url.scheme, ping, status_whois, status_req)
            data.append(temp_data)
        self.database.insert_webtest(data)
        print '----------- INSERT WEBSITE SUCCESS ---------'

    def test_mail(self):
        data = []
        mail_test = Email()
        server = mail_test.mail_server
        for host in server:
            mail_test.connect_all_once(server=host, port_smtp=server[host][0], port_imap=server[host][1])
            smtp_status, imap_status, pop3_status = mail_test.get_all_status()
            mail_test.terminate_all()
            temp_data = (self.node, host, self.current_date, self.current_time, 'smtp', smtp_status), \
                        (self.node, host, self.current_date, self.current_time, 'imap', imap_status), \
                        (self.node, host, self.current_date, self.current_time, 'pop3', pop3_status)
            data.extend(temp_data)
        self.database.insert_mail_dns('mailService', data)
        print '----------- INSERT MAIL SUCCESS ---------'

    def test_dns(self):
        data = []
        dns_test = DomainNameServer()
        for server in dns_test.dns_server:
            ping = dns_test.ping_once(server)
            status = dns_test.nslookup_soa(server=server)
            temp_data = (self.node, server, self.current_date, self.current_time, ping, status)
            data.append(temp_data)
        self.database.insert_mail_dns('dnsService', data)
        print '----------- INSERT DNS SUCCESS ---------'


monitor = Monitor()
monitor.test_speedtest()
monitor.test_website()
monitor.test_mail()
monitor.test_dns()
