#!/usr/bin/python

import main.service as service_cl
import platform
import subprocess
import re
import sys


class PingTest(service_cl.Service):

    def get_status(self, destination, port):
        param = '-n' if platform.system().lower() == 'windows' else '-c'

        command = ['ping', param, '4', destination]

        try:
            output = subprocess.check_output(command)
            return self.response_time(output)
        except:
            return 2, None, None, None

    def response_time(self, output):
        response = None
        try:
            searchObj = re.search(r'min/avg/max/(.*) = (.*)/(.*)/(.*)/(.*)ms', output, re.M | re.I)
            response = float(searchObj.group(3))
        except:
            searchObj = re.search(r'Average = (.*)ms', output, re.M | re.I)
            response = float(searchObj.group(1))
        finally:
            if response >= 1000:
                return 1, response, None, None
            else:
                return 0, response, None, None


if __name__ == '__main__':
    example = PingTest(sys.argv[1], sys.argv[2], sys.argv[3])
