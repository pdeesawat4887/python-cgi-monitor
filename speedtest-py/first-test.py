import speedtest

servers = []
# If you want to test against a specific server
# servers = [1234]

s = speedtest.Speedtest()
s.get_servers(servers)
s.get_best_server()
s.download()
s.upload()
s.results.share()

results_dict = s.results.dict()

for i in results_dict:
    print i, results_dict[i]