#!/usr/bin/python

import paramiko
import os
from stat import S_ISDIR


class Prepare:

    def __init__(self, remote_dir, local_dir):
        self.hostname = "172.16.30.164"
        self.username = "root"
        self.password = "root"
        self.remote_dir = remote_dir
        self.local_dir = local_dir

    def download_dir(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, username=self.username, password=self.password)
        sftp = ssh.open_sftp()
        os.path.exists(self.local_dir) or os.makedirs(self.local_dir)
        dir_items = sftp.listdir_attr(self.remote_dir)
        for item in dir_items:
            # assuming the local system is Windows and the remote system is Linux
            # os.path.join won't help here, so construct remote_path manually
            remote_path = self.remote_dir + '/' + item.filename
            local_path = os.path.join(self.local_dir, item.filename)
            if S_ISDIR(item.st_mode):
                self.download_dir()
            else:
                sftp.get(remote_path, local_path)

    def chmod_file(self):
        for root, dirs, files in os.walk(self.local_dir):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0705)
            for f in files:
                os.chmod(os.path.join(root, f), 0705)


if __name__ == '__main__':
    LOCAL_DIR = "/root/"
    REMOTE_DIR = "/root/"
    prepare_probe = Prepare(REMOTE_DIR, LOCAL_DIR)
    prepare_probe.chmod_file()
