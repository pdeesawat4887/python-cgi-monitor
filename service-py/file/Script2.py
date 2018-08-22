import paramiko
import Database
import getpass
import os
import threading


class Active(Database.MySQLDatabase):
    all_probe = {}

    def __init__(self):
        Database.MySQLDatabase.__init__(self)
        self.read_file_dictionary()
        self.all_probe = dict(self.query_all_probe())

    def read_file_dictionary(self):
        line = open('python-cgi-monitor/service-py/conf/dictionary', 'r').read()
        self.mapping_service = eval(line)

    def write_command(self, ssh, folder):

        outlock = threading.Lock()

        command = "mkdir {}".format(folder)
        # command = "rm -rf {}".format(folder)
        # command = "ls"

        stdin, stdout, stderr = ssh.exec_command(command)

        with outlock:
            pass


    def workon(self, probe_ip, probe_id, list_service):

        outlock = threading.Lock()

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=probe_ip, username='root', password='root')

        print 'Success SSH to {}'.format(probe_ip)
        print 'that have PROBE_ID in database as {}'.format(probe_id)


        # service_list = self.query_active_service(probe_id=probe_id)
        # print probe_id, list_service
        # list = ['run1', 'run2', 'run3', 'run4', 'run5', 'run6', 'run7', 'run8']

        threads2 = []
        for folder in list_service:
            t = threading.Thread(target=self.write_command, args=(ssh, folder,))
            t.start()
            threads2.append(t)
        for t in threads2:
            t.join()

        with outlock:
            pass

    def main(self):
        probe_ip = [self.all_probe[i] for i in self.all_probe]
        probe_id = [i for i in self.all_probe]

        threads = []
        for i in range(len(probe_id)):

            temp_data = []
            # service_list =[temp.append(i[0]) for i in self.query_active_service(probe_id=probe_id[i])]
            temp_service = self.query_active_service(probe_id=probe_id[i])
            print probe_ip[i]

            for service_id in temp_service:
                temp_data.append(service_id[0])


            t = threading.Thread(target=self.workon, args=(probe_ip[i], probe_id[i], temp_data,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()


import time
test = Active()
test.main()
# while True:
#     print time.ctime(time.time())
#     test.main()

