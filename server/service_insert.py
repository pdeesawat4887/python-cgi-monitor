#!/usr/bin/python

import cgi
import main.database as mariadb

print "Content-Type: text/html\n"


def insert_new_service():

    form = cgi.FieldStorage()

    service_name = form.getvalue('service_name')
    file_name = form.getvalue('file_name')
    try:
        database = mariadb.MySQLDatabase()
        data = [(None, service_name, file_name)]
        database.insert(table='service', list_data=data)
        condition = 'file_name = %s'
        data = database.select('service', condition,
                               'service_id', file_name=file_name)

        temp_data = []
        all_probe = database.select('probe', None, 'probe_id')
        for probe in all_probe:
            probe_id = probe[0]
            temp = (probe_id, data[0][0], '1')
            temp_data.append(temp)
        database.insert(table='running_service', list_data=temp_data)

        print """<p class="title is-6">Insert {} Successfully!</p>""".format(service_name)
        print """<p class="title is-6"> service_id is '{}'</p>""".format(data[0][0])
        print """<a class="button is-link" href="../template.txt" download>Download file</a>"""
    except Exeception as error:
        print """<p class="title is-6" >{}</p>""".format(error)


if __name__ == '__main__':
    insert_new_service()
