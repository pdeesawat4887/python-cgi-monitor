#!/usr/bin/python

import main.__Database__ as mariadb
import paramiko
import threading
import os


class Server(mariadb.MySQLDatabase):

    def __init__(self):
        mariadb.MySQLDatabase.__init__(self)
        self.all_probe = self.select('probe', None, 'probe_id', 'ip_address', 'path')


    def sent_new_service_file(self, file):

        # for probe in self.all_probe:
        #     print probe
        # self.insert_new_service(service_name=service_name, file_name=file_name)

        threads = []
        for probe in self.all_probe:
            ip = probe[1]
            path = probe[2]
            t = threading.Thread(target=self.creation_ssh_connection, args=(ip, file, path + '/' + file))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    # def insert_new_service(self, service_name, file_name):
    #     data = [('NULL', service_name, file_name)]
    #     self.insert(table='service', list_data=data)

    def creation_ssh_connection(self, host, file, destination):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=host, username=self.setting['ssh_user'], password=self.setting['ssh_password'])
        except:
            ssh.connect(hostname=host, username='pi', password='raspberry')

        sftp = ssh.open_sftp()
        sftp.put('/var/www/upload/' + file, destination)

        command = "chmod +x " + destination
        ssh.exec_command(command)

    def check_if_directory_is_empty(self):

        dirName = '/var/www/upload'

        if os.path.exists(dirName) and os.path.isdir(dirName):
            if not os.listdir(dirName):
                print("Directory is empty")
            else:
                file_name = [f for f in os.listdir(dirName) if os.path.isfile(os.path.join(dirName, f))]
                self.sent_new_service_file(file_name[0])
                os.remove(dirName + '/' + file_name[0])
        else:
            print("Given Directory don't exists")


if __name__ == '__main__':
    example = Server()
    example.check_if_directory_is_empty()
    # example.check_probe_alive()
    # example.creation_ssh_connection2('192.168.254.31', '/Applications/XAMPP/xamppfiles/htdocs/python/python-cgi-monitor/service-py/src/SSHsentfile.py', '/root/SSHsentfile.py')
    # example.create_new_service(service_name='gaming',
    #                            full_path='/Applications/XAMPP/xamppfiles/htdocs/python/python-cgi-monitor/service-py/src/gaming.py')
