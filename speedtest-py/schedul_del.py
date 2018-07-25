import sched, time


def do_something():
    print time.ctime(time.time())
    # s.enter(300, 1, do_something, ())


# s.enter(10, 1, do_something, (s,))

# if __name__ == '__main__':
#     s = sched.scheduler(time.time, time.sleep)
#     do_something()
#     s.run()

try:
    while True:
        do_something()
        time.sleep(60)
except KeyboardInterrupt:
    print('Manual break by user')

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
