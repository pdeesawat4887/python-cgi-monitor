# import sys, os, string, threading
# import paramiko
#
# cmd = "rm -rf SSH-Threading_sub"
#
# outlock = threading.Lock()
#
# def workon(host):
#
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(host, username='root', password='root')
#     print 'success'
#     stdin, stdout, stderr = ssh.exec_command(cmd)
#     # stdin.write('xy\n')
#     # stdin.flush()
#
#     with outlock:
#         print stdout.readlines()
#
# def main():
#     hosts = ['172.16.30.156', '172.16.30.153', '172.16.30.154', ] # etc
#     threads = []
#     for h in hosts:
#         t = threading.Thread(target=workon, args=(h,))
#         t.start()
#         threads.append(t)
#     for t in threads:
#         t.join()
#
# main()

import sys, os, string, threading
import paramiko

outlock = threading.Lock()

def write_command(ssh, word):
    cmd = "mkdir {}".format(word)

    print cmd

    stdin, stdout, stderr = ssh.exec_command(cmd)

    with outlock:
        pass

def workon(host):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username='root', password='root')
    print 'success'

    list = ['run1', 'run2', 'run3']
    threads2 = []
    for word in list:
        t = threading.Thread(target=write_command, args=(ssh, word,))
        t.start()
        threads2.append(t)
    for t in threads2:
        t.join()
    # stdin, stdout, stderr = ssh.exec_command(cmd)
    # stdin.write('xy\n')
    # stdin.flush()

    with outlock:
        pass

def main():
    hosts = ['172.16.30.156', '172.16.30.153', '172.16.30.154', ] # etc
    threads = []
    for h in hosts:
        t = threading.Thread(target=workon, args=(h,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

main()