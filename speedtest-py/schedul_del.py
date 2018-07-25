import sched, time


def do_something():
    print time.ctime(time.time())
    # s.enter(300, 1, do_something, ())


# s.enter(10, 1, do_something, (s,))

# if __name__ == '__main__':
#     s = sched.scheduler(time.time, time.sleep)
#     do_something()
#     s.run()

# try:
#     while True:
#         do_something()
#         time.sleep(60)
# except KeyboardInterrupt:
#     print('Manual break by user')

# def loadFile(file):
#         typeList = []
#         with open(file) as f:
#             for line in f:
#                 key = line.strip().split(',')
#                 typeList.append(key)
#             return typeList

# print loadFile('portstatus.csv')
# serverList = []
# setting = {}
#
# def loadFile(file):
#     with open(file) as f:
#         for line in f:
#             key, value = line.strip().split('=')
#             if 'server' in key:
#                 serverList.append(value)
#             else:
#                 setting[key] = value
#
# loadFile('setting.txt')
# print len(serverList)
# print len(setting)
#
# print setting
# print serverList


def read(file='hosts.txt'):
    with open(file, 'r') as temp_file:
        text = temp_file.read()
        host_list = text.split()
        temp_file.close()
    return host_list

# print read()

# import socket
# import os
#
# url = 'facebook.com'
#
# ip_address = socket.gethostbyname(url)
# ping_value = os.system("ping -c 1 -i 0.1 " + ip_address)
# if ping_value == 0:
#     ping_status = 'Active'
# else:
#     ping_status = 'Check server first'
#
# print ping_status

# dict = {"a":"apple", "b":"banana"}
#
# dict['facebook.com'] = [200, 'OK', 'Active']
#
# word = 'facebook.com'
#
# word = word.split('.')
#
# print word[0]

import requests
protocol = ''
url = 'linkedin.com'
print protocol+url

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36 OPR/53.0.2907.99'}
res_https = requests.get(protocol + url, headers=headers)
status = res_https.status_code
reason = res_https.reason
res_https.close()

print status
print reason
