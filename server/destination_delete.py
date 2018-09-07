#!/usr/bin/python

import cgi
import main.database as mariadb

print "Content-type: text/html\n\n"


def delete_destination():
    database = mariadb.MySQLDatabase()

    form = cgi.FieldStorage()

    del_id = form['del_id'].value

    del_sql_availability = "DELETE FROM availability_service WHERE destination_id='{}';".format(del_id)
    del_sql_performance = "DELETE FROM performance_service WHERE destination_id='{}';".format(del_id)
    del_sql_destination = "DELETE FROM destination WHERE destination_id='{}';".format(del_id)
    database.mycursor.execute(del_sql_availability)
    database.mycursor.execute(del_sql_performance)
    database.mycursor.execute(del_sql_destination)
    database.connection.commit()
    print """1 row successfully deleted"""

if __name__ == '__main__':
    delete_destination()
