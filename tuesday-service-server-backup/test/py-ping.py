import subprocess
import shlex

cmd   = 'ping www.google.com -c 1'

ping = subprocess.Popen(shlex.split(cmd), stderr=subprocess.PIPE,
                        stdout=subprocess.PIPE)
out, err = ping.communicate()

print out
print err