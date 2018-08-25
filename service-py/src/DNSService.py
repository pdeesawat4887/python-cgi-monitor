#!usr/bin/python

import __Service__
import subprocess


class DNSService(__Service__.Service):

    def __init__(self):
        __Service__.Service.__init__(self)

    def get_status(self, destination, port):

        command = ['dig', '@' + destination, 'www.google.com']
        status = 1
        response = 0

        try:
            output = subprocess.check_output(command).split('\n')
            for element in output:
                if 'query time' in element.lower():
                    status = 0
                    response = element.split()[3]
        except:
            status = 2
            response = 0

        return status, response


if __name__ == '__main__':
    service = DNSService()
    service.collect_service_data(service_id='2', type='availability_service')
    service.close_connection()
