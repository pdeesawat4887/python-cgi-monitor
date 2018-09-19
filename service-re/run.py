import main.probe as probe
import os

if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    probeMac = probe.Probe(path)
    print probeMac.ip
    print probeMac.mac_address
    print probeMac.id
