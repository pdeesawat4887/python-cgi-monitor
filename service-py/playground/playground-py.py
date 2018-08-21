
xxx = {u'aaaaaa': u'192.168.1.1', u'a2999bfffe046ced': u'192.168.1.8'}
xxx.update({'apple': 'banaba', 'banana': 'Antt'})

# print xxx

def reading():
    s = open('../conf/dictionary', 'r').read()
    whip = eval(s)
    print type(whip)
    print whip

reading()