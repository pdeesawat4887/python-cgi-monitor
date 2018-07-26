import speedtest
import time
import struct
from firebase import firebase
import socket
import os
import httplib
import urllib


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

    def load_setting(self, file='setting.txt'):
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

    def read_url(self, file='hosts.txt'):
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


class Service:

    def __init__(self):
        self.tool = Tools()
        self.speed = SpeedTestPy()
        self.node = self.speed.setting['node']

    def speedtest(self):
        # tool = Tools()
        # print "tools success"
        # micro = SpeedTestPy()
        # print "SpeedtestPy success"
        # node = self.speed.setting['node']
        # print "node query success"
        f_database = FirebaseDatabase()
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
            f_database.post_data(self.node + '/speedtest/' + name, data)
            # print "convert post firebase success"

            # Show output
            # print 'Time Start Speedtest: {}'.format(st_time)
            # print 'Test #{}'.format(i + 1)
            # print 'Download: {:.2f} {}'.format(d, du)
            # print 'Upload: {:.2f} {}'.format(u, uu)
            # print 'Ping: {}'.format(p)
            # print 'Execute Time: {}'.format(execTime)
        # End of Speedtest Function


def main():
    speed = Service()
    speed.speedtest()
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


def main2():
    node = 'KhoneKean'
    data_dict = {}
    f_database = FirebaseDatabase()
    web = WebService()
    # for protocol in web.protocols:
    #     for url in web.host_list:
    #         status, reason = web.check_status(web.protocols[protocol], url)
    #         ping = web.ping_ip_address(url)
    #         url = url.split('.')
    #         data_dict[url[0]] = [status, reason, ping]
    #     f_database.put_data(node, 'webService/' + protocol, data_dict)
    #     data_dict = {}

    temp_data_status = {}
    temp_data_reason = {}
    temp_data_ping = {}
    for protocol in web.protocols:
        for url in web.host_list:
            status, reason = web.check_status(web.protocols[protocol], url)
            ping = web.ping_ip_address(url)
            temp_url = url.split('.')
            temp_data_status[temp_url[0]] = status
            temp_data_reason[temp_url[0]] = reason
            temp_data_ping[temp_url[0]] = ping
        f_database.put_data(node, 'webService/' + protocol + '/status', temp_data_status)
        f_database.put_data(node, 'webService/' + protocol + '/reason', temp_data_reason)
        f_database.put_data(node, 'webService/' + protocol + '/ping', temp_data_ping)


main2()
