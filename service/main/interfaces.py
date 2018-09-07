import devices


class Interface:
    typeList = {}
    # oidList = []
    result_desc = []
    result_Type = []
    result_Speed = []
    result_Admin = []
    result_Opera = []

    result_list = [result_desc, result_Type,
                   result_Speed, result_Admin, result_Opera]

    IFDESCR = '1.3.6.1.2.1.2.2.1.2'
    IFTYPE = '1.3.6.1.2.1.2.2.1.3'
    IFSPEED = '1.3.6.1.2.1.2.2.1.5'
    IFADMINSTATUS = '1.3.6.1.2.1.2.2.1.7'
    IFOPERSTATUS = '1.3.6.1.2.1.2.2.1.8'

    case = {1: 'UP', 2: 'DOWN', 3: 'Testing', 4: 'Unknow',
            5: 'Dormant', 6: 'notPresent', 7: 'LowerLayerDown'}

    def loadDictionary(self, file):
        with open(file) as f:
            for line in f:
                key, value = line.strip().split()
                self.typeList[int(key)] = value

    def convertStatus(self, numStatus):
        return self.case[numStatus]

    def operation(self, ip, community, version):
        temp_walk = devices.Device()
        self.result_desc = temp_walk.walkthrongh(ip, self.IFDESCR)
        self.result_Type = temp_walk.walkthrongh(ip, self.IFTYPE)
        self.result_Speed = temp_walk.walkthrongh(ip, self.IFSPEED)
        self.result_Admin = temp_walk.walkthrongh(ip, self.IFADMINSTATUS)
        self.result_Opera = temp_walk.walkthrongh(ip, self.IFOPERSTATUS)

    def operationUpdate(self, ip, community, version):
        temp_update = devices.Devices()
        self.result_Speed = temp_update.walkthrongh(ip, self.IFSPEED)
        self.result_Admin = temp_update.walkthrongh(ip, self.IFADMINSTATUS)
        self.result_Opera = temp_update.walkthrongh(ip, self.IFOPERSTATUS)

    def __del__(self):
        self.result_desc = []
        self.result_Type = []
        self.result_Speed = []
        self.result_Admin = []
        self.result_Opera = []
