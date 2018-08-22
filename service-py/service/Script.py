#!/usr/bin/python

import socket
import re, uuid
import time
import os
import sys
import subprocess
import urlparse
import requests
import bitmath
import speedtest
import smtplib
import poplib
import imaplib
import youtube_dl
from pip._vendor.colorama import Fore, Style

import Database
import ProbeFile


class Service(ProbeFile.Probe):
    data = {}

    def __init__(self):
        ProbeFile.Probe.__init__(self)

    def check_response_code(self, response_code):
        ''' Reference from HTTP status code return 0 if status = 2xx, return 1 if invalid or error status and return 2 if status = 4xx-5xx or fail to connection '''
        try:
            if (200 <= int(response_code) <= 299):
                result = 0
            else:
                result = 2
        except Exception as error:
            result = 1
            print 'Error: ', Fore.RED, error, Style.RESET_ALL
        return result

    def get_time_format(self):
        ''' Return time format for database like 2018-08-01 09:06:09 '''
        return time.strftime('%Y-%m-%d %H:%M:%S')

    def get_time(self):
        ''' Return current time '''
        return time.time()

    def get_response_time(self, start, end):
        ''' Return different milli second from 2 different time'''
        return (end - start) * 1000

    def round_2_decimal(self, value):
        ''' Return the floating point value number rounded to 2 digits after the decimal point form input '''
        try:
            return round(float(value), 2)
        except:
            return 'NULL'

    def identify_url(self, url):
        ''' Return 6 tuple correspond to general structure of a URL '''
        return urlparse.urlparse(url)

    def convert_to_mbs(self, number_of_bytes):
        ''' Return Megabit per second from byte per second '''
        try:
            return bitmath.MiB(bytes=number_of_bytes)
        except:
            return 'NULL'

    def query_data(self, service_id):
        ''' Get destination and information from input service_id prepare to use for test '''
        query_sql = "SELECT * FROM configuration WHERE service_id='{}'".format(service_id)
        self.mycursor.execute(query_sql)
        self.result = self.mycursor.fetchall()

    def availability_service(self, service_id, warning_value=2):
        ''' Step to prepare destination, set parameter, testing, prepare attribute before insert to availability_service and insert data '''
        data_for_database = []
        self.query_data(service_id)

        time_start = self.get_time_format()

        for counter in self.result:
            counter = list(counter)

            destination = self.reformat_counter(counter[2])
            status, response = self.get_status(destination, counter[3])
            response = self.round_2_decimal(response)

            temp = (self.id, counter[0], status, response, time_start)
            data_for_database.append(temp)

        self.insert_availability_service(data_for_database)
        print "SUCCESS INSERT DATA", service_id
        data_for_database = []
        # self.close_connection()

    def performance_service(self, service_id, warning_value=2):
        ''' Step to prepare destination, set parameter, testing, prepare attribute before insert to performance_service and insert data '''
        data_for_database = []
        self.query_data(service_id)

        time_start = self.get_time_format()

        for counter in self.result:
            counter = list(counter)

            destination = self.reformat_counter(counter[2])
            ping, download, upload, location = self.get_status(destination, counter[3])
            download = self.round_2_decimal(self.convert_to_mbs(download))
            upload = self.round_2_decimal(self.convert_to_mbs(upload))

            temp = (self.id, counter[0], ping, download, upload, location, time_start)
            data_for_database.append(temp)

        self.insert_performance_service(data_for_database)
        print "SUCCESS INSERT DATA", service_id
        data_for_database = []
        # self.close_connection()

    def get_status(self, destination, port):
        ''' Abstract function: Return status and response for availability service and
         return ping, download, upload, location for performance service.
         Every new service must override this function that importance to get status and other parameter for different service '''
        pass

    def reformat_counter(self, destination):
        ''' Override this function to format destination If format from database cannot use immediate '''
        return destination

    # def notify_line(self, probe_name, ip, service, destination, status, warning_value):
    #
    #     if status == warning_value:
    #         url = 'https://notify-api.line.me/api/notify'
    #         token = 'pyL4xY6ys303vg0bVnvd0DRco7UyILVo5dOXZGjBWD8'
    #         headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    #
    #         msg = '\nWARNING !!!\nProbe Name: {}\nIP Address: {}\nService: {}\nDestination: {}\nStatus: {}\nPlease check your service'.format(
    #             probe_name, ip, service, destination, status)
    #
    #         request = requests.post(url, headers=headers, data={'message': msg})
    #
    #         print request.text
