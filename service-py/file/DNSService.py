#!usr/bin/python

import Script
import subprocess


class DNSService(Script.Service):

    def __init__(self):
        Script.Service.__init__(self)
        self.availability_service('2')

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
