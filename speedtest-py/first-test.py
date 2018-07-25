import speedtest
import Utillity
import time

tool = Utillity.Utilities()
for i in range(10):
    print tool.gettime_ntp()
    time.sleep(60)

# servers = [19036]
# # If you want to test against a specific server
# # servers = [1234]
# s = speedtest.Speedtest()
# s.get_servers(servers)
# dict = s.get_servers(servers).values()[0][0]['name']
# print dict
# # print type(dict)
# # print dict['sponsor']
# s.get_best_server()
# s.download()
# s.upload()
# s.results.share()
# #
# results_dict = s.results.dict()
# print 'result_dict ---> ', results_dict
# print "Download: {}".format(tool.bytes_2_human_readable(results_dict['download']))
# print "Upload: {}".format(tool.bytes_2_human_readable(results_dict['upload']))
#
# # print results_dict
# #
# # for i in results_dict:
# #     print i
#
# client = results_dict['client']
# print 'client_dict ---> ', client
#
# print 'IP: {}\n' \
#       'ISP: {}\n' \
#       'COUNTRY: {}'.format(client['ip'], client['isp'], client['country'])

# 100.4562
# 13.7083
