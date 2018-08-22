import paramiko
import Database
import getpass
import os
import threading


class Active(Database.MySQLDatabase):

    all_probe = {}

    def __init__(self):
        Database.MySQLDatabase.__init__(self)
        self.all_probe = dict(self.query_all_probe())

test = Active()
print test.all_probe
