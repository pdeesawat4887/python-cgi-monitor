# import youtube_dl
#
# ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
#
# with ydl:
#     result = ydl.extract_info(
#         'http://www.youtube.com/watch?v=BaW_jenozKc',
#         download=True # We just want to extract the info
#     )
#
# if 'entries' in result:
#     # Can be a playlist or a list of videos
#     video = result['entries'][0]
# else:
#     # Just a video
#     video = result
#
# # print(video)
# # video_url = video['url']
# # print(video_url)

# from __future__ import unicode_literals
import youtube_dl


# class MyLogger(object):
#     def debug(self, msg):
#         pass
#
#     def warning(self, msg):
#         pass
#
#     def error(self, msg):
#         print(msg)


data = []


def my_hook(d):
    if d['status'] != 'finished':
        print d['speed']
        data.append(d['speed'])
        print data
        # for i in d:
        #     print i, "--->", d[i]


ydl_opts = {
    # 'logger': MyLogger(),
    'progress_hooks': [my_hook],
    # 'format': 'bestvideo'
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': '../video/sample.%(ext)s'
    # 'path': '../conf'
    # 'listformats': True,
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=0vrdgDdPApQ'])
    info = ydl.extract_info('https://www.youtube.com/watch?v=0vrdgDdPApQ', download=False)
#
# for i in info:
#     print i, '----- >',info[i]
print data

import os
import sys

name = '../video'
# dest = '../video_copy'
# os.system('cp -r {} {}'.format(name, dest))
os.system('rm -rf {}'.format(name))
    # print ydl.get_info_extractor()
    # meta = ydl.extract_info('https://www.youtube.com/watch?v=APAg1Ax1SrI', download=False)
    # status = meta.get('status', [meta])
    # for i in status:
    #     # print i['title']
    #     print i

# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     meta = ydl.extract_info(
#         'https://www.youtube.com/watch?v=9bZkp7q19f0', download=False)
#     formats = meta.get('formats', [meta])
# for f in formats:
#     print(f['ext'])
