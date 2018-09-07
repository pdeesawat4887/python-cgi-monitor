#!/usr/bin/python

import cgi
import main.database as mariadb

print "Content-type: text/html\n\n"


def update_destination():
    database = mariadb.MySQLDatabase()
    form = cgi.FieldStorage()

    form_dest = form.getvalue('dest')
    form_port = form.getvalue('port')
    form_dest_id = form.getvalue('d_id')

    if form_port is None or form_port == 'None':
        form_port = 'NULL'

    update_sql = "UPDATE destination SET destination='{}', destination_port={} WHERE destination_id='{}'".format(
        form_dest, form_port, form_dest_id)
    database.mycursor.execute(update_sql)
    database.connection.commit()
    print "Update Successfully!"

if __name__ == '__main__':
    update_destination()
