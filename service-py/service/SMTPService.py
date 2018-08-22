#!usr/bin/python

import Script
import smtplib


class SMTPService(Script.Service):

    def __init__(self):
        Script.Service.__init__(self)
        self.availability_service('7')

    def get_status(self, destination, port):
        try:
            start = self.get_time()
            connection = smtplib.SMTP()
            connection.connect(destination, port)

            end = self.get_time()

            status = self.check_response_code(connection.helo()[0])
            response = self.get_response_time(start, end)

            connection.close()
            return status, response
        except:
            return 2, 0


if __name__ == '__main__':
    service = SMTPService()
