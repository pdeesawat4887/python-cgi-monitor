import main.database as mariadb


class destination(mariadb.MySQLDatabase):

    def __init__(self):
        mariadb.MySQLDatabase.__init__(self)

    def get_service(self):
        data = []
        list_service = []
        list_service = self.select('service', None, 'service_id', 'service_name')
        return list_service

    def get_destination(self, service_id):
        query_sql = "SELECT destination_id, destination, destination_port FROM destination INNER JOIN service ON destination.service_id=service.service_id WHERE destination.service_id={}".format(service_id)
        self.mycursor.execute(query_sql)
        return self.mycursor.fetchall()

if __name__ == '__main__':
    pass