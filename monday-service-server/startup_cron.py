#!/usr/bin/python

import paramiko
import os
from stat import S_ISDIR
import base64


class Prepare:

    def __init__(self, remote_dir, local_dir):
        self.hostname = "192.168.254.31"
        self.username = "root"
        self.password = base64.b64decode("cEBzc3dvcmQ=")
        LOCAL_DIR = '/root/release3/'
        REMOTE_DIR = '/root/release3_service/'
        self.download_dir(REMOTE_DIR, LOCAL_DIR)
        self.chmod_file(LOCAL_DIR)

    def download_dir(self, remote_dir, local_dir):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, password=password)
        sftp = ssh.open_sftp()
        os.path.exists(local_dir) or os.makedirs(local_dir)
        dir_items = sftp.listdir_attr(remote_dir)
        for item in dir_items:
            # assuming the local system is Windows and the remote system is Linux
            # os.path.join won't help here, so construct remote_path manually
            remote_path = remote_dir + '/' + item.filename
            local_path = os.path.join(local_dir, item.filename)
            if S_ISDIR(item.st_mode):
                self.download_dir(remote_path, local_path)
            else:
                sftp.get(remote_path, local_path)

    def chmod_file(self, local_path):
        for root, dirs, files in os.walk(local_path):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0705)
            for f in files:
                os.chmod(os.path.join(root, f), 0705)


if __name__ == '__main__':
    prepare_probe = Prepare()
