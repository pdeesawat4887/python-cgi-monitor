#!/usr/bin/python

import main.database as database
import os
import sys
import cgi
import re
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

class Method:
    def __init__(self, arg, environ):
        self.db = database.MySQLDatabase()
        self.sql = None
        self.attribute = None
        self.argument = arg
        self.environ = environ
        self.prepare_statement()
        self.execute_sql(self.sql)

    def prepare_statement(self):
        pass

    def execute_sql(self, sql):
        pass

    def log_error(self, e):
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        exit()

    def verify_ip(self, ip):
        ip_candidates = re.findall(r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                                   r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                                   r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
                                   r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip)

        if ip_candidates.__len__() != 0:
            return '.'.join(ip_candidates[0])
        else:
            return None

    def verify_text(self, text):
        return text if re.match("^[a-zA-Z0-9_-]*$", text) else None

    def verify_number(self, number):
        return number if re.match("^[0-9]*$", number) else None


class GetMethod(Method):

    def prepare_statement(self):
        # tlb = self.environ["REDIRECT_URL"].split('/')[2::][0]
        if self.argument.has_key('select[]'):
            self.attribute = self.argument.getvalue('select[]')
            if not isinstance(self.attribute, list):
                self.attribute = self.attribute.split(',')
            try:
                self.sql = "SELECT {select} FROM `{table}`".format(select=', '.join(map(lambda item: '{item}'.format(item=self.dict_attribute[item]), self.attribute)), table=self.table)
            except Exception as e:
                print "Incorrect attribute field"
                self.log_error(e)

        self.sql += " WHERE " + " and ".join(map(lambda item: "`{key}`='{value}'".format(key=self.dict_attribute[item], value=self.argument.getvalue('cond[{item}]'.format(item=item))) if self.argument.has_key('cond[{item}]'.format(item=item)) else '1=1', self.dict_attribute))
        self.sql += " ORDER BY " + ", ".join(map(lambda item: "`{attr}` {sort}".format(attr=self.dict_attribute[item], sort=self.argument.getvalue('order[{item}]'.format(item=item))) if self.argument.has_key('order[{item}]'.format(item=item)) else 'null', self.dict_attribute))

        if self.argument.has_key('limit[]'):
            try:
                self.sql += " LIMIT {limit};".format(limit=self.argument['limit[]'].value)
            except:
                self.sql += ";"

        # self.prepare_condition()
        # self.prepare_order()
        # self.prepare_limit()

    def prepare_condition(self):
        pass

    def prepare_order(self):
        pass

    def prepare_limit(self):
        self.sql += ";"

    def execute_sql(self, sql):
        print sql
        # data = self.db.select(sql)
        # json_data = map(lambda result: dict(zip(self.attribute, result)), data)
        # print json.dumps(json_data, default=self.json_serial)

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
            self.sql += ' WHERE ' + ' and '.join(map(
                lambda item: "`{key}`='{value}'".format(key=item, value=dict_condition[item]) if dict_condition[
                                                                                                     item] != None else "1=1",
                dict_condition))
        else:
            print "Missing require field username"
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
        'idr': 'result_id',
        'ipb': 'probe_id',
        'idest': 'destination_id',
        'tm': 'timestamp',
        'stat': 'status',
        'rttr': 'rtt',
        'dl': 'download',
        'ul': 'upload'
    }

    def prepare_condition(self):
        probe_id = self.argument.getvalue("cond[ipb]", None)
        destination_id = self.argument.getvalue("cond[idest]", None)
        if probe_id != None and destination_id != None:
            self.sql += " WHERE `probe_id`='{probe_id}' and `destination_id`='{dest_id}'".format(probe_id=probe_id,
                                                                                                 dest_id=destination_id)


class GetRunningService(GetMethod):
    table = 'running_service'
    dict_attribute = {
        'ipb': 'probe_id',
        'isvc': 'service_id',
        'rning_stat': 'running_status',
        'nsvc': '(select `service_name` from `service` where `running_service`.`service_id`=`service`.`service_id`) as nsvc',
    }

    def prepare_condition(self):
        ipb = self.argument.getvalue("cond[ipb]", None)
        if ipb != None:
            self.sql += " WHERE `probe_id`='{ipb}';".format(ipb=ipb)


class PostMethod(Method):

    def execute_sql(self, sql):
        try:
            self.db.insert(self.table, sql)
            self.execute_extend()
            print "Insert Successfully"
        except Exception as e:
            print "Failed Insert please check your data"
            self.log_error(e)

    def execute_extend(self):
        pass


class InsertDestination(PostMethod):
    table = 'destination'

    def prepare_statement(self):
        isvc = self.argument.getvalue('val[isvc]', None)
        ndest = self.argument.getvalue('val[ndest]', None)
        pt = self.argument.getvalue('val[pt]', 0)
        desc = self.argument.getvalue('val[desc]', None)
        self.sql = [(None, isvc, ndest, pt, desc)]


class InsertUser(PostMethod):
    table = 'user'

    def prepare_statement(self):
        uid = self.argument.getvalue('val[uid]', None)
        pswrd = self.argument.getvalue('val[pswrd]', None)
        privil = self.argument.getvalue('val[privil]', 'Guest')
        self.sql = [(uid, pswrd, None, privil)]


class InsertService(PostMethod):
    table = 'service'

    def prepare_statement(self):
        nsvc = self.argument.getvalue('val[nsvc]', 'default')
        fn = self.argument.getvalue('val[fn]', None)
        cmd = self.argument.getvalue('val[cmd]', None)
        self.sql = [(None, nsvc, fn, cmd)]

    def execute_extend(self):
        isvc = self.db.mycursor.lastrowid
        all_probe = self.db.select("SELECT probe_id FROM probe;")
        list_data = map(lambda item: (item[0], isvc, 1), all_probe)
        self.db.insert('running_service', list_data)
        print "<br> success extension"


class DeleteMethod(Method):

    def prepare_statement(self):
        self.sql = "DELETE FROM `{table}`".format(table=self.table)
        try:
            self.prepare_condition()
        except Exception as e:
            print "Incorrect require field"
            self.log_error(e)

    def prepare_condition(self):
        pass

    def execute_sql(self, sql):
        # print self.sql
        self.db.mycursor.execute(sql)
        self.db.connection.commit()
        print "<br> Delete Successfully"


class DeleteDestination(DeleteMethod):
    table = 'destination'

    def prepare_condition(self):
        idest = self.argument["del[idest]"].value
        ndest = self.argument["del[ndest]"].value

        self.sql += " WHERE `destination_id`='{idest}' and `destination`='{ndest}'".format(idest=idest, ndest=ndest)


class DeleteService(DeleteMethod):
    table = 'service'

    def prepare_condition(self):
        isvc = self.argument["del[isvc]"].value
        nsvc = self.argument["del[nsvc]"].value

        self.sql += " WHERE `service_id`='{isvc}' and `service_name`='{nsvc}'".format(isvc=isvc, nsvc=nsvc)


class DeleteUser(DeleteMethod):
    table = 'user'

    def prepare_condition(self):
        self.sql += " WHERE `username`='{username}'".format(username=self.argument["del[uid]"].value)


class DeleteProbe(DeleteMethod):
    table = 'probe'

    def prepare_condition(self):
        ipb = self.argument["del[ipb]"].value
        madr = self.argument["del[madr]"].value

        self.sql += " WHERE `probe_id`='{ipb}' and `mac_address`='{madr}'".format(ipb=ipb, madr=madr)


class PatchMethod(Method):

    def prepare_statement(self):
        self.sql = "UPDATE {table} SET ".format(table=self.table)
        try:
            self.prepare_value()
        except Exception as e:
            print "Incorrect some field update"
            self.log_error(e)
        try:
            self.prepare_condition()
        except Exception as e:
            print "Missing some require field"
            self.log_error(e)

    def prepare_value(self):
        if self.argument.has_key('key[]') and self.argument.has_key('value[]'):
            attribute = self.argument.getvalue('key[]')
            attribute_key = self.argument.getvalue('value[]')
            if not isinstance(attribute, list):
                attribute = attribute.split(',')
                attribute_key = attribute_key.split(',')
            self.sql += ', '.join(
                map(lambda key, value: "`{key}`='{value}'".format(key=self.dictionary[key], value=value), attribute,
                    attribute_key))

    def prepare_condition(self):
        pass

    def execute_sql(self, sql):
        # print self.sql
        self.db.mycursor.execute(sql)
        self.db.connection.commit()


class UpdateProbe(PatchMethod):
    dictionary = GetProbe.dict_attribute
    table = 'probe'

    def prepare_condition(self):
        ipb = self.argument["cond[ipb]"].value
        self.sql += " WHERE `probe_id`='{ipb}';".format(ipb=ipb)


class UpdateService(PatchMethod):
    dictionary = GetService.dict_attribute
    table = 'service'

    def prepare_condition(self):
        isvc = self.argument["cond[isvc]"].value
        self.sql += " WHERE `service_id`='{isvc}';".format(isvc=isvc)


class UpdateDestination(PatchMethod):
    dictionary = GetDestination.dict_attribute
    table = 'destination'

    def prepare_condition(self):
        idest = self.argument["cond[idest]"].value
        self.sql += " WHERE `destination_id`='{idest}';".format(idest=idest)


class UpdateRunning(PatchMethod):
    dictionary = GetRunningService.dict_attribute
    table = 'running_service'

    def prepare_condition(self):
        ipb = self.argument["cond[ipb]"].value
        isvc = self.argument["cond[isvc]"].value
        self.sql += " WHERE `probe_id`='{ipb}' and `service_id`='{isvc}';".format(ipb=ipb, isvc=isvc)


class UpdateUser(PatchMethod):
    dictionary = GetUser.dict_attribute
    table = 'user'

    def prepare_condition(self):
        uid = self.argument["cond[uid]"].value
        self.sql += " WHERE `username`='{uid}';".format(uid=uid)


if __name__ == '__main__':
    print "Access-Control-Allow-Origin: *"
    print "Access-Control-Allow-Headers: X-HTTP-Method-Override"
    # print "Content-Type: text/html\n"
    # print "Content-Type: application/json\n"
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
        'rning_svc': GetRunningService,
    }
    dict_tlb_post = {
        'dest': InsertDestination,
        'persty': InsertUser,
        'svc': InsertService,

    }
    dict_tlb_del = {
        'dest': DeleteDestination,
        'svc': DeleteService,
        'pb': DeleteProbe,
        'persty': DeleteUser,
    }
    dict_tlb_update = {
        'pb': UpdateProbe,
        'svc': UpdateService,
        'dest': UpdateDestination,
        'rning_svc': UpdateRunning,
        'persty': UpdateUser,

    }


    def do_it():
        try:
            check_override = environ['HTTP_X_HTTP_METHOD_OVERRIDE'].lower()
        except:
            check_override = None

        if method_main == 'post':
            if check_override == 'get':
                print "Content-Type: text/html\n"
                # print "Content-Type: application/json\n"
                example = dict_tlb[tlb](argument, environ)
            else:
                print "Content-Type: text/html\n"
                example = dict_tlb_post[tlb](argument, environ)
        elif method_main == 'patch':
            print "Content-Type: text/html\n"
            example = dict_tlb_update[tlb](argument, environ)
        elif method_main == 'delete':
            print "Content-Type: text/html\n"
            example = dict_tlb_del[tlb](argument, environ)


    def tester():
        print "Content-Type: text/html\n"
        print sys.stdin.read()
        print "------------------------------------ <br>", argument, "<br>"
        print "------------------------------------ <br>", argument.list, "<br>"
        # for i in range(len(argument.getvalue("key[]"))):
        #     print argument.getvalue("key[]")[i]
        #     print argument.getvalue("value[]")[i]

        print 'Hello -   ---------------------------------------------------------- <br><br>'

        dict_attribute = {
            'isvc': 'service_id',
            'nsvc': 'service_name',
            'fn': 'file_name',
            'cmd': 'command'
        }
        # list_result = map(lambda item: argument.has_key('cond['+item+']'), dict_attribute)

        # for i in argument.keys():
        #     print i

        # for x in dict_attribute:
        #     item = 'cond['+x+']'
        #     if argument.has_key('cond['+x+']'):
        #         # print argument.getvalue('cond[isvc]')
        #         print argument.getvalue('cond['+x+']')

        # verbs = " WHERE "
        # verbs += ' and '.join(map(lambda item: "`{key}`={value}".format(key=item, value=argument.getvalue(
        #     'cond[' + item + ']')) if argument.has_key('cond[' + item + ']') else '1=1', dict_attribute))
        # print verbs

        verbs = ""
        verbs += " ORDER BY " + ', '.join(map(lambda item: "`{attr}` {sort}".format(attr=dict_attribute[item], sort=argument.getvalue('order[{item}]'.format(item=item))) if argument.has_key('order[{xxx}]'.format(xxx=item)) else 'null', dict_attribute))
        print verbs
        # verbs += ", ".join(map(lambda item: , ))


    do_it()
    # tester()
