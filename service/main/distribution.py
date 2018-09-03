#!/usr/bin/python

import database as maria_db
import paramiko
import threading
import os
import platform
import subprocess
import requests


class Server(maria_db.MySQLDatabase):

    def __init__(self):
        maria_db.MySQLDatabase.__init__(self)
        self.all_probe = self.select('probe', None, 'probe_id', 'ip_address', 'path')

    def check_ping(self, ip_address):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', ip_address]
        return subprocess.call(command) == 0

    def update_probe_alive(self, probe_id, ip_address):
        if self.check_ping(ip_address) != 0:
            update_sql = "UPDATE probe SET status='{}' WHERE probe_id='{}'".format(1, probe_id)
            self.mycursor.execute(update_sql)
            self.connection.commit()

    def check_probe(self):
        threads = []
        for probe in self.all_probe:
            probe_id = probe[0]
            ip_address = probe[1]
            t = threading.Thread(target=self.update_probe_alive, args=(probe_id, ip_address,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    def get_warning_from_baseline(self):

        query_sql_perf = "SELECT probe_name, ip_address, service_name, destination, destination_port, location, ping, download, upload, time" \
                         " FROM performance_service" \
                         " inner join destination on destination.destination_id=performance_service.destination_id" \
                         " inner join probe on performance_service.probe_id=probe.probe_id" \
                         " inner join service on destination.service_id=service.service_id" \
                         " where ((ping != 0 and (upload < {} or download < {})) or (ping = 0 and download < {}) )and (time > NOW() - INTERVAL {} MINUTE);".format(
            self.setting['upload_baseline'], self.setting['download_baseline'], self.setting['download_only'],
            self.setting['interval'])

        query_sql_avai = "SELECT probe_name, ip_address, service_name, destination, destination_port, response_time, time " \
                         "FROM availability_service " \
                         "inner join destination on destination.destination_id=availability_service.destination_id " \
                         "inner join probe on availability_service.probe_id=probe.probe_id " \
                         "inner join service on destination.service_id=service.service_id " \
                         "where (availability_service.status != 0 or response_time > {} ) and (time > NOW() - INTERVAL {} MINUTE);".format(
            self.setting['response_time'], self.setting['interval'])

        self.mycursor.execute(query_sql_perf)
        perf_result = self.mycursor.fetchall()

        self.mycursor.execute(query_sql_avai)
        avai_result = self.mycursor.fetchall()

        return avai_result, perf_result

    def notify_me(self, data, type):
        url = 'https://notify-api.line.me/api/notify'
        token = 'pyL4xY6ys303vg0bVnvd0DRco7UyILVo5dOXZGjBWD8'
        headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}

        for warning in data:
            print warning
            if type is 'performance':
                msg = '\nWARNING !!!\nProbe Name: {}\nIP Address: {}\nService: {}\nDestination: {}\nPort: {}\nLocation: {}\nPing: {}\nDownload: {}\nUpload: {}\nTime: {}\nPlease check your service'.format(
                    warning[0], warning[1], warning[2], warning[3], warning[4], warning[5], warning[6], warning[7],
                    warning[8], warning[9])
            else:
                msg = '\nWARNING !!!\nProbe Name: {}\nIP Address: {}\nService: {}\nDestination: {}\nPort: {}\nResponse Time: {}\nTime: {}\nPlease check your service'.format(
                    warning[0], warning[1], warning[2], warning[3], warning[4], warning[5], warning[6])

            request = requests.post(url, headers=headers, data={'message': msg})

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

    def sent_new_service_file(self, file):
        threads = []
        for probe in self.all_probe:
            ip = probe[1]
            path = probe[2]
            t = threading.Thread(target=self.creation_ssh_connection, args=(ip, file, path + '/' + file))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

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


if __name__ == '__main__':
    server = Server()
    server.check_probe()
    availability, performance = server.get_warning_from_baseline()
    server.notify_me(data=availability, type='availability')
    server.notify_me(data=performance, type='performance')
