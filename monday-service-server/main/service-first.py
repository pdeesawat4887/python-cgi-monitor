#!/usr/bin/python

import database
import bitmath
import socket
import time


class Service:

    def __init__(self, service_id, probe_id, command):
        self.service_id = service_id
        self.probe_id = probe_id
        self.command = command
        self.db = database.MySQLDatabase()
        print self.collect_data()

    def query_destination(self):
        query_sql = """SELECT `destination_id`, `destination`, `destination_port`
        FROM DESTINATIONS WHERE `service_id`='{service_id}' and `destination_id` in (SELECT `destination_id`
        FROM RUNNING_DESTINATIONS WHERE running_dest_status=1 and probe_id='{probe_id}')""".format(service_id=self.service_id, probe_id=self.probe_id)
        return self.db.select(query_sql)

    def collect_data(self):

        info_test_result = []
        destinations = self.query_destination()
        time_insert = time.strftime('%Y-%m-%d %H:%M:%S')

        if len(destinations) == 0:
            return "No active destination in service: {}".format(self.service_id)
        else:
            for dest in destinations:
                temp_id = dest[0]
                temp_dest = dest[1]
                temp_port = dest[2]

                info_test = ('NULL', self.probe_id, temp_id, time_insert,)
                info_result = self.get_status(temp_dest, temp_port)

                info_test_result.append(info_test + info_result)

            self.db.insert('test_result', info_test_result)
            return "Successfully insert service: {}".format(self.service_id)

    def get_status(self, destination, port):

        output = "status={status_final}"

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print "socket creation failed with error %s" % (err)
            status_f = 3

        regex = {'http://': '', 'https://': ''}
        url = reduce(lambda a, kv: a.replace(*kv), regex.iteritems(), destination)

        try:
            host_ip = socket.gethostbyname(url)
        except socket.gaierror:
            status_f = 3

        s.settimeout(1)

        try:
            start_time = time.time()
            s.connect((host_ip, port))
            end_time = time.time()
            status_f = 1
            output += ", rtt={rtt}".format(rtt=end_time - start_time)
        except socket.timeout:
            status_f = 2
        finally:
            s.close()
            return output.format(status_final=status_f)

    def parse_parameter(self, stdout):
        dict_result = {'status': None,
                       'rtt': None,
                       'download': None,
                       'upload': None,
                       'other': None,
                       'other_description': None,
                       'other_unit': None,
                       }

        results = stdout.replace(' ', '').replace('\n', '').split(',')

        map(lambda item: dict_result.update({item.split('=')[0]: float(
            item.split('=')[1]) if 'none' not in item.lower() else None}), results)
        return dict_result


    def round_to_n_decimal(self, value, digit):
        return round(float(value), digit)

    def convert_bps_to_mbps(self, num_of_bytes):
        bit = bitmath.Byte(num_of_bytes)
        return bit.to_MiB().value
