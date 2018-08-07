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


### return 0: active, working
### return 1: Inactive, Not working
### return 2: Error
### return 3: Unknow


class Service:
    setting = {}

    def __init__(self):
        self.configure_setting()

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
            print 'Error: ', Fore.RED, error, Style.RESET_ALL  #########
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
        Service.__init__()
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
        Service.__init__(self)
        self.get_host()

    def get_host(self):
        origin_host = self.read_file(file='conf/website_conf.txt')
        for host in origin_host:
            self.host.append(self.identify_url(host))

    def get_website_status_whois(self, url):
        temp_url = url.replace('www.', '')
        result_whois = pythonwhois.get_whois(temp_url)

        try:
            checker = result_whois['status'][0].lower()
            if 'active' in checker:
                result_status = 0
            elif 'prohibited' in checker:
                result_status = 3
            else:
                result_status = 2
        except Exception as error:
            result_status = 2
            print 'Error: ', Fore.RED, error, Style.RESET_ALL

        return result_status

    def get_website_request(self, url):
        header = {'User-Agent': self.setting['User-Agent']}
        try:
            res_http = requests.get(url, headers=header)
            checker = res_http.status_code
            res_http.close()
            return self.check_response_code(checker)
        except Exception as error:
            print 'Error: ', Fore.GREEN, error, Style.RESET_ALL
            return 2

    def main(self):
        for url in self.host:
            print '-------------> ', url.netloc

            ping = self.ping_once(url.netloc)
            status_whois = self.get_website_status_whois(url.netloc)
            status_req = self.get_website_request(url.scheme + '://' + url.netloc)

            print ping
            print status_whois
            print status_req


test = Website()
# test.get_website_request('https://shopee.co.th')
# print test.host
test.main()
# test.get_website_request()
