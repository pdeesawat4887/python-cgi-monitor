#!/usr/bin/python

from easysnmp import Session


class SnmpWalker:

    def __init__(self, host, community, version):
        self.host = host
        self.community = community
        self.version = version
        self.create_session()

    def create_session(self):
        self.session = Session(hostname=self.host, community=self.community, version=self.version)

    def walk_through(self, oid):
        return self.session.walk(oid)


# if __name__ == '__main__':
#     HOST = '192.168.91.41'
#     COMMUNITY = 'public'
#     VERSION = 2
#     walker = SnmpWalker(HOST, COMMUNITY, VERSION)
#     list_oid = [u'ifSpeed', u'ifType', u'ifInOctets', u'ifInDiscards', u'ifNumber', u'ifLastChange', u'ifPhysAddress', u'ifInUcastPkts', u'ifInErrors', u'ifOutOctets', u'ifAdminStatus', u'ifInUnknownProtos', u'ifDescr', u'ifIndex', u'ifOutUcastPkts', u'ifOutDiscards', u'ifOutErrors', u'ifMtu', u'ifOperStatus']
#     result = walker.walk_through('enterprises.9.9.48.1.1.1')
#
#     for i in result:
#         print i.__dict__

from easysnmptable import Session

with Session(hostname='192.168.91.41', community='public', version=2) as session:
    table = session.gettable('ifTable')

for index, row in table.rows.items():
    print("index: {}".format(index))
    for key, value in row.items():
        print("{}: {}".format(key, value))