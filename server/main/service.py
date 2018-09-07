#!/usr/bin/python

import time
import urlparse
import bitmath
from pip._vendor.colorama import Fore, Style
import probe


class Service(probe.Probe):

    def __init__(self):
        probe.Probe.__init__(self)

    def check_response_code(self, response_code):
        ''' Reference from HTTP status code return 0 if status = 2xx, return 1 if invalid or error status and return 2
        if status = 4xx-5xx or fail to connection '''
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
        ''' Return time format for database like 2018-08-01 09:06:09 '''
        return time.strftime('%Y-%m-%d %H:%M:%S')

    def get_time(self):
        ''' Return current time '''
        return time.time()

    def get_response_time(self, start, end):
        ''' Return different milli second from 2 different time'''
        return (end - start) * 1000

    def round_2_decimal(self, value):
        ''' Return the floating point value number rounded to 2 digits after the decimal point form input '''
        try:
            return round(float(value), 2)
        except:
            return None

    def identify_url(self, url):
        ''' Return 6 tuple correspond to general structure of a URL '''
        return urlparse.urlparse(url)

    def convert_to_mbs(self, number_of_bytes):
        ''' Return Megabit per second from byte per second '''
        try:
            bit = bitmath.Bit(number_of_bytes)
            return bit.to_Mib()
        except:
            return None

    def collect_service_data(self, service_id, type):
        data_for_database = []
        condition = " service_id = %s"
        my_result = self.select('destination', condition, '*', service_id=service_id)
        time_start = self.get_time_format()

        for counter in my_result:
            counter = list(counter)
            destination_id = counter[0]
            dest = counter[2]
            dest_port = counter[3]

            destination = self.format_destination(dest)

            if type == 'availability_service':
                status, response = self.get_status(destination, dest_port)
                response = self.round_2_decimal(response)
                temp = (None, self.id, destination_id, status, response, time_start)
            else:
                ping, download, upload, location = self.get_status(destination, dest_port)
                download = self.round_2_decimal(self.convert_to_mbs(download))
                upload = self.round_2_decimal(self.convert_to_mbs(upload))
                temp = (None, self.id, destination_id, ping, download, upload, location, time_start)

            data_for_database.append(temp)
        self.insert(type, data_for_database)
        print "SUCCESS INSERT DATA", service_id

    def get_status(self, destination, port):
        pass

    def format_destination(self, destination):
        return destination
