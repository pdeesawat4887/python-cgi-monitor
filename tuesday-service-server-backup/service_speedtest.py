#!/usr/bin/python

import sys
import speedtest


class SpeedtestResult:

    def __init__(self, destination, port):
        self.get_status(destination)

    def get_status(self, destination):
        try:
            client = speedtest.Speedtest()
            client.get_servers([destination])
            client.get_best_server()
            client.download()
            client.upload()
            result = client.results.dict()
            ping = result['ping']
            download = result['download']
            upload = result['upload']

            print "status=1, rtt={ping}, download={dl}, upload={ul}".format(ping=ping, dl=download, ul=upload)
        except:
            print "status=3"


if __name__ == '__main__':
    speed = SpeedtestResult(sys.argv[1], sys.argv[2])
    # xxx = SpeedtestResult('2054', 0)
