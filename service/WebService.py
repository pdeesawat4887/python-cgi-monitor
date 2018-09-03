#!usr/bin/python

import main.service as service
import requests


class WebService(service.Service):

    def __init__(self):
        service.Service.__init__(self)

    def get_status(self, destination, port):
        header = {'User-Agent': self.setting['User-Agent']}
        try:
            res_http = requests.get(destination, headers=header)
            status_code = res_http.status_code
            timer = res_http.elapsed.total_seconds() * 1000
            res_http.close()
            status = self.check_response_code(status_code)
            return status, timer
        except:
            return 2, 0


if __name__ == '__main__':
    service = WebService()
    service.collect_service_data(service_id='4', type='availability_service')
