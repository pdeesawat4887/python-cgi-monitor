#!usr/bin/python

import __Service__
import poplib


class POP3Service(__Service__.Service):

    def __init__(self):
        __Service__.Service.__init__(self)

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
    service.collect_service_data(service_id='9', type='availability_service')
    service.close_connection()
