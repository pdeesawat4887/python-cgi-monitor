import Devices


class Interface:
    typeList = {}
    # oidList = []
    result_desc = []
    result_Type = []
    result_Mtu = []
    result_Speed = []
    result_Admin = []
    result_Opera = []

    IFDESCR = '1.3.6.1.2.1.2.2.1.2'
    IFTYPE = '1.3.6.1.2.1.2.2.1.3'
    IFMTU = '1.3.6.1.2.1.2.2.1.4'
    IFSPEED = '1.3.6.1.2.1.2.2.1.5'
    IFADMINSTATUS = '1.3.6.1.2.1.2.2.1.7'
    IFOPERSTATUS = '1.3.6.1.2.1.2.2.1.8'

    case = {1: 'UP', 2: 'DOWN', 3: 'Testing', 4: 'Unknow', 5: 'Dormant', 6: 'notPresent', 7: 'LowerLayerDown'}

    def loadDictionary(self, file):
        with open(file) as f:
            for line in f:
                key, value = line.strip().split()
                self.typeList[int(key)] = value

    # def loadOID(self, file):
    #     self.oidList = [line.rstrip('\n') for line in open(file)]

    def convertStatus(self, numStatus):
        return self.case[numStatus]

    def operation(self, ip, community, version):
        temp_walk = Devices.Devices(community, version)
        self.result_desc = temp_walk.walkthrongh(ip, self.IFDESCR)
        self.result_Type = temp_walk.walkthrongh(ip, self.IFTYPE)
        self.result_Mtu = temp_walk.walkthrongh(ip, self.IFMTU)
        self.result_Speed = temp_walk.walkthrongh(ip, self.IFSPEED)
        self.result_Admin = temp_walk.walkthrongh(ip, self.IFADMINSTATUS)
        self.result_Opera = temp_walk.walkthrongh(ip, self.IFOPERSTATUS)
        # self.removeDWDM()

    def operationUpdate(self, ip, community, version):
        temp_update = Devices.Devices(community, version)
        self.result_Mtu = temp_update.walkthrongh(ip, self.IFMTU)
        self.result_Speed = temp_update.walkthrongh(ip, self.IFSPEED)
        self.result_Admin = temp_update.walkthrongh(ip, self.IFADMINSTATUS)
        self.result_Opera = temp_update.walkthrongh(ip, self.IFOPERSTATUS)

    def removeDWDM(self):
        error = []
        for dump in self.result_desc:
            if 'dwdm' in dump.value:
                error.append(dump)
        for dwdm in error:
            self.result_desc.remove(dwdm)

    def __del__(self):
        self.result_desc = []
        self.result_Type = []
        self.result_Mtu = []
        self.result_Speed = []
        self.result_Admin = []
        self.result_Opera = []

# first_dict = {}
# tester = Interface()
# tester.loadDictionary('exchangex')
# tester.operation('192.168.1.8', 'public', 2)
# print tester.result_desc
#
# for i in tester.result_Type:
#     print tester.typeList[int(i.value)]
#
# for i in tester.result_Opera:
#     print tester.case[int(i.value)]
