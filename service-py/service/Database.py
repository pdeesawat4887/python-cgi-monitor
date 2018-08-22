#!/usr/bin/python

import mysql.connector
from pip._vendor.colorama import Fore, Style


class MySQLDatabase:
    setting = {}

    def __init__(self):
        '''Create connection to MariaDB SQL'''
        self.prepare_setting(file='conf/server')
        self.create_connection()

    def prepare_setting(self, file):
        ''' Open and read configure file to prepare for probe and service test '''
        infile = open(file, "r")
        for line in infile:
            if not line.strip():
                continue
            else:
                if not '#' in line:
                    key, value = line.strip().split('=')
                    self.setting[key] = value
        infile.close()

    def create_connection(self):
        try:
            self.connection = mysql.connector.connect(user=self.setting['mysql_user'],
                                                      password=self.setting['mysql_password'],
                                                      host=self.setting['mysql_host'],
                                                      database=self.setting['mysql_database'])
            self.mycursor = self.connection.cursor()
        except Exception as error:
            print 'Error database: ', Fore.RED, error, Style.RESET_ALL

    def query_all_probe(self):
        try:
            query_sql = "SELECT probe_id, ip_address FROM probe"
            self.mycursor.execute(query_sql)
            my_result = self.mycursor.fetchall()
            return my_result
        except Exception as error:
            print 'Error', error

    def query_active_service(self, probe_id):
        query_sql = "SELECT service_id FROM setting WHERE probe_id='{}' and setting='0';".format(probe_id)
        self.mycursor.execute(query_sql)
        my_result = self.mycursor.fetchall()
        return my_result

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
        temp_db = []
        insert_sql = "INSERT INTO probe VALUES ('{}', '{}', '{}', '{}', '0')".format(id, name, ip, mac_address)
        self.mycursor.execute(insert_sql)
        self.connection.commit()

        service_result = self.query_all_service()

        for service_id in service_result:
            temp = (id, service_id[0], 0)
            temp_db.append(temp)
        self.insert_active_new_probe(temp_db)

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

    def query_all_service(self):
        query_sql = "SELECT service_id FROM service"
        self.mycursor.execute(query_sql)
        my_result = self.mycursor.fetchall()
        return my_result

    def insert_active_new_probe(self, list_data):
        insert_sql = "INSERT INTO setting VALUES (%s, %s, %s)"
        self.mycursor.executemany(insert_sql, list_data)
        self.connection.commit()

    def query_service(self, service_id):
        ''' Get service_name for Line Notify '''
        query_sql = "SELECT service_name FROM service WHERE service_id='{}'".format(service_id)
        self.mycursor.execute(query_sql)
        my_result = self.mycursor.fetchone()
        return my_result[0]

    def close_connection(self):
        ''' Close connection to MariaDB SQL '''
        self.mycursor.close()
        self.connection.disconnect()
        print 'Terminate Connection'

if __name__ == '__main__':
    xxx = MySQLDatabase()
    print xxx.setting