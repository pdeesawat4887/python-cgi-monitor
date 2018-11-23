#!/usr/bin/python

import os
import main.probe as pb

if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    # print path
    helloProbe = pb.Probe(path)