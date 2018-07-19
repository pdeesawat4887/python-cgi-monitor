# x = {'apple': [123, 456, 789, 'hello'], 'banana': [696969]}
#
# for it in x:
# 	for nn in x[it]:
# 		print nn
#
#
# def create_dict(dict, file):
#     with open(file) as f:
#         for line in f:
#             key, value = line.strip().split()
#             dict[key] = value.split(',')
#
# dict_oid = {}
# create_dict(dict_oid, "oid_list.txt")
#
# print dict_oid
#
# for it in dict_oid:
# 	for nn in dict_oid[it]:
# 		print nn
#
# num = 15
# print type(num)
#
# num = str(num)
# print num
# print type(num)

# class Hello():
#
#     def __init__(self, id):
#         self.id = id
#
#     def test(self):
#         print "Hello, Class Hello"
#
# objs = [Hello(i) for i in range(5)]
#
#
#     print i.id

#
# import ast
# list = '["192.168.1.5","192.168.1.8"]'
# x = ast.literal_eval(list)
# x = [n.strip() for n in x]
#
# for i in x:
#     print i

def gettime_ntp(addr='time.nist.gov'):
    # http://code.activestate.com/recipes/117211-simple-very-sntp-client/
    import socket
    import struct
    import sys
    import time
    TIME1970 = 2208988800L      # Thanks to F.Lundh
    client = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    data = '\x1b' + 47 * '\0'
    client.sendto( data, (addr, 123))
    data, address = client.recvfrom( 1024 )
    if data:
        t = struct.unpack( '!12I', data )[10]
        t -= TIME1970
        return time.ctime(t)

time = gettime_ntp()
print time