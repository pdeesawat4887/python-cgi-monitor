# import re
#
# all = {
#     'cond[iclus]': '1',
#     'val[iclus]': '1',
#     'val[ipb]': 'hello',
#     'val[clus_desc]': 'update clust description'
# }
#
# new = dict((re.compile("=?\[(.*)\]").search(key).group(1), value) for key, value in all.iteritems() if 'val' in key)
#
# print new
#
# # s = 'cond[ipb]'
# # p = re.compile("=?\[(.*)\]").search(s).group(1)
# # print p
#
# statement = "UPDATE CLUSTERS SET "
#
# statement += ', '.join(map(lambda item: "`{key}`='{value}'".format(key=item, value=new[item]), new))
#
# print statement

prac = ['abcdefghij', 'abc', 'hello', '1234567890', 'abcde12345']

def hello(str):
    if len(str) == 10:
        return str
    else:
        return None

box = filter(lambda item: hello(item), prac)

print box
print len(box)