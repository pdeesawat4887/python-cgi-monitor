import os
import random
import string
import database as maria
import sys
import time

# FILE_PATH = "/tmp/register.reg"
# if os.stat(FILE_PATH).st_size == 0:
#     id = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(16))
#     open(FILE_PATH, "wb").write(id)
# else:
#     id = open(FILE_PATH, "r").readline()
# print id
#
# print os.path.dirname(sys.argv[0])

db = maria.MySQLDatabase()

NAME = 'MACos'
IP = '192.254.51.102'
MAC = '00:50:56:ad:51:1f'
TIME = time.strftime('%Y-%m-%d %H:%M:%S')


def insert_probe(probe_temp_id):
    sql = "INSERT INTO PROBES VALUES ('{probe_id}', '{name}', '{ip}', '{mac}', '{status}', '{last_update}', '{date_add}', '{collection_id}') ON DUPLICATE KEY UPDATE `last_updated`=NOW()".format(
        probe_id=probe_temp_id, name=NAME, ip=IP, mac=MAC, status=3, last_update=TIME, date_add=TIME,
        collection_id=probe_temp_id)
    return sql


def update_probe(probe_temp_id):
    sql = "UPDATE PROBES SET `ip_address`='{ip}', `mac_address`='{mac}', `probe_status`='{status}', `last_updated`=NOW() WHERE `probe_id`='{probe_id}'".format(
        ip=IP, mac=MAC, status=3, probe_id=probe_temp_id
    )
    return sql


TEMP_FILE_REGISTER = "/Applications/XAMPP/xamppfiles/htdocs/python/python-cgi-monitor/monday-service-server/main/conf/temp"
REAL_FILE_REGISTER = "/Applications/XAMPP/xamppfiles/htdocs/python/python-cgi-monitor/monday-service-server/main/conf/reg"

# if os.stat(REAL_FILE_REGISTER).st_size != 0:
#     id = open(REAL_FILE_REGISTER, "r").readline()
# else:

# if os.stat(TEMP_FILE_REGISTER).st_size == 0:
#     id = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(16))
#     open(TEMP_FILE_REGISTER, "wb").write(id)
# else:
#     id = open(TEMP_FILE_REGISTER, "r").readline()
#
# print id
#
# db.mycursor.execute(insert_probe(id))
# db.connection.commit()

if os.path.isfile(TEMP_FILE_REGISTER) and os.access(TEMP_FILE_REGISTER, os.R_OK):
    print "File exists and is readable"
# try:
#     db.mycursor.execute(update_probe(id))
#     db.connection.commit()
#     print 'update'
# except Exception as e:
#     print e
#     db.mycursor.execute(insert_probe(id))
#     db.connection.commit()
