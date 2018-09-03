#!usr/bin/python

import main.service as service
import imaplib


class IMAPService(service.Service):

    def __init__(self):
        service.Service.__init__(self)

    def get_status(self, destination, port):
        try:
            start = self.get_time()
            connection = imaplib.IMAP4_SSL(destination, port)
            msg = connection.welcome
            end = self.get_time()
            connection.shutdown()

            response = self.get_response_time(start, end)

            if 'ok' and 'ready' in msg.lower():
                return 0, response
        except:
            try:
                start = self.get_time()
                connection = imaplib.IMAP4_SSL(destination, port)
                msg = connection.welcome
                end = self.get_time()
                connection.shutdown()

                response = self.get_response_time(start, end)

                if 'ok' and 'ready' in msg.lower():
                    return 0, response
            except:
                return 2, 0


if __name__ == '__main__':
    service = IMAPService()
    service.collect_service_data(service_id='8', type='availability_service')
