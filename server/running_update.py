#!/usr/bin/python

import cgi
import main.database as mariadb

print "Content-type: text/html\n\n"


def update_running():
    database = mariadb.MySQLDatabase()

    form = cgi.FieldStorage()

    probe_id = form.getvalue('probe_id')
    service_id = form.getvalue('service_id')
    status_service = form.getvalue('status_service')

    update_sql = "UPDATE running_service SET running='{}' WHERE probe_id='{}' and service_id='{}' ".format(status_service, probe_id, service_id)
    database.mycursor.execute(update_sql)
    database.connection.commit()

    print "Update Successfully"

if __name__ == '__main__':
    update_running()
