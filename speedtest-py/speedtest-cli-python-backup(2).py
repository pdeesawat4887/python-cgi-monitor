import speedtest
import time
import struct
from firebase import firebase
import socket
import os
import httplib
import urllib
import smtplib
import poplib
import imaplib
import sys


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

        return number_of_bytes, unit

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
            'linux1': 'Linux',
            'linux2': 'Linux',
            'darwin': 'OS X',
            'win32': 'Windows'
        }
        if sys.platform not in platforms:
            return sys.platform

        return platforms[sys.platform]

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
        start_time = time.time()
        s = speedtest.Speedtest()
        s.get_servers([server])
        name = s.get_servers([server]).values()[0][0]['name']
        s.get_best_server()
        s.download()
        s.upload()
        res = s.results.dict()
        return name, res["download"], res["upload"], res["ping"], (time.time() - start_time)

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

    def read_url(self, file='conf/hosts.txt'):
        with open(file, 'r') as temp_file:
            text = temp_file.read()
            self.host_list = text.split()
            temp_file.close()

    def ping_ip_address(self, url):
        try:
            ip_address = socket.gethostbyname(url)
            ping_value = os.system("ping -c 1 -i 0.1 " + ip_address)
            if ping_value == 0:
                ping_status = 'Active'
            else:
                ping_status = 'Check server first'
        except Exception as ex:
            ping_status = 'Cannot ping to destination'
        return ping_status

    def check_status(self, protocol, url):
        try:
            res_https = urllib.urlopen(protocol + url)
            status = res_https.getcode()
            reason = httplib.responses[status]
            res_https.close()
        except Exception as ex:
            status = 'Could not connect to page.'
            reason = 'Could not connect to page.'
        return status, reason


class EmailService:
    mail_server = {}
    emails = []

    def __init__(self):
        self.read_server()

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

        if (200 <= check <= 299):
            status = 'Working'
        else:
            status = 'Not Working'

        return status

    def connect_imap_server(self, hostServer, port):
        try:
            self.server = imaplib.IMAP4_SSL(hostServer, port)
        except Exception as e:
            self.server = imaplib.IMAP4(hostServer, port)

    def get_imap_status(self):

        check = self.server.welcome

        if 'OK' in check:
            status = 'Working'
        else:
            status = 'Not Working'

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


class Service:

    def __init__(self):
        self.tool = Tools()
        self.speed = SpeedTestPy()
        self.node = self.speed.setting['node']
        # self.f_database = FirebaseDatabase(url='https://pythontestcode.firebaseio.com/')
        self.f_database = FirebaseDatabase()

    def speedtest(self):
        # tool = Tools()
        # print "tools success"
        # micro = SpeedTestPy()
        # print "SpeedtestPy success"
        # node = self.speed.setting['node']
        # print "node query success"
        # f_database = FirebaseDatabase()
        # print "firebase success"
        test_time = self.speed.server_list
        # print "num of server success"

        # Speedtest Function
        for i in range(len(test_time)):
            # print "in for success"
            name, d, u, p, execTime = self.speed.test(test_time[i])
            # print "test success"
            d, du = self.tool.convert(d)
            # print "convert dw success"
            u, uu = self.tool.convert(u)
            # print "convert ul success"
            st_time = time.ctime(time.time())  # change to ntp time
            # print "convert ntp success"
            data = {'download': (d, du), 'upload': (u, uu), 'ping': p, 'execTime': execTime, 'time': st_time}
            # print "convert data success"
            # f_database.put_data('speedtest', node + '/' + name, data)
            self.f_database.post_data(self.node + '/speedtest/' + name, data)
            # print "convert post firebase success"

            # Show output
            # print 'Time Start Speedtest: {}'.format(st_time)
            # print 'Test #{}'.format(i + 1)
            # print 'Download: {:.2f} {}'.format(d, du)
            # print 'Upload: {:.2f} {}'.format(u, uu)
            # print 'Ping: {}'.format(p)
            # print 'Execute Time: {}'.format(execTime)
        # End of Speedtest Function
        print " ----> SpeedTest Complete. <------", time.ctime(time.time())

    def web_service(self):
        temp_data_status = {}
        temp_data_reason = {}
        temp_data_ping = {}
        web = WebService()
        for protocol in web.protocols:
            for url in web.host_list:
                print url
                status, reason = web.check_status(web.protocols[protocol], url)
                print "complete url"
                ping = web.ping_ip_address(url)
                temp_url = url.split('.')
                temp_data_status[temp_url[0]] = status
                temp_data_reason[temp_url[0]] = reason
                temp_data_ping[temp_url[0]] = ping
            self.f_database.put_data(self.node, 'webService/' + protocol + '/status', temp_data_status)
            self.f_database.put_data(self.node, 'webService/' + protocol + '/reason', temp_data_reason)
            self.f_database.put_data(self.node, 'webService/' + protocol + '/ping', temp_data_ping)
        print " ----> WebTest Complete. <------", time.ctime(time.time())

    def mail_service(self):

        protocols = ['smtp', 'imap', 'pop3']
        mail = EmailService()
        data = {}

        for protocol in range(len(protocols)):
            for server in mail.mail_server:
                temp_server = str(server).replace('.', '-')
                data[temp_server] = mail.choice_connection(protocols[protocol], server,
                                                           mail.mail_server[server][protocol])
            self.f_database.put_data(self.node, 'mailServer/' + protocols[protocol], data)
            data = {}

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


def main():
    device = Service()
    device.speedtest()
    device.web_service()
    device.mail_service()
    # End of Speedtest Function


if __name__ == '__main__':
    try:
        while True:
            main()
            time.sleep(300)
    except KeyboardInterrupt:
        print 'Manual break by user'

# interval 5 mins.
# usage 1.5 kb firebase


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
