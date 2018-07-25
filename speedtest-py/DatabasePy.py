#!/usr/bin/env python

import MySQLdb


class Database:

    # dbc = ("localhost", "root", "root", "test-catma")

    def __init__(self, host, user, passwd, database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
    # End of __init__

    def openConnection(self):
        try:
            db = MySQLdb.connect(self.host, self.user,
                                 self.passwd, self.database)
            self.connection = db
            self.session = db.cursor()
        except MySQLdb.Error as e:
            print 'Error {} {}'.format(e.args[0], e.args[1])
    # End of openConnection

    def closeConnection(self):
        self.session.close()
        self.connection.close()
    # End of closeConnection

    def select(self, table, where=None, *args, **kwargs):
        result = None
        query = 'SELECT '
        keys = args
        values = tuple(kwargs.values())
        l = len(keys) - 1

        for item, key in enumerate(keys):
            query += key + ' '
            if item < l:
                query += ','

        query += 'FROM {}'.format(table)
        # End of SELECT

        if where:
            query += ' WHERE {}'.format(where)
        # End of WHERE

        self.openConnection()
        print "%"
        print "------------>", query
        print "VALUES ----->", values
        self.session.execute(query, values)
        numRow = self.session.rowcount
        numColumn = len(self.session.description)

        if numRow >= 1 and numColumn > 1:
            result = [item for item in self.session.fetchall()]
        else:
            result = [item[0] for item in self.session.fetchall()]


        self.closeConnection()
        return result
    # End of select

    def update(self, table, where=None, *args, **kwargs):
        query = 'UPDATE {} SET '.format(table)
        keys = kwargs.keys()
        values = tuple(kwargs.values()) + tuple(args)
        l = len(keys) - 1
        for item, key in enumerate(keys):
            query += key + ' = %s'
            if i < l:
                query += ','
        query += ' WHERE {}'.format(where)

        self.openConnection()
        self.session.execute(query, values)
        self.connection.commit()
        updateRows = self.session.rowcount
        self.closeConnection()

        return updateRows
    # End of update

    def insert(self, table, *args, **kwargs):
        values = None
        query = "INSERT INTO {} ".format(table)
        if kwargs:
            keys = kwargs.keys()
            values = tuple(kwargs.values())
            query += "(" + ",".join(["`%s`"] * len(keys)) % tuple(keys) + \
                ") VALUES (" + ",".join(["%s"] * len(values)) + ")"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"] * len(values)) + ")"

        self.openConnection()
        self.session.execute(query, values)
        self.connection.commit()
        self.closeConnection()
        return self.session.lastrowid
        # End def insert

    #     db = MySQLdb.connect(*self.dbc)
    #     self.cursor = db.cursor()

    # def query(self, sql):
    #     self.cursor.execute(sql)
    #     return self.cursor.fetchall()

    # def rows(self):
    #     return self.cursor.rowcount
conditional_query = "host like '%s'"
databaseCon = Database('localhost', 'root', 'root', 'test-catma')
# sql = "SELECT * FROM devices"
result = databaseCon.select("devices", conditional_query, 'host', 'upload', 'download', host="test%")
# databaseCon.query(sql)
# print databaseCon.rows()
print result