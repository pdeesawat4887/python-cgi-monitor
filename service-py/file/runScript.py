import subprocess
# subprocess.call(['chmod', '+x', 'Script.py'])
# subprocess.call(['./Script.py'])

import paramiko
#
# ssh = paramiko.SSHClient()
# hostname = '172.16.30.150'
# username = 'root'
# password = 'root'
# ssh.connect(hostname=hostname, username=username, password=password, )

def ssh_command(ssh):
    command = input("Command:")
    ssh.invoke_shell()
    stdin, stdout, stderr = ssh.exec_command(command)
    print(stdout.read())

def ssh_connect(host, user, key):
    try:
        ssh = paramiko.SSHClient()
        print('Calling paramiko')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=user, password=key)
        print 'SUCCESS'
        cmd = 'ping -c 4 google.com'
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

        print 'ssh_stdin', dir(ssh_stdin)
        print 'ssh_stdout',ssh_stdout.read
        print 'ssh_stderr',ssh_stderr.readline
        # ssh_command(ssh)
    except Exception as e:
        print('Connection Failed')
        print(e)

if __name__=='__main__':
    # user = input("Username:")
    # key = input("Public key full path:")
    # host = input("Target Hostname:")
    user = 'root'
    key = 'root'
    host = '172.16.30.150'
    ssh_connect(host, user, key)
