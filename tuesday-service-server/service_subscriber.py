#!/usr/bin/python

import sys
import telnetlib
import re

class Subscriber:

    def __init__(self, destination, destination_port):
        self.get_subscriber(destination, destination_port)

    def get_subscriber(self, destination, port):

        host = destination
        pswd_en = "cisco"

        try:
            tn = telnetlib.Telnet(host, 24)
        except:
            tn = telnetlib.Telnet(host, port)
        finally:
            tn.write("enable\n")
            tn.read_until("Password: ")
            tn.write(pswd_en + "\n")
            tn.write("sh int LineCard 0 subscriber all-names | i subscribers\n")
            tn.write("exit\n")
            output = tn.read_all()
            tn.close()
        try:
            searchObj = re.search(r'There are (.*) subscribers', output, re.M | re.I)
            response = int(searchObj.group(1))
            print "status=1, other={sub}, other_unit=user, other_description=AAA_Subscribers".format(sub=response)
        except Exception as error:
            print "status=3"

if __name__ == '__main__':
    subscriber = Subscriber(sys.argv[1], sys.argv[2])