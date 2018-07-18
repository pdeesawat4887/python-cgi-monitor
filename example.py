# x = {'apple': [123, 456, 789, 'hello'], 'banana': [696969]}
#
# for it in x:
# 	for nn in x[it]:
# 		print nn
#
#
# def create_dict(dict, file):
#     with open(file) as f:
#         for line in f:
#             key, value = line.strip().split()
#             dict[key] = value.split(',')
#
# dict_oid = {}
# create_dict(dict_oid, "oid_list.txt")
#
# print dict_oid
#
# for it in dict_oid:
# 	for nn in dict_oid[it]:
# 		print nn
#
# num = 15
# print type(num)
#
# num = str(num)
# print num
# print type(num)

# class Hello():
#
#     def __init__(self, id):
#         self.id = id
#
#     def test(self):
#         print "Hello, Class Hello"
#
# objs = [Hello(i) for i in range(5)]
#
#
#     print i.id


import ast
list = '["192.168.1.5","192.168.1.8"]'
x = ast.literal_eval(list)
x = [n.strip() for n in x]

for i in x:
    print i