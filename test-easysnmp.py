from easysnmp import Session

dict_oid = {}

class Router:

    def __init__(self, host, community, version):
        self.host = host
        self.community = community
        self.version = version
        self.session = Session(hostname=self.host,
                               community=self.community, version=self.version)

    def walkthrough(self, oid):
        items = self.session.walk(oid)
        return items



def create_dict(dict, file):
    with open(file) as f:
        for line in f:
            key, value = line.strip().split()
            dict[key] = value

create_dict(dict_oid, "oid_list.txt")

router = Router('192.168.1.8', 'public', 2)

list = ['system']
info = []

for it in list:
    print "it ---->", dict_oid[it]
    info.append(router.walkthrough(dict_oid[it]))
    # print "oid_map ---->", router.walkthrough(dict_oid[it])
print info
# print router.walkthrough('system')