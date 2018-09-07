from easysnmp import Session


class Devices:

    def __init__(self):
        self.community = 'public'
        self.version = 2

    def community_string(self, community):
        self.community = community

    def version(self, version):
        self.version = int(version)

    def walkthrongh(self, ip, oid):
        session = Session(hostname=ip,
                          community=self.community, version=self.version)
        return session.walk(oid)

if __name__ == '__main__':
    ip = ['192.168.91.41']
    ifIndex = 0
    ifDescr = 0
    ifType = 0
    ifMtu = 0
    ifSpeed = 0
    ifPhysAddress = 0
    ifAdminStatus = 0
    ifOperStatus = 0
    ifLastChange = 0
    ifInOctets = 0
    ifInUcastPkts = 0
    test = Devices()
    for x in ip:
        result = test.walkthrongh(ip=x, oid='interfaces')
        print result[0].value
        for i in range(1, int(result[0].value)+1):
            print result[i].oid, result[i].value




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