import subprocess
# subprocess.call(['chmod', '+x', 'Script.py'])
# subprocess.call(['./Script.py'])

import paramiko
import Database
import getpass

#
# ssh = paramiko.SSHClient()
# hostname = '172.16.30.150'
# username = 'root'
# password = 'root'
# ssh.connect(hostname=hostname, username=username, password=password, )

class ActiveService(Database.MySQLDatabase):
    probe_info = {}
    file = {
        1: 'ICMPService.py',
        2: 'DNSService.py',
        4: 'WebService.py',
        5: 'SpeedtestService.py',
        6: 'VideoService.py',
        7: 'SMTPService.py',
        8: 'IMAPService.py',
        9: 'POP3Service.py'
    }

    def __init__(self):
        Database.MySQLDatabase.__init__(self)
        self.query_all_probe()
        self.command_to_probe()

    def query_all_probe(self):
        try:
            query_sql = "SELECT probe_id, ip_address FROM probe"
            self.mycursor.execute(query_sql)
            my_result = self.mycursor.fetchall()

            for line in my_result:
                self.probe_info[line[0]] = line[1]

        except Exception as error:
            self.probe_info = {}
            print 'Error', error

    def query_active_service(self, probe_id):
        query_sql = "SELECT service_id FROM setting WHERE probe_id='{}' and setting='0'".format(probe_id)
        self.mycursor.execute(query_sql)
        my_result = self.mycursor.fetchall()
        return my_result

    def ssh_command(self, ssh, file):
        ssh.invoke_shell()
        # command = 'chmod +x python-cgi-monitor/service-py/file/' + file
        command = './python-cgi-monitor/service-py/file/' + file
        print command

        stdin, stdout, stderr = ssh.exec_command(command)

        print(stdout.read())

    def ssh_connect(self, host, user='root', password='root'):
        try:
            ssh = paramiko.SSHClient()
            print user
            print password
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
            user = raw_input('User: ')
            pswd = getpass.getpass('Password: ')

            print result
            ssh = self.ssh_connect(host=ip, user=user, password=pswd)
            for service in result:
                print service[0]

    # if __name__ == '__main__':
    #     # user = input("Username:")
    #     # key = input("Public key full path:")
    #     # host = input("Target Hostname:")
    #
    #     user = 'root'
    #     key = 'root'
    #     host = '172.16.30.150'
    #     ssh_connect(host, user, key)


xxx = ActiveService()

# for i in xxx.probe:
#     print '---->', i
#     for j in xxx.query_active_service(i):
#         print xxx.file[str(j[0])]
