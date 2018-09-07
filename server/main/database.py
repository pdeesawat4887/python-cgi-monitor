#!/usr/bin/python

import mysql.connector
import os
import sys
from pip._vendor.colorama import Fore, Style


class MySQLDatabase:
    setting = {}

    def __init__(self):
        self.path = os.path.dirname(sys.argv[0])
        self.prepare_setting(file=self.path + "/main/conf/configuration")
        self.create_connection()

    def prepare_setting(self, file):
        ''' Open and read configure file to prepare for database, probe and service test '''
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

    def select(self, table, where=None, *args, **kwargs):
        query = "SELECT "
        keys = args
        values = tuple(kwargs.values())
        length = len(keys) - 1

        for attribute, key in enumerate(keys):
            query += key
            if attribute < length:
                query += ","

        query += " FROM %s" % table
        if where:
            query += " WHERE %s" % where

        self.mycursor.execute(query, values)
        my_result = self.mycursor.fetchall()
        return my_result

    def insert(self, table, list_data):

        query = "INSERT INTO %s " % table
        query += " VALUES (" + ",".join(["%s"] * len(list_data[0])) + ")"

        self.mycursor.executemany(query, list_data)
        self.connection.commit()

    def set_probe(self, id, name, ip, mac_address):
        ''' Check before test, that database contain this probe '''
        condition = "probe_id = %s"
        my_result = self.select('probe', condition, 'probe_id', probe_id=id)

        if my_result.__len__() == 1:
            self.update_probe(id, name, ip, mac_address, self.path)
        else:
            temp_db = []
            self.insert('probe', [(id, name, ip, mac_address, 0, self.path)])
            service_result = self.select('service', None, 'service_id')

            for service_id in service_result:
                temp = (id, service_id[0], 0)
                temp_db.append(temp)
            self.insert('running_service', temp_db)

    def update_probe(self, id, name, ip, mac_address, path):
        update_sql = "UPDATE probe SET probe_name='{}', ip_address='{}', mac_address='{}', status='{}', path='{}' WHERE probe_id='{}'".format(
            name, ip, mac_address, 0, path, id)
        self.mycursor.execute(update_sql)
        self.connection.commit()

    def close_connection(self):
        ''' Close connection to MariaDB SQL '''
        self.mycursor.close()
        self.connection.disconnect()
