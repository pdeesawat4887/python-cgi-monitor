#!usr/bin/python

import Script
import imaplib


class IMAPService(Script.Service):

    def __init__(self):
        Script.Service.__init__(self)
        self.availability_service('8')

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
