#!/usr/bin/python

import main.database as maria
import re
import time
import cgi

class Verify:

    def __init__(self):
        self.restricted = "~!@#$%^&*()+`={}|[];':\\"

    def verify_text(self, length, value, restrict):
        format_reg = {
            'limit': length,
            'restrict': restrict
        }
        if value == False:
            return "ERROR"
        elif value == None or value == '':
            return None
        else:
            value = str(value)
            return False if len(value) > int(length) else value if re.match("^{restrict}{{0,{limit}}}$".format(**format_reg), value) else False

        # elif len(value) < length:
        #     # print "^{restrict}{{0,{limit}}}$".format(**data)
        #     return value if re.match("^{restrict}{{0,{limit}}}$".format(**data), value) else False
        # else:
        #     return False

    def valid(self, word):
        for i in word:
            if i in self.restricted:
                return 'RES'
        return word

    def verify_escape(self, word):
        time_start = time.time()
        hello = "Valid" if re.match("^[a-zA-Z0-9_-]*$", word) else "Invalid"
        time_end = time.time()

        print hello
        print (time_end - time_start)*1000, 'ms'


candy = Verify()
# text = 'https://www.youtube.com/watch?v=1O2NlSRb-6o'
# pat = '[a-zA-Z0-9\_\-\.\:\?\=\/]'
#
# start = time.time()
# print candy.verify_text(24, text, pat)
# end = time.time()
# print (end-start)*1000, 'ms'


# prot = "service_destination.py"
# protocol = "[a-zA-Z0-9\.\-\_]"
# start = time.time()
# print candy.verify_text(64, prot, protocol)
# end = time.time()
# print (end-start)*1000, 'ms'

# text = 123456
# candy = Verify()
# pat = '[0-9]'
#
# start = time.time()
# print candy.verify_text(248, text, pat)
# end = time.time()
# print (end-start)*1000, 'ms'


# data = {
#             'limit': 32,
#             'restrict': '[hello]'
#         }
# hello = "^{restrict}{{0, {limit}}}$".format(**data)
# print  hello

# form = cgi.FieldStorage()
#
# print candy.verify_text(248, form.getvalue('service_id', False), pat)

# db = maria.MySQLDatabase()
#
# sql = "UPDATE `DESTINATIONS` SET {value} WHERE {condition}"
#
# sql.format(value=None,
#            condition=None)



data = [1, 2, 5, 10, -1]

dict_attribute = {
        'idest': 'destination_id',
        'isvc': 'service_id',
        'ndest': 'destination_name',
        'ptdest': 'destination_port',
        'dest_desc': 'destination_description',
}

data_attribute = {
        'idest': '11',
        'isvc': '1',
        'ndest': 'www.google.com',
        'ptdest': '443',
}

# output = filter(lambda x: data_attribute[x] if data_attribute[x] != None else None, dict_attribute)
output = map(lambda data: "`{ori}`='{data}'".format(ori=dict_attribute[data], data=data_attribute[data]), data_attribute)

# map(lambda key, value: "`{key}`='{value}'".format(key=self.dictionary[key], value=value), attribute, attribute_key)

print tuple(output)
#
# if "test" in wordFreqDic:
#     print("Yes 'test' key exists in dict")
# else:
#     print("No 'test' key does not exists in dict")