from functools import partial

def test(length, value=None):
    if value != None:
        print 'HAS VALUE: {val} length {length}'.format(val=value, length=length)

def test2(length, value=None):
    if value == None:
        print 'HAS VALUE: {val} length {length}'.format(val=value, length=length)

options = {1: partial(test, '12'),
           2: partial(test2, '21')}

options[1](value='hello')
