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

    def what_myname(self):
        print "My name is {} and i have level at {}".format(self.first, self.level)




if __name__ == '__main__':

    # see = Sweet()
    first_arg = sys.argv[0]
    second_arg = sys.argv[1]
    # third_arg = sys.argv[2]
    # badboy = Manager(first_arg, second_arg, third_arg)
    # badboy = Manager(first_arg, second_arg, third_arg)

    badboy = Manager(first_arg)
    badboy.information(second_arg)