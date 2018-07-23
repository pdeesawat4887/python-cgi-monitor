import speedtest

servers = [3147]
# If you want to test against a specific server
# servers = [1234]
s = speedtest.Speedtest()
s.get_servers(servers)
# dict = s.get_servers(servers).values()[0][0]
# print s.get_servers(servers).values()[0][0]
# print type(dict)
# print dict['sponsor']
s.get_best_server()
s.download()
s.upload()
s.results.share()
#
results_dict = s.results.dict()

print results_dict
#
# for i in results_dict:
#     print i, results_dict[i]