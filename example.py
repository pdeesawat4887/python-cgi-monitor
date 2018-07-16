x = {'apple': [123, 456, 789, 'hello'], 'banana': [696969]}

for it in x:
	for nn in x[it]:
		print nn


def create_dict(dict, file):
    with open(file) as f:
        for line in f:
            key, value = line.strip().split()
            dict[key] = value.split(',')

dict_oid = {}
create_dict(dict_oid, "oid_list.txt")

print dict_oid

for it in dict_oid:
	for nn in dict_oid[it]:
		print nn

num = 15
print type(num)

num = str(num)
print num
print type(num)