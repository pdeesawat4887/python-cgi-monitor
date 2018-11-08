#!/usr/bin/python

import main.database as maria
import csv

db = maria.MySQLDatabase()

def create_csv():
    sql = "SELECT * FROM PROBES;"
    db.mycursor.execute(sql)
    output_description = tuple([field[0] for field in db.mycursor.description])
    m_list = db.mycursor.fetchall()

    with open('persons.csv', 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['PROBES'])
        filewriter.writerow(output_description)
        for row in m_list:
            filewriter.writerow(row)

def example_csv():
    with open('persons.csv', 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Name', 'Profession'])
        filewriter.writerow(['Derek', 'Software Developer'])
        filewriter.writerow(['Steve', 'Software Developer'])
        filewriter.writerow(['Paul', 'Manager'])

create_csv()
# example_csv()