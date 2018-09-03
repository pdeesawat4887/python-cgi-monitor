#!usr/bin/python

from __future__ import unicode_literals
import main.service as service
import os
import youtube_dl


class VideoService(service.Service):
    data_speed = []

    def __init__(self):
        service.Service.__init__(self)

    def collect_data(self, result):
        if result['status'] != 'finished':
            speed = result['speed']
            if isinstance(speed, float):
                self.data_speed.append(speed)

    def get_status(self, destination, port):
        opts = {
            'progress_hooks': [self.collect_data],
            'format': 'best[height<=?1080]',
            'outtmpl': self.path + '/video/sample.%(ext)s'
        }

        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download([destination])

            avg = sum(self.data_speed) / float(len(self.data_speed))

            name = self.path + '/video'
            os.system('rm -rf {}'.format(name))

            self.data_speed = []

        return 'NULL', avg, 'NULL', 'NULL'


if __name__ == '__main__':
    service = VideoService()
    service.collect_service_data(service_id='6', type='performance_service')