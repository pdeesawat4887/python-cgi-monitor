#!/usr/bin/python

import main.database as database
import os
import sys
import cgi
import json
from datetime import date, datetime
import decimal


# print "Status: 404 Not Found\r\n"
# print "Content-Type: text/html\n"
# print "Access-Control-Allow-Origin: *"
# print "Content-Type: application/json\n"

# argument = cgi.FieldStorage()
# print argument
# for a in os.environ:
#     print 'Var: ', a, 'Value: ', os.getenv(a), '<br>'
# print("all done")
# print dir(os.environ), '<br>'

class GetMethod:

    def __init__(self, arg, environ):
        self.db = database.MySQLDatabase()
        self.sql = None
        self.attribute = None
        self.argument = arg
        self.environ = environ
        self.prepare_statement()
        self.prepare_condition()
        self.prepare_order()
        self.prepare_limit()
        self.execute_sql(self.sql)

    def prepare_statement(self):
        # tlb = self.environ["REDIRECT_URL"].split('/')[2::][0]
        if self.argument.has_key('select[]'):
            self.attribute = self.argument.getvalue('select[]')
            if not isinstance(self.attribute, list):
                self.attribute = self.attribute.split(',')
            try:
                self.sql = "SELECT {select} FROM `{table}`".format(select=', '.join(map(lambda item: '`{item}`'.format(item=self.dict_attribute[item]), self.attribute)), table=self.table)
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print "Sorry !!! no attribute for show you. Please try again"
                exit()

    def prepare_condition(self):
        pass

    def prepare_order(self):
        pass

    def prepare_limit(self):
        self.sql += ";"

    def execute_sql(self, sql):
        # print sql
        data = self.db.select(sql)
        json_data = map(lambda result: dict(zip(self.attribute, result)), data)
        print json.dumps(json_data, default=self.json_serial)

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        print TypeError("Type %s not serializable" % type(obj))


class GetProbe(GetMethod):
    table = 'probe'
    dict_attribute = {
        'ipb': 'probe_id',
        'nom': 'probe_name',
        'iadr': 'ip_address',
        'madr': 'mac_address',
        'stat': 'status',
        'ud': 'last_update',
    }


class GetService(GetMethod):
    table = 'service'
    dict_attribute = {
        'isvc': 'service_id',
        'nsvc': 'service_name',
        'fn': 'file_name',
        'cmd': 'command'
    }

    def prepare_order(self):
        self.sql += " ORDER BY service_name"

class GetUser(GetMethod):
    table = 'user'
    dict_attribute = {
        'uid': 'username',
        'pswrd': 'password',
        'privil': 'role',
    }

    def prepare_condition(self):

        dict_condition = {
            'username': self.argument.getvalue("cond[uid]", None),
            'password': self.argument.getvalue("cond[pswrd]", None),
            'role': self.argument.getvalue("cond[privil]", None),
        }

        if dict_condition['username'] != None:
            self.sql  += ' WHERE ' + ' and '.join(map(lambda item: "`{key}`='{value}'".format(key=item, value=dict_condition[item]) if dict_condition[item] != None else "1=1", dict_condition))
        else:
            print "Please insert at least 1 condition"
            exit()

class GetDestination(GetMethod):
    table = 'destination'
    dict_attribute = {
        'idest': 'destination_id',
        'isvc': 'service_id',
        'ndest': 'destination',
        'pt': 'destination_port',
        'desc': 'description',
    }

    def prepare_condition(self):
        service_id = self.argument.getvalue("cond[isvc]", None)
        if service_id != None:
            self.sql += ' WHERE `service_id`={service_id}'.format(service_id=service_id)

class GetTestResult(GetMethod):
    table = 'test_result'
    dict_attribute = {
        'id': 'idr',
        'probe_id': 'ipb',
        'destination_id': 'idest',
        'timestamp': 'tm',
        'status': 'stat',
        'rrt': 'rrtr',
        'download': 'dl',
        'upload': 'ul'
    }

    def prepare_condition(self):
        probe_id = self.argument.getvalue("cond[ipb]", None)
        destination_id = self.argument.getvalue("cond[idest]", None)
        if probe_id != None and destination_id != None:
            self.sql += " WHERE `probe_id`='{probe_id}' and `destination_id`='{dest_id}'".format(probe_id=probe_id, dest_id=destination_id)


if __name__ == '__main__':
    print "Access-Control-Allow-Origin: *"
    print "Access-Control-Allow-Headers: X-HTTP-Method-Override"
    # print "Content-Type: text/html\n"
    print "Content-Type: application/json\n"
    environ = os.environ
    argument = cgi.FieldStorage()

    method_main = environ['REQUEST_METHOD'].lower()
    tlb = environ["REDIRECT_URL"].split('/')[2::][0]

    dict_tlb = {
        'pb': GetProbe,
        'svc': GetService,
        'persty': GetUser,
        'dest': GetDestination,
        'tesr': GetTestResult,


    }

    # print argument
    # result = argument.getvalue('select[]')
    # print result
    # print type(result)

    def do_it():
        if method_main == 'post':
            try:
                if environ['HTTP_X_HTTP_METHOD_OVERRIDE'].lower() == 'get':
                    example = dict_tlb[tlb](argument, environ)
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

    def tester():
        print sys.stdin.read()
        print "------------------------------------ <br>", argument, "<br>"
        print "------------------------------------ <br>", argument.list, "<br>"


        # result = argument.getvalue('condition[0]')
        # print "CONDITION: <br>", result, "<br>"


    do_it()
    # tester()