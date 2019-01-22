import subprocess
import time

def match_ping_1():
    numPings = 10
    # pingTimeout = 3
    # maxWaitTime = 3
    output = subprocess.check_output('ping -c %s 8.8.8.8' % (numPings), shell=True)
    # print output

    output = output.split('\n')[-3:]
    # print output
    # -1 is a blank line, -3 & -2 contain the actual results

    xmit_stats = output[0].split(",")
    # print xmit_stats
    timing_stats = output[1].split("=")[1].split("/")
    # print timing_stats

    packet_loss = float(xmit_stats[2].split("%")[0])

    ping_min = float(timing_stats[0])
    ping_avg = float(timing_stats[1])
    ping_max = float(timing_stats[2])

    print (ping_min, ping_avg, ping_max)

def match_ping_2(host):
    NUM = '10'
    WAIT = '0.5'
    SIZE = '64'
    TIMEOUT = '3'

    ping = subprocess.Popen(
        ["ping", "-c", NUM, "-i", WAIT, "-s", SIZE, "-t", TIMEOUT, host],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    out, error = ping.communicate()
    # print out

    import re
    matcher = re.compile("round-trip min/avg/max/stddev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)")
    print matcher.search(out).groups()[1]



# start_1 = time.time()
# match_ping_1()
# print "Finished Test Method 1: ", (time.time()-start_1)

# MAIN_URL = 'pantip.com'

# start_2 = time.time()
# match_ping_2(MAIN_URL)
# print "Finished Test Method 2: ", (time.time()-start_2)

dictionary = {
    "Google": 'google.com',
    "Gmail": 'gmail.com',
    "Pantip": 'pantip.com',
    "Blognone": 'blognone.com',
}

for i, j in dictionary.iteritems():
    print i
    match_ping_2(j)
    print "--------------------------------------------------"