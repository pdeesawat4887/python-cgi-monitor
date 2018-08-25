# import os
# import paramiko
# import scp
#
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
# ssh.connect(hostname='192.168.254.33', username='root', password='p@ssword')
# # sftp = ssh.open_sftp()
# # # sftp.put('conf/server', '/root/FTPTest.txt')
# # # sftp.close()
# # # ssh.close()
#
# with scp.SCPClient(ssh.get_transport()) as scp:
#     scp.put('conf/server', '/root/FTP')
#     # scp.get('test2.txt')

import __Database__

class Upload(Database.MySQLDatabase):

    def __init__(self):
        Database.MySQLDatabase.__init__(self)
        self.all_probe = self.select('probe', None, 'probe_id', 'ip_address', 'path')

fff= Upload()
for i in fff.all_probe:
    print i