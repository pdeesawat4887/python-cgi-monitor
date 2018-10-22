#!/usr/bin/python

# import nmap
#
# nm = nmap.PortScanner()

import os
import sys
import subprocess

# process = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE)
# out = process.communicate()
# print out

stdout = "upload=3.142, download=2.56, rtt=6\n"

dict_result = {'status': None,
               'upload': None,
               'download': None,
               'rtt': None}

results = stdout.replace(' ', '').replace('\n', '').split(',')

map(lambda item: dict_result.update({item.split('=')[0]: float(item.split('=')[1]) if 'none' not in item.lower() else None}), results)

print dict_result

# print key
# print value
# print dict_result

# for k, v in dict_result.items():
#     print type(k), type(v)

# for result in results:
#     key, value = result.split('=')
# 	dict_result[key]=float(value)
# print dict_result