#!usr/bin/python

import __Service__
import speedtest


class SpeedtestService(__Service__.Service):

    def __init__(self):
        __Service__.Service.__init__(self)

    def get_status(self, destination, port):
        try:
            clinet = speedtest.Speedtest()
            clinet.get_servers([destination])
            clinet.get_best_server()
            clinet.download()
            clinet.upload()
            result = clinet.results.dict()
            return result['ping'], result['download'], result['upload'], result['server']['name']
        except:
            print "Error"
            return 0, 0, 0, 'NULL'


if __name__ == '__main__':
    service = SpeedtestService()
    service.collect_service_data(service_id='5', type='performance_service')
    service.close_connection()
