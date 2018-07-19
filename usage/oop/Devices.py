from easysnmp import Session


class Devices:

    ipList = []

    def __init__(self, host, community, version):
        self.host = host
        self.community = community
        self.version = version
        self.session = Session(hostname=self.host,
                               community=self.community, version=self.version)

    def walkthrough(self, oid):
        return self.session.walk(oid)

    def addIp(self, ip):
        self.ipList.append(ip)

walker = Devices('192.168.91.46', 'public', 2)

for i in walker.walkthrough('icmp'):
    print i.value