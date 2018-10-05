#!/usr/bin/python

import mysql.connector
import base64


class MySQLDatabase:

    def __init__(self):
        self.host = '172.16.30.176'
        self.user = 'monitor'
        self.password = base64.b64decode('cEBzc3dvcmQ=')
        self.database = 'project_monitor_dump'
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

    def close_connection(self):
        self.mycursor.close()
        self.connection.disconnect()
