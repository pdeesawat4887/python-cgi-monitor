# # x = {'apple': [123, 456, 789, 'hello'], 'banana': [696969]}
# #
# # for it in x:
# # 	for nn in x[it]:
# # 		print nn
# #
# #
# # def create_dict(dict, file):
# #     with open(file) as f:
# #         for line in f:
# #             key, value = line.strip().split()
# #             dict[key] = value.split(',')
# #
# # dict_oid = {}
# # create_dict(dict_oid, "oid_list.txt")
# #
# # print dict_oid
# #
# # for it in dict_oid:
# # 	for nn in dict_oid[it]:
# # 		print nn
# #
# # num = 15
# # print type(num)
# #
# # num = str(num)
# # print num
# # print type(num)
#
# # class Hello():
# #
# #     def __init__(self, id):
# #         self.id = id
# #
# #     def test(self):
# #         print "Hello, Class Hello"
# #
# # objs = [Hello(i) for i in range(5)]
# #
# #
# #     print i.id
#
# #
# # import ast
# # list = '["192.168.1.5","192.168.1.8"]'
# # x = ast.literal_eval(list)
# # x = [n.strip() for n in x]
# #
# # for i in x:
# #     print i
# import Devices
#
# dict = {}
# total = []
#
# mib = ['tcp', 'system']
# user = Devices.Devices('public', 2)
# ipList = ['192.168.91.41', '192.168.91.46']
#
# # result = []
# #
# # result.append(user.walkthrongh(oneIP, oneOID))
# # result.append(user.walkthrongh(twoIP, oneOID))
# #
# # print user.walkthrongh(oneIP, oneOID)
#
# # for i in result:
# #     for xx in i:
# #         print xx.oid, xx.value
#
# import threading
# import thread
# import time
#
#
# # class myThread(threading.Thread):
# #     def __init__(self, ip, mib):
# #         threading.Thread.__init__(self)
# #         self.ip = ip
# #         self.mib = mib
# #
# #     def run(self):
# #         user = Devices.Devices('public', 2)
# #         yyy = user.walkthrongh(self.ip, self.mib)
# #         for i in yyy:
# #             print i.oid, i.value
# #
# # for ip in ipList:
# #
# #     for oid in mib:
# #         print '-------------', ip, '-----------------'
# #         thread1 = myThread(ip, oid)
# #         thread1.start()
#
#
# # result = []
#
# # Define a function for the thread
# # def print_time( ip, mib):
# #    user = Devices.Devices('public', 2)
# #    yyy = user.walkthrongh(ip, mib)
# #    for i in yyy:
# #        print i.oid, i.value
# # # Create two threads as follows
# # # threadLock = threading.Lock()
# # for ip in ipList:
# #     try:
# #         thread.start_new_thread( print_time, (ip, 'system', ))
# #     except:
# #         print "Error: unable to start thread"
# #     while 1:
# #         pass
# # try:
# #    thread.start_new_thread( print_time, ("192.168.91.41", 'system', ) )
# #    thread.start_new_thread( print_time, ("192.168.91.46", 'system', ) )
# # except:
# #    print "Error: unable to start thread"
# #
# # while 1:
# #    pass

import Devices

oidList = ['system', 'udp']
result = []
result2 = []
user = Devices.Devices('public', 2)
for oid in oidList:
    result.append(user.walkthrongh('192.168.91.41', oid))
    result2.append(user.walkthrongh('192.168.91.46', oid))

print result.__len__()
print result2.__len__()

for i in range(len(result)):
    for xx in range(len(result[i])):
        print result[i][xx].value
