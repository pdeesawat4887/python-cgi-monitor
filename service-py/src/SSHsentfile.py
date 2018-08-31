#!/usr/bin/python

import __Database__
import ICMPService
import paramiko
import threading
import os


class Server(__Database__.MySQLDatabase):

    def __init__(self):
        __Database__.MySQLDatabase.__init__(self)
        self.all_probe = self.select('probe', None, 'probe_id', 'ip_address', 'path')

    def check_ping(self, ip_address):
        ping = ICMPService.ICMPService()
        status, response = ping.get_status(destination=ip_address, port=None)
        return status

    def check_probe_alive(self):

        for probe in self.all_probe:
            id = probe[0]
            ip = probe[1]

            if self.check_ping(ip) == 1:
                update_sql = "UPDATE probe SET status='{}' WHERE probe_id='{}'".format(1, id)
                self.mycursor.execute(update_sql)
                self.connection.commit()

    def create_new_service(self, service_name, full_path):
        file_name = full_path.split('/')[-1]
        print file_name

        # for probe in self.all_probe:
        #     print probe
        self.insert_new_service(service_name=service_name, file_name=file_name)

        threads = []
        for probe in self.all_probe:
            ip = probe[1]
            path = probe[2]
            t = threading.Thread(target=self.creation_ssh_connection, args=(ip, full_path, path + '/' + file_name))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    def insert_new_service(self, service_name, file_name):
        data = [('NULL', service_name, file_name)]
        self.insert(table='service', list_data=data)

    def creation_ssh_connection(self, host, source, destination):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=self.setting['ssh_user'], password=self.setting['ssh_password'])
        sftp = ssh.open_sftp()
        sftp.put(source, destination)

    def creation_ssh_connection2(self, host, source, destination):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username='root', password='p@ssword')
        sftp = ssh.open_sftp()
        sftp.put(source, destination)

    def check_if_directory_is_empty(self):

        dirName = '/var/www/upload'

        if os.path.exists(dirName) and os.path.isdir(dirName):
            if not os.listdir(dirName):
                print("Directory is empty")
            else:
                onlyfiles = [f for f in os.listdir(dirName) if os.path.isfile(os.path.join(dirName, f))]
                print onlyfiles
        else:
            print("Given Directory don't exists")



if __name__ == '__main__':
    example = Server()
    example.check_if_directory_is_empty()
    # example.check_probe_alive()
    # example.creation_ssh_connection2('192.168.254.31', '/Applications/XAMPP/xamppfiles/htdocs/python/python-cgi-monitor/service-py/src/SSHsentfile.py', '/root/SSHsentfile.py')
    # example.create_new_service(service_name='gaming',
    #                            full_path='/Applications/XAMPP/xamppfiles/htdocs/python/python-cgi-monitor/service-py/src/gaming.py')
