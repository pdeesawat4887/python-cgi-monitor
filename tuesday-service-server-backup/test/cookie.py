import time
import sys

class Sweet:

    def __init__(self, level, type, work=None, **kwargs):
        self.work = work
        self.level = level
        self.type = type
        self.print_info()
        self.work_hard()

    def print_info(self):
        print "Type {} at level: {}".format(self.type, self.level)

    def information(self, text):
        print "Text input is: {}".format(text)

    def work_hard(self):
        print "I work really hard for {}".format(self.work)


class Manager(Sweet):

    def __init__(self, first):
        self.first = first

        print "My name is {} and i have level at {}".format(self.first, self.level)

# candy = Sweet(1, 'sugar')

# even = []
# odd = []
#
# for i in range(100000):
#     if i%2 == 0:
#         even.append(i)
#     else:
#         odd.append(i)



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

# fara = ['apple', 'banana', 'orange']
# text = 'orange'
# if text in fara:
#     print text

protocol = "TCP"
file_name = 'service.py'

if file_name != None:
    print file_name
elif protocol.lower() == 'tcp':
    print "{} Choose".format(protocol)
