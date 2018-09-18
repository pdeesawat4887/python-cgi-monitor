import main.probe as probe

if __name__ == '__main__':
    probeMac = probe.Probe()
    print probeMac.ip
    print probeMac.mac_address
    print probeMac.id