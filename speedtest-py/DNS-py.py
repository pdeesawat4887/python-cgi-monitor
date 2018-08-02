import os
import subprocess
import firebase
import socket
import struct
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
            'linux1': '-c ',
            'linux2': '-c ',
            'darwin': '-c ',
            'win32': '-n '
        }
        if sys.platform not in platforms:
            return sys.platform

        return platforms[sys.platform]


class FirebaseDatabase:

    def __init__(self, url):
        self.connection = firebase.FirebaseApplication(url)

    def put_data(self, table, path, data):
        self.connection.put(table, path, data)

    def post_data(self, path, data):
        self.connection.post(path, data)


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

    def __get_nslookup_result__(self, platform, host, dns_server):
        result = self.__nslookup__(host, dns_server)
        return self.__check_nslookup_result__(result)

    def __ping__(self, platform, host, dns_server):
        try:
            ping = os.system("ping " + platform + "1 " + dns_server)
            if ping == 0:
                ping_status = 'Active'
            else:
                ping_status = 'Check server first'
        except Exception as ex:
            ping_status = 'Cannot ping to destination'
        return ping_status

    def __select_function__(self, func, platform, host, dns_server):
        operation = {'ping': self.__ping__, 'status': self.__get_nslookup_result__}
        temp = operation[func](platform, host, dns_server)
        return temp


node = 'AngThong'

f_database = FirebaseDatabase(url='https://pythontestcode.firebaseio.com/')

checker = DNSService()

tool = Tools()

operation = ['ping', 'status']

data = {}

platform = tool.get_platform()

for operate in range(len(operation)):
    print operation[operate]
    for dns in checker.target:
        print dns
        temp_dns = str(dns).replace('.', '-')
        data[temp_dns] = checker.__select_function__(func=operation[operate], platform=platform, host='google.com',
                                                     dns_server=dns)
    print data
    f_database.put_data(node, 'DNSService/' + operation[operate], data)
    data = {}

# print checker.target
# for i in checker.target:
#     print checker.__ping__(i, '-c ')
