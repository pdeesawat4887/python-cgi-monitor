#!/usr/bin/python

import database
import bitmath
import socket
import time
import subprocess


class Service:

    def __init__(self, service_id, probe_id, collection_id, transport_protocol=None, file_cmd=None, file_name=None,
                 udp_cmd=None, path=None, **kwargs):
        self.service_id = service_id
        self.probe_id = probe_id
        self.collection_id = collection_id  ### do this
        self.transport_protocol = transport_protocol
        self.file_cmd = file_cmd
        self.file_name = file_name
        self.udp_cmd = udp_cmd
        self.path = path
        self.db = database.MySQLDatabase()
        self.collect_data()

    def query_destination(self):
        query_sql = """SELECT `destination_id`, `destination_name`, `destination_port`
        FROM DESTINATIONS WHERE `service_id`='{service_id}' AND `destination_id` IN (SELECT `destination_id`
        FROM RUNNING_DESTINATIONS WHERE `running_dest_status`=1 AND `collection_id`='{coll}')""".format(
            service_id=self.service_id, coll=self.collection_id)
        return self.db.select(query_sql)

    def collect_data(self):

        self.info_test_result = []  # list of data for insert
        # print self.info_test_result
        destinations = self.query_destination()  # get all active destination
        self.start_date = time.strftime('%Y-%m-%d %H:%M:%S')  # get start_date for insert

        for destination in destinations:
            stdout = None
            temp_id = destination[0]
            temp_dest = destination[1]
            temp_port = destination[2]

            # check external file first
            if self.file_name != None:
                process = subprocess.Popen([self.file_cmd, self.path + '/' + self.file_name, temp_dest,
                                            "{temp_port}".format(temp_port=temp_port)],
                                           stdout=subprocess.PIPE)
                stdout, stderr = process.communicate()
            elif self.transport_protocol.lower() == 'udp':
                stdout = self.udp_work(temp_dest, temp_port)  # create already
            elif self.transport_protocol.lower() == 'tcp':
                stdout = self.tcp_work(temp_dest, temp_port)  # create already

            # print "-----------------------> ", stdout.replace('\n', '')
            # print "-----------------------END---------------------"
            if stdout != None:
                self.parse_parameter(temp_id, stdout)

        # print self.info_test_result
        self.db.insert('TESTRESULTS', self.info_test_result)
        print "Successfully insert service: {svc_id}".format(svc_id=self.service_id)

    def udp_work(self, destination, destination_port):
        stdout = "status={status_final}"

        msg_from_client = self.udp_cmd
        bytes_to_send = str.encode(msg_from_client)
        server_address_port = (destination, destination_port)
        buffer_size = 1024

        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPClientSocket.settimeout(1)

        start_time = time.time()
        UDPClientSocket.sendto(bytes_to_send, server_address_port)

        try:
            msg_from_server = UDPClientSocket.recvfrom(buffer_size)
            end_time = time.time()
            status_final = 1
            stdout += ', rtt={rtt}'.format(rtt=end_time - start_time)
        except:
            status_final = 3
        finally:
            UDPClientSocket.close()

        return stdout.format(status_final=status_final)

    def tcp_work(self, destination, destination_port):
        stdout = "status={status_final}"

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print "socket creation failed with error %s" % (err)
            status_final = 3

        regex = {'http://': '', 'https://': ''}
        destination = reduce(lambda a, kv: a.replace(*kv), regex.iteritems(), destination)

        try:
            host_ip = socket.gethostbyname(destination)
        except socket.gaierror:
            status_final = 3

        s.settimeout(1)

        try:
            start_time = time.time()
            s.connect((host_ip, destination_port))
            end_time = time.time()
            status_final = 1
            stdout += ", rtt={rtt}".format(rtt=(end_time - start_time) * 1000)
        except socket.timeout:
            status_final = 2
        finally:
            s.close()
            return stdout.format(status_final=status_final)

    def parse_parameter(self, destination_id, stdout):  # be improve to return tuple of insert
        dict_result = {'status': None,
                       'rtt': None,
                       'download': None,
                       'upload': None,
                       'other': None,
                       'other_description': None,
                       'other_unit': None,
                       }

        # print stdout
        results = stdout.replace(' ', '').replace('\n', '').split(',')
        # print results

        map(lambda item: dict_result.update(
            {item.split('=')[0]: item.split('=')[1] if 'none' not in item.lower() else None}), results)

        pattern = (None, self.collection_id, self.service_id, self.start_date, destination_id, dict_result['status'],
                   dict_result['rtt'], dict_result['download'], dict_result['upload'], dict_result['other'],
                   dict_result['other_description'], dict_result['other_unit'])

        self.info_test_result.append(pattern)

    def round_to_n_decimal(self, value, digit):
        return round(float(value), digit)

    def convert_bps_to_mbps(self, num_of_bytes):
        bit = bitmath.Byte(num_of_bytes)
        return bit.to_MiB().value

# if __name__ == '__main__':
#     svc = Service(service_id='2', probe_id='zzzz', collection_id='asd123', transport_protocol='tcp')
