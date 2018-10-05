# import base64
#
# print base64.b64encode('p@ssword')
#
# abc = '/api-man/probe'
#
# cba = abc.split('/')[2::]
#
# key = cba[0]
#
# print key
#
# sql = 'SELECT {select} FROM {table}'
#
# # print sql.format(select='*', table='probe')
#
# select = []
#
# print sql.format(select=', '.join(map(lambda item: '`{}`'.format(item), select)), table='probe')


# input_user = ['DROP `table`;', 'probe_name']
#
# for i in input_user:
#     print i.find(';') != -1

import json

# # json_data = []
# temp = [u'iadr', u'madr']
# data = [(u'192.168.254.32', u'00:50:56:ad:51:1f'), (u'192.168.254.33', u'00:50:56:ad:6d:79'),
#         (u'10.5.3.26', u'00:50:56:ad:e3:44'), (u'192.168.51.102', u'a0:99:9b:04:6c:ed'),
#         (u'192.168.254.34', u'b8:27:eb:15:59:8a')]
#
#
#
# # for result in data:
# #     json_data.append(dict(zip(temp, result)))
# # print json.dumps(json_data)
# #
# # # print output
# # # print dict(output)
# # json_data = []
# json_data = map(lambda result: dict(zip(temp, result)), data)
# # print json.dumps(json_data)


# import string
# import re
#
# r = re.compile(r'[a-zA-Z]+')
# print "WELCOME FOR NAME VERIFICATION. TYPE ALPHABETS ONLY!"
# x = raw_input("Your Name:")
#
# while not r.match(x):
#     print "Come on,'", x,"' can't be your name"
#     x = raw_input("Your Name:")
#
# if 5<=len(x)<=10:
#     print "Hi,", x, "!"
# elif len(x)>10:
#     print "Mmm,Your name is too long!"
# elif len(x)<5:
#     print "Alas, your name is too short!"
#
# raw_input("Press 'Enter' to exit!")
#
# dic = {
#     'apple': 'hello',
#     'world': 'banana',
#     'best': None
# }
#
# text = "FROM user"
#
# # for i in dic:
# text += ' and '.join(map(lambda item: "{key}:{value}".format(key=item, value=dic[item]) if dic[item] != None else "1=1", dic))
#
# print text

# override = "get"

# name = None
# lname = 'foo'
# fname = 'bar'
# listy = []
#
# listy.append((name, lname, fname))
#
# print listy
#

import database

db = database.MySQLDatabase()

sql = "UPDATE `running_service` SET `running_status`=%s WHERE `probe_id`=%s and `service_id`=%s;"
data = [
    (1, "ba27ebfffe15598a", 1),
    (1, "ba27ebfffe15598a", 2),
    (1, "ba27ebfffe15598a", 3),
    (1, "ba27ebfffe15598a", 4),
    (1, "ba27ebfffe15598a", 5),
    (1, "ba27ebfffe15598a", 6),
    (1, "ba27ebfffe15598a", 7),
    (1, "ba27ebfffe15598a", 8),
    (1, "ba27ebfffe15598a", 21),
    (1, "ba27ebfffe15598a", 26),
    (1, "ba27ebfffe15598a", 27),
]

db.mycursor.executemany(sql, data)
db.connection.commit()
