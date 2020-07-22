import speedtest
import time
import struct
from firebase import firebase
import socket
import os
import urllib
import smtplib
import poplib
import imaplib
import sys
import subprocess
import mysql.connector
import pythonwhois
import urlparse
import requests
from contextlib import contextmanager


class Tools:

    def convert(self, number_of_bytes):
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

    def get_ntp_time(self, addr='time.nist.gov'):
        TIME1970 = 2208988800L  # Thanks to F.Lundh
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = '\x1b' + 47 * '\0'
        client.sendto(data, (addr, 123))
        data, address = client.recvfrom(1024)
        if data:
            t = struct.unpack('!12I', data)[10]
            t -= TIME1970
            return time.ctime(t)

    def get_platform(self):
        platforms = {
            'linux1': '-c',
            'linux2': '-c',
            'darwin': '-c',
            'win32': '-n'
        }
        if sys.platform not in platforms:
            return sys.platform

        return platforms[sys.platform]

    def check_code(self, code):

        try:
            if (200 <= code <= 299):
                result = 'Working'
            else:
                result = 'Not Working'
        except Exception as ex:
            result = 'Could not connect to page. error at tool Class'

        return result

    # def load_setting(self, file):
    #     typeList = {}
    #     with open(file) as f:
    #         for line in f:
    #             key, value = line.strip().split()
    #             typeList[key] = value
    #         return typeList


# tool = Tools()
# serverList = []
# dictionary = tool.load_setting('setting.txt')
# print dictionary
# for i in dictionary:
#     if 'server' in i:
#         serverList.append(dictionary[i])
#     print dictionary[i]
#
# print serverList
# # print dictionary


class FirebaseDatabase:

    def __init__(self, url='https://pythonwithfirebase-catma.firebaseio.com'):
        self.connection = firebase.FirebaseApplication(url)

    def put_data(self, table, path, data):
        self.connection.put(table, path, data)

    def post_data(self, path, data):
        self.connection.post(path, data)


class SpeedTestPy:
    setting = {}
    server_list = []

    def __init__(self):
        self.load_setting()

    def test(self, server):
        s = speedtest.Speedtest()
        s.get_servers([server])
        name = s.get_servers([server]).values()[0][0]['name']
        s.get_best_server()
        s.download()
        s.upload()
        res = s.results.dict()
        return name, res["download"], res["upload"], res["ping"]

    def load_setting(self, file='conf/setting.txt'):
        with open(file) as f:
            for line in f:
                key, value = line.strip().split('=')
                if 'server' in key:
                    self.server_list.append(value)
                else:
                    self.setting[key] = value


class WebService:
    host_list = []
    protocols = {'HTTP': 'http://', 'HTTPS': 'https://'}

    def __init__(self):
        self.read_url()
        self.tool = Tools()

    def read_url(self, file='conf/hosts.txt'):
        with open(file, 'r') as temp_file:
            text = temp_file.read()
            self.host_list = text.split()
            temp_file.close()

    # def ping_ip_address(self, platform, url):
    #     try:
    #         ip_address = socket.gethostbyname(url)
    #         ping_value = os.system("ping " + platform + "1 " + ip_address)
    #         if ping_value == 0:
    #             ping_status = 'Active'
    #         else:
    #             ping_status = 'Check server first'
    #     except Exception as ex:
    #         ping_status = 'Cannot ping to destination'
    #     return ping_status

    def ping_ip_address(self, platform, url):
        with open(os.devnull, 'w') as DEVNULL:
            try:
                subprocess.check_call(
                    ['ping', platform, '1', url],
                    stdout=DEVNULL,
                    stderr=DEVNULL
                )
                is_up = True
            except subprocess.CalledProcessError:
                is_up = False
        return is_up

    # def ping_ip_address(self, platform, protocol, url):
    #     try:
    #         ip_address = socket.gethostbyname(url)
    #         ping_value = os.system("ping " + platform + "1 " + ip_address)
    #         if ping_value == 0:
    #             ping_status = 'Active'
    #         else:
    #             ping_status = 'Check server first'
    #     except Exception as ex:
    #         ping_status = 'Cannot ping to destination'
    #     return ping_status

    def check_status(self, protocol, url):
        try:
            res_https = urllib.urlopen(protocol + url)
            code = res_https.getcode()
            # reason = httplib.responses[status]
            res_https.close()

            status = self.tool.check_code(code)

        except Exception as ex:
            status = 'Could not connect to page. at webService Class'
        return status

    # def check_status(self, platform, protocol, url):
    #     try:
    #         res_https = urllib.urlopen(protocol + url)
    #         code = res_https.getcode()
    #         # reason = httplib.responses[status]
    #         res_https.close()
    #
    #         status = self.tool.check_code(code)
    #
    #     except Exception as ex:
    #         status = 'Could not connect to page. at webService Class'
    #     return status

    # def check_reason(self, status):
    #     try:
    #         reason = httplib.responses[status]
    #     except:
    #         reason = 'Could not connect to page.'
    #     return reason

    # def choice_operation(self, func, platform, protocol, url):
    #     operation = {'ping': self.ping_ip_address, 'status': self.check_status}
    #     data = operation[func](platform, protocol, url)
    #     return data


class EmailService:
    mail_server = {}
    emails = []

    def __init__(self):
        self.read_server()
        self.tool = Tools()

    def read_server(self, file="conf/email_conf.txt"):
        with open(file) as f:
            for line in f:
                if not '#' in line:
                    try:
                        key, smtp, imap, pop3 = line.strip().split(':')
                        self.mail_server[key] = [smtp, imap, pop3]
                    except:
                        if not '#' or ' ' in line:
                            print "Please check configure file at line", line

    def connect_smtp_server(self, hostServer, port):
        try:
            self.server = smtplib.SMTP()
            self.server.connect(hostServer, port)
            self.code = self.server.helo()
        except Exception as e:
            print e
            print "\nCouldn't connect."

    # def get_smtp_hello(self):
    #     self.code = self.server.helo()

    def get_smtp_status(self):

        check = int(self.code[0])
        status = self.tool.check_code(check)

        return status

    def connect_imap_server(self, hostServer, port):
        try:
            self.server = imaplib.IMAP4_SSL(hostServer, port)
        except Exception as e:
            self.server = imaplib.IMAP4(hostServer, port)

    def get_imap_status(self):

        check = self.server.welcome

        status = self.tool.check_code(check)

        return status

    def connect_pop_server(self, hostServer, port):
        try:
            self.server = poplib.POP3_SSL(hostServer)
        except Exception as e:
            self.server = poplib.POP3(hostServer)

    def get_pop_status(self):

        check = self.server.getwelcome()
        self.server.quit()

        if 'OK' in check:
            status = 'Working'
        else:
            status = 'Not Working'

        return status

    def check_response(self, msg):

        if 'OK' in msg:
            status = 'Working'
        else:
            status = 'Not Working'

        return status

    def connect_all(self, hostServer, port_smtp, port_imap):
        try:
            self.connect_smtp = smtplib.SMTP()
            self.connect_smtp.connect(hostServer, port_smtp)
            self.connect_pop3 = poplib.POP3_SSL(hostServer)
        except Exception as error:
            print error

        try:
            self.connect_imap = imaplib.IMAP4_SSL(hostServer, port_imap)
        except Exception as error:
            self.connect_imap = imaplib.IMAP4(hostServer, port_imap)
            print error

        try:
            self.connect_pop3 = poplib.POP3_SSL(hostServer)
        except Exception as error:
            self.connect_pop3 = poplib.POP3(hostServer)
            print error

    def status_all(self):
        smtp = int(self.connect_smtp.helo()[0])
        imap = self.connect_imap.welcome
        pop3 = self.connect_pop3.getwelcome()

        status_smtp = self.tool.check_code(smtp)
        status_imap = self.check_response(imap)
        status_pop3 = self.check_response(pop3)

        return status_smtp, status_imap, status_pop3

    def terminate_all(self):
        self.connect_smtp.close()
        self.connect_imap.close()
        self.connect_pop3.quit()

    # def quit_smtp_connection(self):
    #     self.server.quit()
    #
    # def quit_pop_connection(self):
    #     self.server.quit()
    #
    # def quit_imap_connection(self):
    #     self.server.close()

    # def connect_both(self, hostServer, port):
    #     self.connect_smtp_server(hostServer, port)
    #     self.connect_pop_server(hostServer)
    #     self.connect_imap_server(hostServer, port)
    #
    # def quit_both(self):
    #     self.quit_smtp_connection()
    #     self.quit_pop_connection()
    #     self.quit_imap_connection()

    ################## Special Function ######################

    def choice_connection(self, func, hostServer, port):
        connect_dict = {'smtp': self.connect_smtp_server, 'imap': self.connect_imap_server,
                        'pop3': self.connect_pop_server}

        get_data = {'smtp': self.get_smtp_status, 'imap': self.get_imap_status, 'pop3': self.get_pop_status}

        connect_dict[func](hostServer, port)

        data = get_data[func]()

        return data
    # def choice_close(self, func):
    #     close_dict = {'smtp': self.quit_smtp_connection, 'imap': self.quit_imap_connection,
    #                   'pop3': self.quit_pop_connection}
    #
    #     close_dict[func]()


class DNSService:
    target = []

    def __init__(self):
        self.__get_target__()

    def __get_target__(self, file='conf/dns_server_conf.txt'):
        with open(file, 'r') as temp_file:
            text = temp_file.read()
            self.target = text.split()
            temp_file.close()

    def __nslookup__(self, host, dns_server):
        try:
            result = (subprocess.check_output(['nslookup', '-ty=SOA', host, dns_server]))
        except subprocess.CalledProcessError as err:
            result = err
        return result

    def __check_nslookup_result__(self, result):
        if 'origin' in result:
            status = 'Working'
        else:
            status = 'Not Working'
        return status

    # def __get_nslookup_result__(self, platform, host, dns_server):
    #     result = self.__nslookup__(host, dns_server)
    #     return self.__check_nslookup_result__(result)
    #
    # def __ping__(self, platform, host, dns_server):
    #     try:
    #         ping = os.system("ping " + platform + "1 " + dns_server)
    #         if ping == 0:
    #             ping_status = 'Active'
    #         else:
    #             ping_status = 'Check server first'
    #     except Exception as ex:
    #         ping_status = 'Cannot ping to destination'
    #     return ping_status

    def __get_nslookup_result__(self, host, dns_server):
        result = self.__nslookup__(host, dns_server)
        return self.__check_nslookup_result__(result)

    def __ping__(self, platform, dns_server):
        try:
            ping = os.system("ping " + platform + " 1 " + dns_server)
            if ping == 0:
                ping_status = 'Active'
            else:
                ping_status = 'Check server first'
        except Exception as ex:
            ping_status = 'Cannot ping to destination'
        return ping_status

    # def __select_function__(self, func, platform, host, dns_server):
    #     operation = {'ping': self.__ping__, 'status': self.__get_nslookup_result__}
    #     temp = operation[func](platform, host, dns_server)
    #     return temp


class Shopping:
    website_list = []

    def __init__(self):
        self.get_shopping_website()
        pass

    def get_shopping_website(self, file='conf/shopping_conf.txt'):
        with open(file) as f:
            for line in f:
                obj = line.rstrip()
                self.website_list.append(obj)

    def get_whois(self, url_website):
        parse_obj = urlparse.urlparse(url_website)
        try:
            result = pythonwhois.get_whois(parse_obj.netloc)

            if 'Prohibited' in result['status'][0]:
                status = 'unknow'
            else:
                status = result['status'][0]

            expire_date = result['expiration_date'][0].date()
            # return result
        except Exception as error:
            print 'Error: ', error
            status = "Cannot Found in Whois"
            expire_date = "Cannot Found in Whois"

        return status, expire_date

    # def usage_result(self, result):
    #
    #     try:
    #         if 'Prohibited' in result['status'][0]:
    #             status = 'unknow'
    #         else:
    #             status = result['status'][0]
    #
    #         expire_date = result['expiration_date'][0].date()
    #     except:
    #         status = "Cannot Found in Whois"
    #         expire_date = "Cannot Found in Whois"
    #
    #     return status, expire_date

    def checkStatusHTTPS(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36 OPR/53.0.2907.99'}
        try:
            res_https = requests.get(url, headers=headers)
            status = res_https.status_code
            res_https.close()
        except Exception as ex:
            status = 'Could not connect to page.'
        return status

    def main(self):
        pass


class MySQLDatabase:

    def __init__(self):
        self.create_connection()

    def create_connection(self, user='catma', passwd='root', host='localhost', database='service_db'):
        try:
            self.connection = mysql.connector.connect(user=user, password=passwd, host=host, database=database)
            self.mycursor = self.connection.cursor()
        except Exception as error:
            print 'Error:', error

    def insert_many_data_dns_mail(self, table, list_data):
        sql_syntax = "INSERT INTO {} VALUES (NULL, %s, %s, %s, %s, %s, %s)".format(table)
        self.mycursor.executemany(sql_syntax, list_data)
        self.connection.commit()

    def insert_data_speedtest(self, table, list_data):
        sql_syntax = "INSERT INTO {} VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)".format(table)
        self.mycursor.executemany(sql_syntax, list_data)
        self.connection.commit()

    def close_connection(self):
        self.connection.close()


class Service:

    def __init__(self):
        self.tool = Tools()
        self.speed = SpeedTestPy()
        self.node = self.speed.setting['node']
        self.f_database = FirebaseDatabase(url='https://pythontestcode.firebaseio.com/')
        # self.f_database = FirebaseDatabase()
        self.localDatabase = MySQLDatabase()
        self.current_time = time.strftime('%H:%M:%S')
        self.current_date = time.strftime('%Y-%m-%d')

    def new_speedtest(self):

        temp_list = self.speed.server_list
        data = []

        for dest_server in temp_list:
            dest_name, downL, upL, ping = self.speed.test(dest_server)

            print dest_name, ":", time.ctime(time.time())

            downL = self.tool.convert(downL)
            upL = self.tool.convert(upL)
            temp_data = (self.node, dest_name, downL, upL, ping, self.current_date, self.current_time)
            data.append(temp_data)
        self.localDatabase.insert_data_speedtest('speedtestService', data)
        data = []
        print ' ----------------> INSERT SPEEDTEST SUCCESSFULLY <------------------'

    # def speedtest(self):
    #     # tool = Tools()
    #     # print "tools success"
    #     # micro = SpeedTestPy()
    #     # print "SpeedtestPy success"
    #     # node = self.speed.setting['node']
    #     # print "node query success"
    #     # f_database = FirebaseDatabase()
    #     # print "firebase success"
    #     test_time = self.speed.server_list
    #     # print "num of server success"
    #
    #     # Speedtest Function
    #     current_date = time.strftime('%Y-%m-%d')
    #     current_time = time.strftime('%H:%M:%S')
    #     for i in range(len(test_time)):
    #         # print "in for success"
    #         name, d, u, p = self.speed.test(test_time[i])
    #         # print "test success"
    #         d, du = self.tool.convert(d)
    #         # print "convert dw success"
    #         u, uu = self.tool.convert(u)
    #         # print "convert ul success"
    #         st_time = time.ctime(time.time())  # change to ntp time
    #         # print "convert ntp success"
    #         data = {'download': (d, du), 'upload': (u, uu), 'ping': p, 'execTime': execTime, 'time': st_time}
    #         # print "convert data success"
    #         # f_database.put_data('speedtest', node + '/' + name, data)
    #         self.f_database.post_data(self.node + '/speedtest/' + name, data)
    #         # print "convert post firebase success"
    #
    #         # Show output
    #         # print 'Time Start Speedtest: {}'.format(st_time)
    #         # print 'Test #{}'.format(i + 1)
    #         # print 'Download: {:.2f} {}'.format(d, du)
    #         # print 'Upload: {:.2f} {}'.format(u, uu)
    #         # print 'Ping: {}'.format(p)
    #         # print 'Execute Time: {}'.format(execTime)
    #     # End of Speedtest Function
    #     print " ----> SpeedTest Complete. <------", time.ctime(time.time())

    # def web_service(self):
    #     # temp_data_status = {}
    #     # temp_data_reason = {}
    #     # temp_data_ping = {}
    #     # web = WebService()
    #     # platform = self.tool.get_platform()
    #     # for protocol in web.protocols:
    #     #     for url in web.host_list:
    #     #         print url
    #     #         status = web.check_status(web.protocols[protocol], url)
    #     #         reason = web.check_reason(status)
    #     #         print "complete url"
    #     #         ping = web.ping_ip_address(url, platform)
    #     #         temp_url = url.split('.')
    #     #         temp_data_status[temp_url[0]] = status
    #     #         temp_data_reason[temp_url[0]] = reason
    #     #         temp_data_ping[temp_url[0]] = ping
    #     #     self.f_database.put_data(self.node, 'webService/' + protocol + '/status', temp_data_status)
    #     #     self.f_database.put_data(self.node, 'webService/' + protocol + '/reason', temp_data_reason)
    #     #     self.f_database.put_data(self.node, 'webService/' + protocol + '/ping', temp_data_ping)
    #
    #     web = WebService()
    #     data = {}
    #     # print web.check_status('https://', 'google.com')
    #     platform = self.tool.get_platform()
    #     operation = ['ping', 'status']
    #     for protocol in web.protocols:
    #         for operate in operation:
    #             for url in web.host_list:
    #                 temp_url = url.split('.')
    #                 data[temp_url[0]] = web.choice_operation(func=operate, platform=platform,
    #                                                          protocol=web.protocols[protocol], url=url)
    #             self.f_database.put_data(self.node, 'webService/' + protocol + '/' + operate, data)
    #             data = {}
    #
    #     print " ----> WebTest Complete. <------", time.ctime(time.time())

    def web_service_new(self):

        web = WebService()
        data = []
        platform = self.tool.get_platform()
        protocols = web.protocols
        www_list = web.host_list

        for protocol in protocols:
            for www in www_list:
                temp_www = www.split('.')
                ping = web.ping_ip_address(platform=platform, url=www)
                status = web.check_status(protocol=protocols[protocol], url=www)
                temp_data = (self.node, temp_www[0], protocol, ping, status, self.current_date, self.current_time)
                data.append(temp_data)
            self.localDatabase.insert_data_speedtest(table='webService', list_data=data)
            data = []
        print ' ----------------> INSERT WEB SUCCESSFULLY <------------------'

    # def mail_service(self):
    #     protocols = ['smtp', 'imap', 'pop3']
    #     mail = EmailService()
    #     data = {}
    #
    #     for protocol in range(len(protocols)):
    #         for server in mail.mail_server:
    #             temp_server = str(server).replace('.', '-')
    #             data[temp_server] = mail.choice_connection(protocols[protocol], server,
    #                                                        mail.mail_server[server][protocol])
    #         self.f_database.put_data(self.node, 'mailService/' + protocols[protocol], data)
    #         data = {}

    def mail_service_new(self):
        # protocols = ['smtp', 'imap', 'pop3']
        mail = EmailService()
        data = []
        mail_server = mail.mail_server

        for server in mail_server:
            mail.connect_all(hostServer=server, port_smtp=mail_server[server][0], port_imap=mail_server[server][1])
            smtp, imap, pop3 = mail.status_all()
            # mail.terminate_all()
            temp_data = (self.node, server, 'smtp', smtp, self.current_date, self.current_time), \
                        (self.node, server, 'imap', imap, self.current_date, self.current_time), \
                        (self.node, server, 'pop3', pop3, self.current_date, self.current_time)
            data.extend(temp_data)
        self.localDatabase.insert_many_data_dns_mail(table='mailService', list_data=data)
        # mail.terminate_all()
        print ' ----------------> INSERT MAIL SUCCESSFULLY <------------------'

    # def mail_service(self):
    #     temp_smtp = {}
    #     temp_pop = {}
    #     temp_imap = {}
    #     mail = EmailService()
    #     print self.node
    #     for server in mail.mail_server:
    #         temp_server = str(server).replace('.', '-')
    #         port = mail.mail_server[server]
    #         print "Server: {}\nPort: {}".format(temp_server, port)
    #         mail.connect_both(server, port)
    #         print 'connect both success'
    #         smtp_status = mail.get_smtp_status()
    #         temp_smtp[temp_server] = smtp_status
    #         print 'SMTP both success'
    #         pop_status = mail.get_pop_status()
    #         temp_pop[temp_server] = pop_status
    #         print 'POP3 both success'
    #         mail.quit_both()
    #         print '-----------------------------/----------------------/-----------------'
    #         # try:
    #         #     # mail.connect_smtp_server(server, port)
    #         #     mail.connect_both(server, port)
    #         #     snmp_status = mail.get_smtp_status()
    #         #     pop_status = mail.get_pop_status()
    #         #     temp_smtp[temp_server] = snmp_status
    #         #     temp_pop[temp_server] = pop_status
    #         #     # mail.quit_smtp_connection()
    #         #     # mail.quit_both()
    #         #     # print server, mail.status, mail.code
    #         #     self.f_database.put_data(self.node, 'mailService/' + temp_server, mail.status)
    #         #     # self.f_database.put_data('testObj','main1', mail)
    #         # except Exception as e:
    #         #     print e
    #         #     print "\nCouldn't connect."
    #         #     self.f_database.put_data(self.node, 'mailService/' + temp_server, 'Cannot connect to server.')
    #     print 'FOR Finish'
    #     self.f_database.put_data(self.node, 'mailService/SMTP', temp_smtp)
    #     print 'temp_smtp success'
    #     self.f_database.put_data(self.node, 'mailService/POP3', temp_pop)
    #     print 'temp_smtp pop'

    # def dns_service(self):
    #     operation = ['ping', 'status']
    #     data = {}
    #     platform = self.tool.get_platform()
    #     dns_checker = DNSService()
    #
    #     for operate in range(len(operation)):
    #         print operation[operate]
    #         for dns in dns_checker.target:
    #             print dns
    #             temp_dns = str(dns).replace('.', '-')
    #             data[temp_dns] = dns_checker.__select_function__(func=operation[operate], platform=platform,
    #                                                              host='google.com',
    #                                                              dns_server=dns)
    #         print data
    #         self.f_database.put_data(self.node, 'DNSService/' + operation[operate], data)
    #         data = {}

    def dns_service_new(self):

        dns = DNSService()
        data = []
        platform = self.tool.get_platform()
        dns_server = dns.target

        for server in dns_server:
            ping = dns.__ping__(platform, server)
            status = dns.__get_nslookup_result__('google.com', server)
            temp_data = (self.node, server, ping, status, self.current_date, self.current_time)
            data.append(temp_data)
        self.localDatabase.insert_many_data_dns_mail('dnsService', data)
        print ' ----------------> INSERT DNS SUCCESSFULLY <------------------'

    def shopping_service_new(self):

        shopping = Shopping()
        data = []
        shopping_website = shopping.website_list

        for url in shopping_website:
            temp_url = url.replace('www.', '')
            status, expire_d = shopping.get_whois(temp_url)
            webpage_status = shopping.checkStatusHTTPS(url)
            temp_data = (self.node, temp_url, status, expire_d, webpage_status, self.current_date, self.current_time)
            data.append(temp_data)
        self.localDatabase.insert_data_speedtest('shoppingService', data)
        print ' ----------------> INSERT SHOPPING SUCCESSFULLY <------------------'

    @contextmanager
    def suppress_stdout(self):
        with open(os.devnull, "w") as devnull:
            old_stdout = sys.stdout
            sys.stdout = devnull
            try:
                yield
            finally:
                sys.stdout = old_stdout


def main():
    device = Service()
    # with device.suppress_stdout():
    #     device.new_speedtest()
    #     device.web_service_new()
    #     device.mail_service_new()
    #     device.dns_service_new()
    #     device.shopping_service_new()

    # device.speedtest()
    # device.web_service()
    # device.mail_service()
    # device.dns_service()

    # device.new_speedtest()
    device.web_service_new()
    # device.mail_service_new()
    # device.dns_service_new()
    # device.shopping_service_new()

    # try:
    #     while True:
    #         print time.ctime(time.time())
    #
    #         device.new_speedtest()
    #         device.web_service_new()
    #         device.mail_service_new()
    #         device.dns_service_new()
    #
    #         print time.ctime(time.time())
    #         time.sleep(100)
    # except KeyboardInterrupt:
    #     print 'Manual Break by User.'

    # device.new_speedtest()
    # End of Speedtest Function


# if __name__ == '__main__':
#     try:
#         while True:
#             main()
#             print time.ctime(time.time())
#             time.sleep(30)
#     except KeyboardInterrupt:
#         print 'Manual break by user'

if __name__ == '__main__':
    # print time.ctime(time.time())
    main()
    # print time.ctime(time.time())
# interval 5 mins.
# usage 1.5 kb firebaseR

# mail = EmailService()
#
# print mail.mail_server


# def main2():
#     node = 'KhoneKean'
#     data_dict = {}
#     f_database = FirebaseDatabase()
#     web = WebService()
#     # for protocol in web.protocols:
#     #     for url in web.host_list:
#     #         status, reason = web.check_status(web.protocols[protocol], url)
#     #         ping = web.ping_ip_address(url)
#     #         url = url.split('.')
#     #         data_dict[url[0]] = [status, reason, ping]
#     #     f_database.put_data(node, 'webService/' + protocol, data_dict)
#     #     data_dict = {}
#
#     temp_data_status = {}
#     temp_data_reason = {}
#     temp_data_ping = {}
#     for protocol in web.protocols:
#         for url in web.host_list:
#             status, reason = web.check_status(web.protocols[protocol], url)
#             ping = web.ping_ip_address(url)
#             temp_url = url.split('.')
#             temp_data_status[temp_url[0]] = status
#             temp_data_reason[temp_url[0]] = reason
#             temp_data_ping[temp_url[0]] = ping
#         f_database.put_data(node, 'webService/' + protocol + '/status', temp_data_status)
#         f_database.put_data(node, 'webService/' + protocol + '/reason', temp_data_reason)
#         f_database.put_data(node, 'webService/' + protocol + '/ping', temp_data_ping)
#
#
# main2()
