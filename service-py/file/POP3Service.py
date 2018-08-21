#!usr/bin/python

import Script
import poplib


class POP3Service(Script.Service):

    def __init__(self):
        Script.Service.__init__(self)
        self.availability_service('9')

    def get_status(self, destination, port):
        try:
            start = self.get_time()
            connection = poplib.POP3(destination, port)
            msg = connection.welcome
            end = self.get_time()
            connection.quit()

            response = self.get_response_time(start, end)

            if 'ok' and 'ready' in msg.lower():
                return 0, response
        except:
            try:
                start = self.get_time()
                connection = poplib.POP3_SSL(destination, port)
                msg = connection.welcome
                end = self.get_time()
                connection.quit()

                response = self.get_response_time(start, end)

                if 'ok' and 'ready' in msg.lower():
                    return 0, response
            except:
                return 2, 0


if __name__ == '__main__':
    service = POP3Service()
