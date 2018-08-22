#!/usr/bin/python
import subprocess
# subprocess.call(['chmod', '+x', 'Script.py'])
# subprocess.call(['./Script.py'])

import paramiko
import Database
import getpass
import os

import threading


class ActiveService(Database.MySQLDatabase):
    probe_info = {}
    outlock = threading.Lock()

    def __init__(self):
        Database.MySQLDatabase.__init__(self)
        # self.read_file_dictionary()
        # print self.query_all_probe()
        # self.command_to_probe()
        self.uuu()
        self.main()

    def uuu(self):
        self.probe_info = dict(self.query_all_probe())
        print self.probe_info

    def workon(self, host, probe_id):



        # cmd0 = 'rm -rf SSH-Threading'
        # cmd = "mkdir SSH-Threading_sub_two"

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username='root', password='root')
        print 'success'

        lll = self.query_active_service(probe_id=probe_id)
        active = [i[0] for i in lll]

        threads2 = []
        for service in active:
            t = threading.Thread(target=self.ssh_command, args=(ssh, service))
            t.start()
            threads2.append(t)
        for t in threads2:
            t.join()
        # self.ssh_command(ssh, )
        # stdin, stdout, stderr = ssh.exec_command(cmd0)
        # stdin, stdout, stderr = ssh.exec_command(cmd)
        # stdin.write('xy\n')
        # stdin.flush()

        with self.outlock:
            pass
            # print stdout.readlines()

    def ssh_command(self, ssh, service_id):
        # transport = ssh.get_transport()
        # channel = transport.open_session()
        print service_id
        # ssh.invoke_shell()
        # chmod = 'chmod +x python-cgi-monitor/service-py/file/' + self.file[service_id]
        # command = 'python python-cgi-monitor/service-py/file/' + self.file[service_id]
        # command = 'ping -c 4 google.com'
        command = 'mkdir run{}'.format(service_id)
        print command
        # command = 'ping -c 4 google.com'
        # os.system('python '+ self.file[service_id])
        # print command

        # stdin, stdout, stderr = channel.exec_command(command)
        stdin, stdout, stderr = ssh.exec_command(command)
        # ssh.exec_command(chmod)
        # stdin, stdout, stderr = ssh.exec_command(command)
        # print(stderr.read())
        # print(stdout.read())
        # return stdout, stderr

        with self.outlock:
            pass

    def main(self):

        threads = []
        for i in self.probe_info:
            print '------->', i
            t = threading.Thread(target=self.workon, args=(self.probe_info[i], i,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    def read_file_dictionary(self):
        line = open('python-cgi-monitor/service-py/conf/dictionary', 'r').read()
        self.file = eval(line)
        print self.file


    def ssh_connect(self, host, user='root', password='root'):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, username=user, password=password)
            print('Successful connection')
            return ssh
        except Exception as e:
            print('Connection Failed')
            print(e)

    def command_to_probe(self):
        for probe_id in self.probe_info:
            ip = self.probe_info[probe_id]
            result = self.query_active_service(probe_id=probe_id)

            print 'Connect to ip: ' + ip

            ssh = self.ssh_connect(host=ip)

            for service in result:
                try:
                    self.ssh_command(ssh, service[0])
                except Exception as error:
                    print error


import os
# dict = {1: 'ICMPService.py'}
# print 'python', os.path.abspath(dict[1])
import time

print time.ctime(time.time())