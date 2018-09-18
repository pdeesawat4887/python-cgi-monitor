#!/usr/bin/python

from __future__ import unicode_literals
import main.service as service_cl
import os
import sys
import youtube_dl


class Youtube_downloader(service_cl.Service):
    data_speed = []

    def collect_video_data(self, result):
        if result['status'] != 'finished':
            speed = result['speed']
            if isinstance(speed, float):
                self.data_speed.append(speed)

    def get_status(self, destination, port):
        opts = {
            'progress_hooks': [self.collect_video_data],
            'format': 'best[height<=?1080]',
            'outtmpl': sys.path[0] + '/video/sample.%(ext)s'
        }

        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download([destination])

            avg = sum(self.data_speed) / float(len(self.data_speed))

            name = sys.path[0] + '/video'
            os.system('rm -rf {}'.format(name))

            self.data_speed = []

            avg = self.round_to_n_decimal(self.convert_bps_to_mbps2(avg), 6)

        return 0, None, avg, None

if __name__ == '__main__':
    service = Youtube_downloader(sys.argv[1], sys.argv[2], sys.argv[3])
