#!/usr/bin/python

import mysql.connector
import base64


class MySQLDatabase:

    def __init__(self):
        self.host = '192.168.254.31'
        self.user = 'monitor'
        # self.password = base64.b64decode("c2VydmljZV9tb25pdG9y")
        self.password = 'p@ssword'
        self.database = 'project_monitor_release_copy'

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
        self.mycursor.executemany(query, list_data)
        self.connection.commit()

    def commit_sql_statement(self, sql_cmd):
        self.mycursor.execute(sql_cmd)
        self.connection.commit()

    # def insert_dup(self, table, list_data):
    #     query = "INSERT INTO %s " % table
    #     query += "VALUES (" + ",".join(["%s"] * len(list_data[0])) + ") ON DUPLICATE KEY"
    #     print query
    #     self.mycursor.executemany(query, list_data)
    #     self.connection.commit()

    def close_connection(self):
        self.mycursor.close()
        self.connection.disconnect()


if __name__ == '__main__':
    db = MySQLDatabase()
    print db.select('select * from DESTINATIONS')
