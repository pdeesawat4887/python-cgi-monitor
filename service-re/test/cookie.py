import time
import sys

class Sweet:

    def __init__(self, level, type):
        self.level = level
        self.type = type

    def print_info(self):
        print "Type {} at level: {}".format(self.type, self.level)

    def information(self, text):
        print "Text input is: {}".format(text)


class Manager(Sweet):

    def __init__(self, first):
        self.first = first

    # def __init__(self, level, type, first):
    #     Sweet.__init__(self, level, type)
    #     self.first = first

        print "My name is {} and i have level at {}".format(self.first, self.level)




# if __name__ == '__main__':
#
#     # see = Sweet()
#     first_arg = sys.argv[0]
#     second_arg = sys.argv[1]
#     # third_arg = sys.argv[2]
#     # badboy = Manager(first_arg, second_arg, third_arg)
#     # badboy = Manager(first_arg, second_arg, third_arg)
#
#     badboy = Manager(first_arg)
#     badboy.information(second_arg)

# fara = {'apple':1, 'banana':2, 'orange':3}
#
# if 'orange' in fara:
#     print fara['orange']

class Parent:
    first  = 'pacharapol'
    last = 'deesawat'

    def get_name(self):
        print self.first, self.last

class Child(Parent):
    first = 'yomost'

example = Child()
example.get_name()


class aaa:

    def hello(self):
        print 'aaa hello'


class bbb:

    def hello(self):
        print 'bbb hello'


class ccc:

    def hello(self):
        print 'ccc hello'

dict = {'apple': aaa, 'banana': bbb, 'cat': ccc}

test = dict['apple']()
test.hello()