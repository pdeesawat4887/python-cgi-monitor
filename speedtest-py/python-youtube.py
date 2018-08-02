from pytube import YouTube

yt = YouTube("https://www.youtube.com/watch?v=RBumgq5yVrA")
# yt = yt.get('mp4', '720p')
# yt.download('/conf')
stream = yt.streams.first()
stream.download()