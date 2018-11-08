#!/usr/bin/python

import main.database as mariadb
import cgi


def add_running_services(collection_id):
    list_services = map(lambda item: item[0], db.select("SELECT `service_id` FROM SERVICES"))
    list_run_svc = map(lambda item: (collection_id, item, 2), list_services)
    return list_run_svc


def add_running_destinations(collection_id):
    list_destinations = map(lambda item: item[0], db.select("SELECT `destination_id` FROM DESTINATIONS"))
    list_run_dest = map(lambda item: (collection_id, item, 1), list_destinations)
    return list_run_dest


def add_services_destinations(probe_id):
    collection_id = db.select("SELECT `collection_id` FROM PROBES WHERE `probe_id`='{ipb}'".format(ipb=probe_id))[0][0]
    db.insert('RUNNING_SERVICES', add_running_services(collection_id))
    db.insert('RUNNING_DESTINATIONS', add_running_destinations(collection_id))
    return collection_id


# if __name__ == '__main__':
#     form = cgi.FieldStorage()
#     probe_id = form.getvalue('ipb', None)
#     db = mariadb.MySQLDatabase()
#
#     add_services_destinations('MZWGP7JOOWDXNYYF')
#
#     # if probe_id != None:
#     #     add_services_destinations('MRB3PR7OJQ51T7LO')


if __name__ == '__main__':
    db = mariadb.MySQLDatabase()
    db.insert('DESTINATIONS', [(None, 1, 'www.youtube.com', 443, 'youtube video')])
    idest = db.mycursor.lastrowid
    print idest