#!/usr/bin/python

import database
import bitmath
import socket
import time
import subprocess


class Service:

    def __init__(self, service_id, probe_id, cluster_id, transport_protocol=None, file_cmd=None, file_name=None,
                 udp_cmd=None, path=None, **kwargs):
        self.service_id = service_id
        self.probe_id = probe_id
        self.cluster_id = cluster_id
        self.transport_protocol = transport_protocol
        self.file_cmd = file_cmd
        self.file_name = file_name
        self.udp_cmd = udp_cmd
        self.path = path
        self.db = database.MySQLDatabase()
        self.info_test_result = []  # list of data for insert
        self.collect_data()

    def get_active_destination(self):
        query_sql = """SELECT `destination_id`, `destination_name`, `destination_port` FROM DESTINATIONS 
        WHERE `service_id`='{isvc}' AND `destination_id` IN (SELECT `destination_id` FROM RUNNING_DESTINATIONS 
        WHERE `running_dest_status`='Active' AND `cluster_id`='{iclus}');""".format(isvc=self.service_id,
                                                                                    iclus=self.cluster_id)
        return self.db.select(query_sql)

    def collect_data(self):

        # print self.info_test_result
        destinations = self.get_active_destination()  # get all active destination
        self.start_date = time.strftime('%Y-%m-%d %H:%M:%S')  # get start_date for insert

        option_protocol = {
            'tcp': self.tcp_work,
            'udp': self.udp_work,
            'other': self.file_work,
        }

        if destinations:
            for destination in destinations:
                stdout = None
                temp_id = destination[0]
                temp_dest = destination[1]
                temp_port = destination[2]

                stdout = option_protocol[self.transport_protocol](temp_dest, temp_port)
                if stdout != None:
                    self.parse_parameter(temp_id, stdout)

            self.db.insert('TESTRESULTS', self.info_test_result)
            print "Successfully insert service: {svc_id}".format(svc_id=self.service_id)

        else:
            print "PLEASE INSERT DESTINATION IN SERVICE '{nsvc}'.".format(nsvc=self.db.select(
                "SELECT `service_name` FROM SERVICES WHERE `service_id`='{isvc}'".format(isvc=self.service_id))[0][0])

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
        except Exception:
            status_final = 3
        finally:
            s.close()
            return stdout.format(status_final=status_final)

    def file_work(self, destination, destination_port):
        process = subprocess.Popen(
            [self.file_cmd, self.path + '/' + self.file_name, destination, str(destination_port)],
            stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout

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

        pattern = (None, self.cluster_id, self.service_id, self.start_date, destination_id, dict_result['status'],
                   dict_result['rtt'], dict_result['download'], dict_result['upload'], dict_result['other'],
                   dict_result['other_description'], dict_result['other_unit'])

        self.info_test_result.append(pattern)

    # def round_to_n_decimal(self, value, digit):
    #     return round(float(value), digit)
    #
    # def convert_bps_to_mbps(self, num_of_bytes):
    #     bit = bitmath.Byte(num_of_bytes)
    #     return bit.to_MiB().value

# if __name__ == '__main__':
#     svc = Service(service_id='2', probe_id='zzzz', collection_id='asd123', transport_protocol='tcp')
