import main.database as mariadb_db
import json
# from datetime import date, datetime
import datetime


class API:
    # sql = "None"
    sql = 'SELECT * from {}'.format('probe')

    def get_data(self):
        database = mariadb_db.MySQLDatabase()
        database.mycursor.execute(self.sql)
        row_headers = [x[0] for x in database.mycursor.description]
        rv = database.mycursor.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        print json.dumps(json_data, default=self.json_serial)

    def json_serial(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        print TypeError("Type %s not serializable" % type(obj))

example = API()
example.get_data()