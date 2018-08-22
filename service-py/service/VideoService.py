#!usr/bin/python

import Script
import os
import youtube_dl


class VideoService(Script.Service):
    data_speed = []

    def __init__(self):
        Script.Service.__init__(self)
        self.performance_service('6')

    def collect_data(self, result):
        if result['status'] != 'finished':
            speed = result['speed']
            if isinstance(speed, float):
                self.data_speed.append(speed)

    def get_status(self, destination, port):
        opts = {
            'progress_hooks': [self.collect_data],
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '../video/sample.%(ext)s'
        }

        with youtube_dl.YoutubeDL(opts) as ydl:
            ydl.download([destination])

            avg = sum(self.data_speed) / float(len(self.data_speed))

            name = '../video'
            os.system('rm -rf {}'.format(name))

            self.data_speed = []

        return 'NULL', avg, 'NULL', 'NULL'


if __name__ == '__main__':
    service = VideoService()
