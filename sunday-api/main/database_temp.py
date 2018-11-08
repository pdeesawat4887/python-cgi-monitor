#!/usr/bin/python

import mysql.connector
import base64


class MySQLDatabase:

    def __init__(self):
        self.host = '192.168.254.31'
        self.user = 'monitor'
        self.password = base64.b64decode('cEBzc3dvcmQ=')
        self.database = 'project_monitor_release_temp'
        self.create_connection()

    def create_connection(self):
        try:
            self.connection = mysql.connector.connect(
                user=self.user, password=self.password, host=self.host, database=self.database)
            self.mycursor = self.connection.cursor()
        except Exception as error:
            print "Error database:", error

    def select(self, sql_query):
        self.mycursor.execute(sql_query)
        return self.mycursor.fetchall()

    def insert(self, table, list_data):
        query = "INSERT INTO %s " % table
        query += "VALUES (" + ",".join(["%s"] * len(list_data[0])) + ")"
        try:
            self.mycursor.executemany(query, list_data)
        except:
            self.connection.rollback()
            raise
        else:
            self.connection.commit()
        # self.connection.commit()

    def foreign_key_func(self, func='enable', **kwargs):
        option = {
            'disable': '0',
            'enable': '1',
        }
        try:
            sql = "SET FOREIGN_KEY_CHECKS={func};".format(func=option[func])
        except Exception as error:
            print "Error database:", error
        self.mycursor.execute(sql)
        self.connection.commit()

    def execute_insert(self, table, list_data):
        query = "INSERT IGNORE INTO %s " % table
        query += "VALUES (" + ",".join(["%s"] * len(list_data[0])) + ")"
        try:
            self.mycursor.executemany(query, list_data)
        except:
            self.connection.rollback()
            raise

    def close_connection(self):
        self.mycursor.close()
        self.connection.disconnect()


# if __name__ == '__main__':
#     hello = MySQLDatabase()
#     hello.mycursor.execute('SELECT COUNT(`service_id`) FROM SERVICES;')
#     svc = hello.mycursor.fetchall()[0][0]
#     hello.mycursor.execute('SELECT COUNT(`probe_id`) FROM PROBES;')
#     pb = hello.mycursor.fetchall()[0][0]
#     hello.mycursor.execute('SELECT COUNT(`destination_id`) FROM DESTINATIONS;')
#     dest = hello.mycursor.fetchall()[0][0]
#     hello.mycursor.execute('SELECT COUNT(`result_id`) FROM TESTRESULTS WHERE `result_status`!=1;')
#     test = hello.mycursor.fetchall()[0][0]
#
#     # json_data = map(lambda result: dict(zip(self.attribute, result)), data)
#
#     collection = [[svc, pb, dest, test]]
#     # print collection
#     oo = ['service', 'probe', 'destination', 'result']
#
#     # hhh = zip(collection, oo)
#     # print hhh
#     import json
#
#     print(json.dumps([dict(zip(oo, row)) for row in collection], indent=1))

    # json_data = map(lambda result: dict(zip(oo, result)), collection)

    # json_d = map(lambda item, attr: dict(item, attr), collection, oo)
    # print json_d

    #
    # json_data = {'service': svc,
    #              'probe': pb,
    #              'destination': dest,
    #              'test_result': test}
    #
    # print json_data

    # hello.foreign_key_func()
    # hello.insert('DESTINATIONS', [('NULL', 1, 'www.gh.comwqeqeqewqewqsfdsfssfdsfsdffsjieurfojfiosjfikdjkkxdfserfewsfefrfrgwww.gh.comwqeqeqewqewqsfdsfssfdsfsdffsjieurfojfiosjfikdjkkxdfserfewsfefrfrgwww.gh.comwqeqeqewqewqsfdsfssfdsfsdffsjieurfojfiosjfikdjkkxdfserfewsfefrfrg', 12356789, 'hello girl')])
    # print int(hello.select("SELECT count(`result_id`) FROM TESTRESULTS")[0][0])