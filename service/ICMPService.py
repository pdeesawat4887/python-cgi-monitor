#!usr/bin/python

import main.service as service
import subprocess
import sys


class ICMPService(service.Service):

    def __init__(self):
        service.Service.__init__(self)

    def get_status(self, destination, port):

        param = '-n' if sys.platform.lower() == 'windows' else '-c'
        command = ['ping', param, '4', destination]
        status = 1
        response = 0

        try:
            output = subprocess.check_output(command).split('\n')
            for element in output:
                if 'min/avg/max/' in element.lower():
                    status = 0
                    response = element.split('/')[-3]
                elif 'average' in element.lower():
                    status = 0
                    response = element.split()[-1][:-2:]

        except:
            status = 2
            response = 0

        return status, response

    def format_destination(self, destination):
        return self.identify_url(destination).netloc


if __name__ == '__main__':
    service = ICMPService()
    service.collect_service_data(service_id='1', type='availability_service')
