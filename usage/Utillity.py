class Utilities:

    def gettime_ntp(self, addr='time.nist.gov'):
        import socket
        import struct
        import time
        TIME1970 = 2208988800L  # Thanks to F.Lundh
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = '\x1b' + 47 * '\0'
        client.sendto(data, (addr, 123))
        data, address = client.recvfrom(1024)
        if data:
            t = struct.unpack('!12I', data)[10]
            t -= TIME1970
            return time.ctime(t)

    def convertTime(self, hunOfSec):
        # import datetime
        # return datetime.timedelta(milliseconds=(hunOfSec * 10))
        millis = int(hunOfSec) * 100
        seconds = (millis / 1000) % 60
        seconds = int(seconds)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)
        hours = (millis / (1000 * 60 * 60)) % 24
        return ("%d:%d:%d" % (hours, minutes, seconds))

    def humanize(self, milli):
        sec, milli = divmod(milli * 10, 1000)
        min, sec = divmod(sec, 60)
        hour, min = divmod(min, 60)
        day, hour = divmod(hour, 24)
        return ("%d day(s) %d hour(s) %d min(s) %d sec(s)" % (day, hour, min, sec))

    def convertStringToList(self, str):
        import ast
        temp = ast.literal_eval(str)
        temp = [n.strip() for n in temp]
        return temp

# tools = Utilities()
# time = tools.humanize(11557997560)
# # print tools.convertTime(1155772339)
# print time
