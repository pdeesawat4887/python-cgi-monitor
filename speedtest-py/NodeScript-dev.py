import speedtest
import time
import struct
from firebase import firebase
import socket
import os
import urllib
import smtplib
import poplib
import imaplib
import sys
import subprocess
import mysql.connector
import pythonwhois
import urlparse
import requests
from contextlib import contextmanager

# Extra for Exception
from pip._vendor.colorama import Fore, Style


class Service:
    setting = {}

    def configure_setting(self, file='conf/setting.txt'):
        infile = open(file, "r")
        for line in infile:
            if not line.strip():
                continue
            else:
                key, value = line.strip().split('=')
                self.setting[key] = value
        infile.close()

    def convert_byte(self, number_of_bytes):
        if number_of_bytes < 0:
            raise ValueError("!!! number_of_bytes can't be smaller than 0 !!!")

        step_to_greater_unit = 1024.

        number_of_bytes = float(number_of_bytes)
        unit = 'bytes'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'KB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'MB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'GB'

        if (number_of_bytes / step_to_greater_unit) >= 1:
            number_of_bytes /= step_to_greater_unit
            unit = 'TB'

        precision = 1
        number_of_bytes = round(number_of_bytes, precision)

        return number_of_bytes

    def my_platform(self):
        platforms = {
            'linux1': '-c',
            'linux2': '-c',
            'darwin': '-c',
            'win32': '-n'
        }
        if sys.platform not in platforms:
            return sys.platform

        return platforms[sys.platform]

    def check_response_code(self, response_code):
        try:
            if (200 <= int(response_code) <= 299):
                result = 0
            else:
                result = 1
        except Exception as error:
            result = 2
            print 'Error: ', Fore.RED, error, Style.RESET_ALL
        return result

    def ping_once(self, destination):
        platform_count = self.my_platform()
        with open(os.devnull, 'w') as DEVNULL:
            try:
                subprocess.check_call(
                    ['ping', platform_count, '1', destination],
                    stdout=DEVNULL,
                    stderr=DEVNULL
                )
                is_up = 0
            except subprocess.CalledProcessError:
                is_up = 1
        return is_up

    def identify_url(self, url):
        return urlparse.urlparse(url)

    def current_date_time(self):
        current_date = time.strftime('%Y-%m-%d')
        current_time = time.strftime('%H:%M:%S')
        return current_date, current_time

    def read_file(self, file='conf/speedtest_list_re.txt'):
        file_read = []
        infile = open(file, "r")
        for line in infile:
            if not line.strip():
                continue
            else:
                if not '#' in line:
                    file_read.append(line.rstrip())
        infile.close()
        return file_read


class Speedtest(Service):
    server = []

    def __init__(self):
        self.temp_server = self.read_file('conf/speedtest_list_re.txt')
        self.get_server()

    def get_server(self):
        for server_num in self.temp_server:
            self.server.append(server_num.split(')')[0].replace(' ', ''))

    def test_speed(self, server):
        speed = speedtest.Speedtest()
        speed.get_servers([server])
        name = speed.get_servers([server]).values()[0][0]['name']
        speed.get_best_server()
        speed.download()
        speed.upload()
        result = speed.results.dict()
        return name, result['download'], result['upload'], result['ping']


class Website(Service):
    host = []

    def __init__(self):
        self.get_host()

    def get_host(self):
        temp_host = self.read_file(file='conf/website_conf.txt')
        for host in temp_host:
            self.host.append(self.identify_url(host))
