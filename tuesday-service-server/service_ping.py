#!/usr/bin/python

import platform
import subprocess
import re
import shlex


class PingTest:

    def __init__(self, destination, destination_port):
        self.get_status(destination)

    def get_status(self, destination):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = "ping {param} 4 {destination}".format(param=param, destination=destination)
        process = subprocess.Popen(shlex.split(command), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output, stderr = process.communicate()

        if len(output) == 0:
            print  "status={status}".format(status=3)
        else:
            print self.response_time(output)

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
                return "status={status}".format(status=2)
            else:
                return "status={status}, rtt={rtt}".format(status=1, rtt=response)


if __name__ == '__main__':
    # example = PingTest(sys.argv[1], sys.argv[2])
    example = PingTest('www.google.com', 0)
