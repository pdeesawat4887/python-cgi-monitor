import speedtest
import time
import socket
import struct
from firebase import firebase
import sched


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

class Service:

    def speedtest(self):
        tool = Tools()
        print "tools success"
        micro = SpeedTestPy()
        print "SpeedtestPy success"
        node = micro.setting['node']
        print "node query success"
        f_database = FirebaseDatabase()
        print "firebase success"
        test_time = micro.server_list
        print "num of server success"

        # Speedtest Function
        for i in range(len(test_time)):
            print "in for success"
            name, d, u, p, execTime = micro.test(test_time[i])
            print "test success"
            d, du = tool.convert(d)
            print "convert dw success"
            u, uu = tool.convert(u)
            print "convert ul success"
            st_time = time.ctime(time.time())  # change to ntp time
            print "convert ntp success"
            data = {'download': (d, du), 'upload': (u, uu), 'ping': p, 'execTime': execTime, 'time': st_time}
            print "convert data success"
            # f_database.put_data('speedtest', node + '/' + name, data)
            f_database.post_data(node + '/speedtest/' + name, data)
            print "convert post firebase success"

            # Show output
            print 'Time Start Speedtest: {}'.format(st_time)
            # print 'Test #{}'.format(i + 1)
            # print 'Download: {:.2f} {}'.format(d, du)
            # print 'Upload: {:.2f} {}'.format(u, uu)
            # print 'Ping: {}'.format(p)
            # print 'Execute Time: {}'.format(execTime)
        # End of Speedtest Function


def main():

    speed = Service()
    speed.speedtest()
    # tool = Tools()
    # print "tools success"
    # micro = SpeedTestPy()
    # print "SpeedtestPy success"
    # node = micro.setting['node']
    # print "node query success"
    # f_database = FirebaseDatabase()
    # print "firebase success"
    # test_time = micro.server_list
    # print "num of server success"
    #
    # # Speedtest Function
    # for i in range(len(test_time)):
    #     print "in for success"
    #     name, d, u, p, execTime = micro.test(test_time[i])
    #     print "test success"
    #     d, du = tool.convert(d)
    #     print "convert dw success"
    #     u, uu = tool.convert(u)
    #     print "convert ul success"
    #     st_time = time.ctime(time.time())               # change to ntp time
    #     print "convert ntp success"
    #     data = {'download': (d, du), 'upload': (u, uu), 'ping': p, 'execTime': execTime, 'time': st_time}
    #     print "convert data success"
    #     # f_database.put_data('speedtest', node + '/' + name, data)
    #     f_database.post_data(node + '/speedtest/' + name, data)
    #     print "convert post firebase success"
    #
    #     # Show output
    #     print 'Time Start Speedtest: {}'.format(st_time)
    #     # print 'Test #{}'.format(i + 1)
    #     # print 'Download: {:.2f} {}'.format(d, du)
    #     # print 'Upload: {:.2f} {}'.format(u, uu)
    #     # print 'Ping: {}'.format(p)
    #     # print 'Execute Time: {}'.format(execTime)
    # # End of Speedtest Function


if __name__ == '__main__':
    try:
        while True:
            main()
            time.sleep(300)
    except KeyboardInterrupt:
        print 'Manual break by user'

# interval 5 mins.
# usage 1.5 kb firebase