#!/usr/bin/python

from __future__ import unicode_literals
import os
import sys
import youtube_dl


class YoutubeDownloader:

    def __init__(self, destination, destination_port):
        self.data_speed = []
        self.output = None
        self.get_status(destination)


    def collect_video_data(self, result):
        if result['status'] != 'finished':
            speed = result['speed']
            if isinstance(speed, float):
                self.data_speed.append(speed)

    def get_status(self, destination):
        sys.stdout = open(os.devnull, 'w')
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

            # avg = self.round_to_n_decimal(self.convert_bps_to_mbps(avg), 6)

        self.output = "status=1, upload={avg_upload}".format(avg_upload=avg)

if __name__ == '__main__':
    service = YoutubeDownloader(sys.argv[1], sys.argv[2])
    # service = YoutubeDownloader("https://www.youtube.com/watch?v=1O2NlSRb-6o", 0)
    sys.stdout = sys.__stdout__
    # print service.output


