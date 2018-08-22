#!/usr/bin/python

import paramiko
import Database
import threading



class Active(Database.MySQLDatabase):
    all_probe = {}

    def __init__(self):
        Database.MySQLDatabase.__init__(self)
        self.read_file_dictionary()
        self.all_probe = dict(self.query_all_probe())
        self.main()

    def read_file_dictionary(self):
        line = open(self.path + '/conf/dictionary', 'r').read()
        # line = open('../conf/dictionary', 'r').read()
        self.mapping_service = eval(line)

    def write_command(self, ssh, file):

        outlock = threading.Lock()

        # command = "mkdir {}".format(file)
        # command = "rm -rf {}".format(file)
        # command = "ls"
        command = "python " + self.path + '/' + self.mapping_service[file]

        print command

        # stdin, stdout, stderr = ssh.exec_command(command)
        #
        # if self.setting['output'] == 0:
        #     print stdout.read()
        # print stderr.read()

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
        for file in list_service:
            t = threading.Thread(target=self.write_command, args=(ssh, file,))
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
            print temp_data

            t = threading.Thread(target=self.workon, args=(probe_ip[i], probe_id[i], temp_data,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()


# import time
#
# test = Active()
# test.main()
# while True:
#     # print time.ctime(time.time())
#     test.main()
#     time.sleep(300)

if __name__ == '__main__':
    sss = Active()
