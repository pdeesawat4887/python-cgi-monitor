

class Candy:

    def __init__(self, type, fname, lname):
        self.type = type
        self.fname =fname
        self.lname = lname
        self.operation()

    def operation(self):
        option = {
            'candy': self.hello_candy,
            'sweet': self.hello_sweet,
            'chocolate': self.hello_chocolate,
        }

        result, text = option[self.type](self.fname, self.lname)
        print '--------- RESULT -------'
        print result
        print '--------- text -------'
        print text

    def hello_candy(self, fname, lname):
        return fname+lname, "Hello candy {} {}".format(fname, lname)

    def hello_sweet(self, fname, lname):
        return lname + fname, "Hello sweet {} {}".format(lname, fname)

    def hello_chocolate(self, fname, lname):
        return lname + fname, None


# helen = Candy('chocolate', 'pacharapol', 'deesawat')


import socket
import time
def tcp(destination, destination_port):
    stdout = "status={status_final}"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print "socket creation failed with error %s" % (err)
        status_final = 3

    regex = {'http://': '', 'https://': ''}
    destination = reduce(lambda a, kv: a.replace(*kv), regex.iteritems(), destination)

    try:
        host_ip = socket.gethostbyname(destination)
    except socket.gaierror:
        status_final = 3

    s.settimeout(1)

    try:
        start_time = time.time()
        s.connect((host_ip, destination_port))
        end_time = time.time()
        status_final = 1
        stdout += ", rtt={rtt}".format(rtt=(end_time - start_time) * 1000)
    except socket.timeout:
        status_final = 2
    finally:
        s.close()
        return stdout.format(status_final=status_final)

hello = tcp('google.com', 443)
print hello