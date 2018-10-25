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


# candy = Verify()
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

# data = [1, 2, 5, 10, -1]
#
# dict_attribute = {
#         'idest': 'destination_id',
#         'isvc': 'service_id',
#         'ndest': 'destination_name',
#         'ptdest': 'destination_port',
#         'dest_desc': 'destination_description',
# }
#
# data_attribute = {
#         'idest': '11',
#         'isvc': '1',
#         'ndest': 'www.google.com',
#         'ptdest': '443',
# }
#
# # output = filter(lambda x: data_attribute[x] if data_attribute[x] != None else None, dict_attribute)
# output = map(lambda data: "`{ori}`='{data}'".format(ori=dict_attribute[data], data=data_attribute[data]), data_attribute)
#
# # map(lambda key, value: "`{key}`='{value}'".format(key=self.dictionary[key], value=value), attribute, attribute_key)
#
# print tuple(output)
#
# if "test" in wordFreqDic:
#     print("Yes 'test' key exists in dict")
# else:
#     print("No 'test' key does not exists in dict")
#
db = maria.MySQLDatabase()

def logging(user=None, type=None, table=None, sql=None, **kwargs):
    id = db.mycursor.lastrowid
    mapping = {
        'PROBES': ('probe_name', 'probe_id'),
        'SERVICES': ('service_name', 'service_id'),
        'DESTINATIONS': ('destination_name', 'destination_id'),
        'RUNNING_SERVICES': ('distinct(select service_name from SERVICES where RUNNING_SERVICES.service_id=SERVICES.service_id)', 'id'),
        'RUNNING_DESTINATIONS': ('distinct(select destination_name from DESTINATIONS where RUNNING_DESTINATIONS.destination_id=DESTINATIONS.destination_id)', 'id'),
    }
    word = db.select("SELECT {select} FROM {table} WHERE {cond}='{val}';".format(select=mapping[table][0], table=table, cond=mapping[table][1], val=id))[0][0]

    sql_insert = 'INSERT INTO `LOGGING_EVENTS` VALUES ("Null", "{user}", "{ty}", "{tlb}", "{word}", "{sql}", NOW())'.format(user=user, ty=type, tlb=table, word=word, sql=sql)
    db.mycursor.execute(sql_insert)
    db.connection.commit()

db.insert('RUNNING_SERVICES', [('null', 'bkk2', '1', '2')])
logging(user='admin', type='insert', table='RUNNING_SERVICES', sql="INSERT INTO RUNNING_SERVICES VALUES ('null', ''bkk2', '1', '2')")

# def hello(fname=None, lname=None, **kwargs):
#     print 'First name:', fname, 'Last Name:', lname
#
# hello(lname='fluke', fname='lastnamefluke')