#!usr/bin/python

import main.service as service
import smtplib


class SMTPService(service.Service):

    def __init__(self):
        service.Service.__init__(self)

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
    service.collect_service_data(service_id='7', type='availability_service')
