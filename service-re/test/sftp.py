# import paramiko, os
#
# paramiko.util.log_to_file('/tmp/paramiko.log')
# from stat import S_ISDIR
#
# host = "192.168.254.33"
# port = 22
# transport = paramiko.Transport((host, port))
# password = "root"
# username = "p@ssword"
#
# transport.connect(username=username, password=password)
# transport.auth_none('p@ssword')
# sftp = paramiko.SFTPClient.from_transport(transport)
#
#
#
# def sftp_walk(remotepath):
#     path = remotepath
#     files = []
#     folders = []
#     for f in sftp.listdir_attr(remotepath):
#         if S_ISDIR(f.st_mode):
#             folders.append(f.filename)
#         else:
#             files.append(f.filename)
#     if files:
#         yield path, files
#     for folder in folders:
#         new_path = os.path.join(remotepath, folder)
#         for x in sftp_walk(new_path):
#             yield x
#
#
# for path, files in sftp_walk("." or '/root/helloSFTP'):
#     for file in files:
#         # sftp.get(remote, local) line for dowloading.
#         sftp.get(os.path.join(os.path.join(path, file)), '/local/path/')


import paramiko
import os

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname='192.168.254.33',username='root', password='p@ssword')

apath = '/root/helloSFTP/'
rawcommand = 'ls {}'.format(apath)
command = rawcommand
stdin, stdout, stderr = ssh.exec_command(command)
filelist = stdout.read().splitlines()

ftp = ssh.open_sftp()
for afile in filelist:
    print afile
    (head, filename) = os.path.split(afile)
    print(filename)
    ftp.get(afile, apath+filename)
ftp.close()
ssh.close()



import os
from stat import S_ISDIR

def download_dir(remote_dir, local_dir):
    import os
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='172.16.30.164', username='root', password='root')
    sftp = ssh.open_sftp()
    os.path.exists(local_dir) or os.makedirs(local_dir)
    dir_items = sftp.listdir_attr(remote_dir)
    for item in dir_items:
        # assuming the local system is Windows and the remote system is Linux
        # os.path.join won't help here, so construct remote_path manually
        remote_path = remote_dir + '/' + item.filename
        local_path = os.path.join(local_dir, item.filename)
        if S_ISDIR(item.st_mode):
            download_dir(remote_path, local_path)
        else:
            sftp.get(remote_path, local_path)


download_dir("/testDirectory","/root/monitor")
