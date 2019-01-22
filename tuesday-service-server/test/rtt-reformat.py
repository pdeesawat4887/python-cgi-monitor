import requests
import time
import socket


def RTT(url):
    # time when the signal is sent
    t1 = time.time()
    r = requests.get(url)
    # time when acknowledgement of signal
    # is received
    t2 = time.time()
    # total time taken
    tim = str(t2 - t1)
    print("Time in seconds :" + tim)
    # driver program
# url address
# url = "https://www.google.com"
# url_wos = "http://www.google.com"
# RTT("https://www.google.com")
# RTT("http://www.google.com")
# RTT("https://pantip.com")
# RTT("https://www.blognone.com")
# RTT("http://example.com")
# RTT('192.168.254.34')

# RTT('http://203.151.13.166')


def request_time(test_url):

    if 'http://' not in test_url:
        test_url = 'http://' + test_url

    print test_url

    list_data = []
    for i in range(1,10):
        r = requests.get(test_url)
        roundtrip = r.elapsed.total_seconds()
        list_data.append(roundtrip)
    # return list_data
    return reduce(lambda x, y: x + y, list_data) / len(list_data)

def request_time_manual(test_url):
    # time when the signal is sent
    list_data_manual = []
    for i in range(1,10):
        t1 = time.time()
        r = requests.get(test_url)
        t2 = time.time()
        tim = t2 - t1
        list_data_manual.append(tim)
    return reduce(lambda x, y: x + y, list_data_manual) / len(list_data_manual)

def request_time_reduce(test_url):
    timeout = 1
    post_fields = 'hello'
    reduce_list = []
    for i in range(1,10):
        response = requests.post(test_url, data=post_fields, timeout=timeout)
        reduce_list.append(response.elapsed.total_seconds())
    return reduce(lambda x, y: x + y, reduce_list) / len(reduce_list)

def tcp(destination, destination_port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print "socket creation failed with error %s" % (err)
        status_final = 3

    regex = {'http://': '', 'https://': ''}
    destination = reduce(lambda a, kv: a.replace(*kv), regex.iteritems(), destination)

    try:
        host_ip = socket.gethostbyname(destination)
    except socket.gaierror:
        status_final = 3

    s.settimeout(1)

    try:
        start_time = time.time()
        s.connect((host_ip, destination_port))
        end_time = time.time()
        status_final = 1
        stdout = end_time - start_time
    except socket.timeout:
        status_final = 2
    finally:
        s.close()
        return stdout

def tcp_legacy(test_url):
    tcp_list = []
    for i in range(1,10):
        tcp_list.append(tcp(test_url, 443))
    return reduce(lambda x, y: x + y, tcp_list) / len(tcp_list)


def forecast(MAIN):
    main_1=[]
    main_2=[]
    main_3=[]
    main_4=[]

    # for i in range(1, 10):
    main_1.append(request_time(MAIN))
    main_2.append(request_time_manual(MAIN))
    main_3.append(request_time_reduce(MAIN))
        # main_4.append(tcp_legacy(MAIN))

    print main_1
    print main_2
    print main_3
    # print main_4

# forecast('https://www.google.com')
# print '-----------------------------------------------------------'
# forecast('http://www.google.com')
# print '-----------------------------------------------------------'
# forecast('https://pantip.com')
# print '-----------------------------------------------------------'
#
print request_time('203.151.13.166')
# print request_time_manual('https://pantip.com')
# print request_time_reduce('https://pantip.com')
# print request_time('https://pantip.com')
# print request_time_manual('172.217.166.142')
# print request_time('https://www.blognone.com')