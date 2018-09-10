#!usr/bin/python

import __Service__
import imaplib


class IMAPService(__Service__.Service):

    def __init__(self):
        __Service__.Service.__init__(self)

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
    service.close_connection()
