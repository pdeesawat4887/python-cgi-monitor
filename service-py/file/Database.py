#!/usr/bin/python

import mysql.connector
from pip._vendor.colorama import Fore, Style

class MySQLDatabase:

    def __init__(self):
        '''Create connection to MariaDB SQL'''
        self.create_connection()

    # def create_connection(self, user='centos', passwd='root', host='192.168.1.8', database='project_vm'):
    def create_connection(self, user='catma', passwd='root', host='127.0.0.1', database='project_vm'):
        try:
            self.connection = mysql.connector.connect(user=user, password=passwd, host=host, database=database)
            self.mycursor = self.connection.cursor()
        except Exception as error:
            print 'Error database: ', Fore.RED, error, Style.RESET_ALL

    def query_probe(self, id, name, ip, mac_address):
        ''' Check before test, that database contain this probe '''
        query_sql = "SELECT probe_id FROM probe WHERE probe_id='{}'".format(id)
        self.mycursor.execute(query_sql)
        my_result = self.mycursor.fetchall()
        if self.mycursor.rowcount == 1:
            probe_id = my_result[0][0]
        else:
            self.insert_new_probe(id=id, name=name, ip=ip, mac_address=mac_address)
            probe_id = id
        return probe_id

    def insert_new_probe(self, id, name, ip, mac_address):
        ''' If probe doesn't exist in database, insert probe first '''
        insert_sql = "INSERT INTO probe VALUES ('{}', '{}', '{}', '{}', '0')".format(id, name, ip, mac_address)
        self.mycursor.execute(insert_sql)
        self.connection.commit()

    def insert_availability_service(self, list_data):
        ''' Insert row to availability_service from list of data that contain id(AUTO_IN), configure_id, status, response_time, time '''
        insert_sql = "INSERT INTO availability_service VALUES (NULL, %s, %s, %s, %s, %s)"
        self.mycursor.executemany(insert_sql, list_data)
        self.connection.commit()

    def insert_performance_service(self, list_data):
        ''' Insert row to performance_service from list of data that contain id(AUTO_IN), configure_id, status, response_time, time '''
        insert_sql = "INSERT INTO performance_service VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)"
        self.mycursor.executemany(insert_sql, list_data)
        self.connection.commit()

    def query_service(self, service_id):
        ''' Get service_name for Line Notify '''  ### Unuse line notify at here
        query_sql = "SELECT service_name FROM service WHERE service_id='{}'".format(service_id)
        self.mycursor.execute(query_sql)
        my_result = self.mycursor.fetchone()
        return my_result[0]

    def close_connection(self):
        ''' Close connection to MariaDB SQL '''
        self.mycursor.close()
        self.connection.disconnect()
        print 'Terminate Connection'

