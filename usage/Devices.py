from easysnmp import Session


class Devices:
    ipList = []
    temp = []
    oidList = []
    result = []

    def __init__(self, community, version):
        # self.host = host
        self.community = community
        self.version = version
        # self.session = Session(hostname=self.host,
        #                        community=self.community, version=self.version)

    def walkthrongh(self, ip, oid):
        session = Session(hostname=ip,
                          community=self.community, version=self.version)
        return session.walk(oid)

    def addIp(self, ip):
        self.ipList.append(ip)

    # def create_dict(self, file):
    #     # with open(file) as f:
    #     self.oidList = [line.rstrip('\n') for line in open(file)]
    #     # for line in f:
    #     #     self.oidList.append(line.split())

    def setOID(self, oid):
        self.oid = oid

    def start(self):
        for ip in self.ipList:
            myResult = self.walkthrongh(ip, self.oid)
            self.result.append(myResult)

    def testClass(self):
        print "Success,"

    def testClass(self):
        print "Success,"

    def testTwoClass(self):
        print "Switchcase"

    def main(self,ipList, community, version, mib):
        self.community = community
        self.version = version
        for ip in ipList:
            self.addIp(ip)
        self.setOID(mib)
        self.start()


# ipList = ['192.168.1.5', '192.168.1.8']
# walker = Devices()
# walker.main(ipList, 'public', 2, 'system')
# print walker.result
# walker = Devices('public', 2)
# # walker.create_dict('mapping')
# # for i in walker.oidList:
# #     print i
# # print walker.oidList
# walker.addIp('192.168.91.41')
# walker.addIp('192.168.91.46')
# walker.setOID('system')
# walker.main()
# # walker.addIp('192.168.91.46')

# # -------------------------------------------------------------------------
#
# ipList = ['192.168.91.41', '192.168.91.46']
# user = Devices('public', 2)
# for ip in ipList:
#     user.addIp(ip)
# user.setOID('system')
# user.start()
#
# for item in user.result:
#     for x in range(len(item)):
#         print '<tr>' \
#               '<td>' + item[x].oid + '</td>' \
#                                     '<td>' + item[x].value + '</td>'
#
# # -------------------------------------------------------------------------