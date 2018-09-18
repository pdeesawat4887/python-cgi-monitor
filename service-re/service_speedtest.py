#!/usr/bin/python

import main.service as service_cl
import sys
import speedtest


class Speedtest(service_cl.Service):

    def get_status(self, destination, port):
        try:
            client = speedtest.Speedtest()
            client.get_servers([destination])
            client.get_best_server()
            client.download()
            client.upload()
            result = client.results.dict()
            status = 0
            ping = result['ping']

            download = self.round_to_n_decimal(self.convert_bps_to_mbps(result['download']), 6)
            upload = self.round_to_n_decimal(self.convert_bps_to_mbps(result['upload']), 6)

            return status, ping, download, upload
        except:
            return 2, None, None, None


if __name__ == '__main__':
    xxx = Speedtest(sys.argv[1], sys.argv[2], sys.argv[3])
