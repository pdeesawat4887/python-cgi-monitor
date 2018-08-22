#!usr/bin/python

import Script
import speedtest


class SpeedtestService(Script.Service):

    def __init__(self):
        Script.Service.__init__(self)
        self.performance_service('5')

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
