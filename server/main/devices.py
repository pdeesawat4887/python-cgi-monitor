from easysnmp import Session


class Device:

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
