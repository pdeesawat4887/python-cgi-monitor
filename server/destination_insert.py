#!/usr/bin/python

import cgi
import main.database as mariadb

print "Content-type: text/html\n\n"


def insert_new_destination():
    database = mariadb.MySQLDatabase()

    form = cgi.FieldStorage()
    form_dest = form.getvalue('destination')
    form_port = form.getvalue('destination_port')
    form_service = form.getvalue('TypeList')

    if form_port is None:
        form_port = None

    data = [(None, form_service, form_dest, form_port)]
    database.insert(table='destination', list_data=data)

    print "Insert Successfully"

if __name__ == '__main__':
    insert_new_destination()
