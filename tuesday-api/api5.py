#!/usr/bin/python

import main.database as database
import os
import sys
import cgi
import re
import json
from datetime import date, datetime
import decimal
from functools import partial


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

    def bad_request(self, response):
        self.output_flag = False
        print "Status: 400 Bad Request\r"
        print "Content-Type: text/html\n"
        print response
        exit()

    def log_error(self, e):
        self.output_flag = False
        print "Status: 400 Bad Request\r"
        print "Content-Type: text/html\n"
        print "Error on ", e
        exit()

    # def log_error(self, e):
    #     self.output_flag = False
    #     print "Status: 400 Bad Request\r"
    #     print "Content-Type: text/html\n"
    #
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #
    #     print 'Error on line {}<br>{}<br>{}<br><br>{}<br>{}<br>{}'.format(sys.exc_info()[-1].tb_lineno, type(e).__name__, e, exc_type, fname, exc_tb.tb_lineno)
    #
    #     exit()

    def error_insert(self, status=400, explain='Bad Request', word=None, attr=None):
        self.output_flag = False
        print "Status: {status} {explain}\r".format(status=status, explain=explain)
        print "Content-Type: text/html\n"
        print "{word}: Error {attr}".format(word=word, attr=attr, ty=type)
        exit()

    def ipFormatChk(self, ip_str):
        if len(ip_str.split()) == 1:
            ipList = ip_str.split('.')
            if len(ipList) == 4:
                for i, item in enumerate(ipList):
                    try:
                        ipList[i] = int(item)
                    except Exception as e:
                        self.log_error(e)
                    if not isinstance(ipList[i], int):
                        return None
                if max(ipList) < 256:
                    return ip_str
                else:
                    return None
            else:
                return None
        else:
            return None

    def verify_text(self, text):
        try:
            return text if re.match("^[a-zA-Z0-9_-]*$", text) else None
        except Exception as e:
            self.log_error(e)

    def verify_number(self, number):
        try:
            return number if re.match("^[0-9]*$", number) else None
        except Exception as e:
            self.log_error(e)

    def verify_unique(self, table, column, value):
        if value == None:
            self.bad_request('cannot found {col} value.'.format(col=column))

        val = int(self.db.select("SELECT count(`{column}`) FROM {table} WHERE `{column}`={value};".format(column=column, table=table, value=value))[0][0])

        if val > 0:
            self.bad_request('Duplicate key')
        else:
            return value

    def verify_input(self, length, restrict, value, attribute):

        format_reg = {
            'limit': length,
            'restrict': restrict
        }
        if int(length) == 1:
            length = 8
        if value == False:
            return self.error_insert(word="Missing Require Field", attr=attribute)
        elif value == None or value == '':
            return None
        else:
            value = str(value)
            return self.error_insert(attr=attribute, word="Max Length") if len(value) > int(length) else value if re.match("^{restrict}{{0,{limit}}}$".format(**format_reg), value) else self.error_insert(attr=attribute, word="Incorrect format")

    # @staticmethod
    def verify_update(self, length, restrict, attribute, value=None):
        format_reg = {
            'limit': length,
            'restrict': restrict
        }
        value = str(value)

        if int(length) == 1:
            length = 8
        return self.error_insert(attr=attribute, word="Max Length") if len(value) > int(
            length) else value if re.match("^{restrict}{{0,{limit}}}$".format(**format_reg),
                                           value) else self.error_insert(attr=attribute, word="Incorrect format")

    # def error_update(self, status=400, explain='Bad Request', word=None, attr=None):
    #     self.output_flag = False
    #     print "Status: {status} {explain}\r".format(status=status, explain=explain)
    #     print "Content-Type: text/html\n"
    #     print "{word}: Error {attr}".format(word=word, attr=attr, ty=type)
    #     exit()

class GetMethod(Method):

    def prepare_statement(self):
        if self.argument.has_key('select[]'):
            self.attribute = self.argument.getvalue('select[]')
            if not isinstance(self.attribute, list):
                self.attribute = self.attribute.split(',')
            try:
                self.sql = "SELECT {select} FROM `{table}`".format(select=', '.join(map(lambda item: '{item}'.format(item=self.dict_attribute[item]), self.attribute)), table=self.table)
            except Exception as e:
                self.log_error(e)

        self.sql += " WHERE " + " and ".join(map(lambda item: "`{key}`='{value}'".format(key=self.dict_attribute[item], value=self.argument.getvalue('cond[{item}]'.format(item=item))) if self.argument.has_key('cond[{item}]'.format(item=item)) else '1=1', self.dict_attribute))
        self.sql += " ORDER BY " + ", ".join(map(lambda item: "`{attr}` {sort}".format(attr=self.dict_attribute[item], sort=self.argument.getvalue('order[{item}]'.format(item=item))) if self.argument.has_key('order[{item}]'.format(item=item)) else 'null', self.dict_attribute))

        if self.argument.has_key('limit[]'):
            try:
                self.sql += " LIMIT {limit};".format(limit=self.argument['limit[]'].value)
            except:
                self.sql += ";"

    def execute_sql(self, sql):
        # print sql
        data = self.db.select(sql)
        json_data = map(lambda result: dict(zip(self.attribute, result)), data)
        self.output_type = 'json'
        self.output_flag = True
        self.output = json.dumps(json_data, default=self.json_serial)

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        # print TypeError("Type %s not serializable" % type(obj))


class GetProbe(GetMethod):
    table = 'PROBES'
    dict_attribute = {
        'ipb': 'probe_id',
        'pb_nom': 'probe_name',
        'ipadr': 'ip_address',
        'madr': 'mac_address',
        'pb_stat': 'probe_status',
        'last_ud': 'last_updated',
        'd_add': 'date_added',
        'icoll': 'collection_id',
    }


class GetService(GetMethod):
    table = 'SERVICES'
    dict_attribute = {
        'isvc': 'service_id',
        'nsvc': 'service_name',
        'trans_prot': 'transport_protocol',
        'f_cmd': 'file_command',
        'fn': 'file_name',
        'u_cmd': 'udp_command',
        'svc_desc': 'service_description',
        'svc_dest_ex': 'destination_example'
    }


class GetUser(GetMethod):
    table = 'USERS'
    dict_attribute = {
        'uid': 'id',
        'user': 'username',
        'privil': 'role',
    }


class GetDestination(GetMethod):
    table = 'DESTINATIONS'
    dict_attribute = {
        'idest': 'destination_id',
        'isvc': 'service_id',
        'ndest': 'destination_name',
        'ptdest': 'destination_port',
        'dest_desc': 'destination_description',
    }


class GetTestResult(GetMethod):
    table = 'TESTRESULTS'
    dict_attribute = {
        'itst': 'result_id',
        'icoll': 'collection_id',
        'isvc': 'service_id',
        'strt': 'start_date',
        'idest': 'destination_id',
        'stat_tst': 'result_status',
        'rtt': 'round_trip_time',
        'dl': 'download',
        'ul': 'upload',
        'oth': 'other',
        'oth_desc': 'other_description',
        'oth_un': 'other_unit',
        'ndest': "(select `destination_name` from `DESTINATIONS` where `TESTRESULTS`.`destination_id`=`DESTINATIONS`.`destination_id`) as ndest",
        'ptdest': "(select `destination_port` from `DESTINATIONS` where `TESTRESULTS`.`destination_id`=`DESTINATIONS`.`destination_id`) as ptdest",
        'desc_dest': "(select `destination_description` from `DESTINATIONS` where `TESTRESULTS`.`destination_id`=`DESTINATIONS`.`destination_id`) as desc_dest",
        'nsvc': "(select `service_name` from `SERVICES` where `TESTRESULTS`.`service_id`=`SERVICES`.`service_id`) as nsvc",
        'trans_prot': "(select `transport_protocol` from `SERVICES` where `TESTRESULTS`.`service_id`=`SERVICES`.`service_id`) as trans_prot",
        'svc_desc': "(select `service_description` from `SERVICES` where `TESTRESULTS`.`service_id`=`SERVICES`.`service_id`) as svc_desc",
    }


class GetRunningService(GetMethod):
    table = 'RUNNING_SERVICES'
    dict_attribute = {
        'icoll': 'collection_id',
        'isvc': 'service_id',
        'rning_svc_stat': 'running_svc_status',
        'nsvc': "(select `service_name` from `SERVICES` where `RUNNING_SERVICES`.`service_id`=`SERVICES`.`service_id`) as nsvc",
        'trans_prot': "(select `transport_protocol` from `SERVICES` where `RUNNING_SERVICES`.`service_id`=`SERVICES`.`service_id`) as trans_prot",
        'f_cmd': "(select `file_command` from `SERVICES` where `RUNNING_SERVICES`.`service_id`=`SERVICES`.`service_id`) as f_cmd",
        'fn': "(select `file_name` from `SERVICES` where `RUNNING_SERVICES`.`service_id`=`SERVICES`.`service_id`) as fn",
        'u_cmd': "(select `udp_command` from `SERVICES` where `RUNNING_SERVICES`.`service_id`=`SERVICES`.`service_id`) as u_cmd",
        'svc_desc': "(select `service_description` from `SERVICES` where `RUNNING_SERVICES`.`service_id`=`SERVICES`.`service_id`) as svc_desc",
        'svc_dest_ex': "(select `destination_example` from `SERVICES` where `RUNNING_SERVICES`.`service_id`=`SERVICES`.`service_id`) as svc_dest_ex"
    }


class GetRunningDestination(GetMethod):
    table = 'RUNNING_DESTINATIONS'
    dict_attribute = {
        'icoll': 'collection_id',
        'idest': 'destination_id',
        'rning_dest_stat': 'running_dest_status',
        'ndest': '(select `destination_name` from `DESTINATIONS` where `RUNNING_DESTINATIONS`.`destination_id`=`DESTINATIONS`.`destination_id`) as ndest',
        'ptdest': "(select `destination_port` from `DESTINATIONS` where `RUNNING_DESTINATIONS`.`destination_id`=`DESTINATIONS`.`destination_id`) as ptdest",
        'desc_dest': "(select `destination_description` from `DESTINATIONS` where `RUNNING_DESTINATIONS`.`destination_id`=`DESTINATIONS`.`destination_id`) as desc_dest",
        'isvc': "(select `service_id` from `DESTINATIONS` where `RUNNING_DESTINATIONS`.`destination_id`=`DESTINATIONS`.`destination_id`) as isvc",
        'nsvc': "(select `service_name` from `SERVICES` where `SERVICES`.`service_id`=(select `service_id` from `DESTINATIONS` where `RUNNING_DESTINATIONS`.`destination_id`=`DESTINATIONS`.`destination_id`)) as nsvc"
    }


class PostMethod(Method):

    def execute_sql(self, sql):
        try:
            self.db.insert(self.table, sql)
            self.execute_extend()
            self.output_type = 'plain'
            self.output_flag = True
            self.output = "Insert {table} Successfully".format(table=self.table)
            # print "Insert Successfully"
        except Exception as e:
            self.log_error(e)

    def execute_extend(self):
        pass


class InsertDestination(PostMethod):
    table = 'DESTINATIONS'

    def prepare_statement(self):

        isvc = self.verify_input(length=11, restrict='[0-9]', attribute='service id', value=self.argument.getvalue('val[isvc]', False))
        ndest = self.verify_input(length=248, restrict='[a-zA-Z0-9\_\-\.\:\?\=\/]', attribute='destination name',value=self.argument.getvalue('val[ndest]', False))
        ptdest = self.verify_input(length=5, restrict='[0-9]', attribute='destination port',value=self.argument.getvalue('val[ptdest]', False))
        dest_desc = self.verify_input(length=2083, restrict='[a-zA-Z0-9\s~!@#$%^&?*()+`={}|\[\];\':.\\\/]', attribute='destination description', value=self.argument.getvalue('val[dest_desc]', None))
        self.sql = [(None, isvc, ndest, ptdest, dest_desc)]

        # isvc = self.verify_number(self.argument.getvalue('val[isvc]', None))
        # ndest = self.verify_text(self.argument.getvalue('val[ndest]'))
        # ptdest = self.verify_number(self.argument.getvalue('val[ptdest]', 0))
        # dest_desc = self.argument.getvalue('val[dest_desc]', None)
        # self.sql = [(None, isvc, ndest, ptdest, dest_desc)]

        ### insert every collection_id execute_extend()
    def execute_extend(self):
        idest = self.db.mycursor.lastrowid
        all_collection_id = self.db.select("SELECT DISTINCT(`collection_id`) FROM `PROBES`;")
        list_data = map(lambda item: (item[0], idest, 'Active'), all_collection_id)
        self.db.insert('RUNNING_DESTINATIONS', list_data)


class InsertUser(PostMethod):
    table = 'user'

    def prepare_statement(self):
        uid = self.argument.getvalue('val[uid]', None)
        pswrd = self.argument.getvalue('val[pswrd]', None)
        privil = self.argument.getvalue('val[privil]', 'Guest')
        self.sql = [(uid, pswrd, None, privil)]


class InsertService(PostMethod):
    table = 'SERVICES'

    def prepare_statement(self):

        often_pattern = "[a-zA-Z0-9\s~!@#$%^&?*()+`={}|\[\];':.\\\/]"

        nsvc = self.verify_input(length=32, restrict='[a-zA-Z0-9\_\-]', attribute='service name', value=self.argument.getvalue('val[nsvc]', False))
        trans_prot = self.verify_input(length=1, restrict='(?:tcp|udp|other|1|2|3)', attribute='transport protocol', value=self.argument.getvalue('val[trans_prot]', False))
        f_cmd = self.verify_input(length=256, restrict=often_pattern, attribute='file command', value=self.argument.getvalue('val[f_cmd]', None))
        fn = self.verify_input(length=64, restrict='[a-zA-Z0-9\.\-\_]', attribute='file command', value=self.argument.getvalue('val[fn]', None))
        u_cmd = self.verify_input(length=2083, restrict=often_pattern, attribute='udp message', value=self.argument.getvalue('val[u_cmd]', None))
        svc_desc = self.verify_input(length=2083, restrict=often_pattern, attribute='service description', value=self.argument.getvalue('val[svc_desc]', None))
        svc_dest_ex = self.verify_input(length=2083, restrict=often_pattern, attribute='destination example', value=self.argument.getvalue('val[svc_dest_ex]', False))
        self.sql = [(None, nsvc, trans_prot, f_cmd, fn, u_cmd, svc_desc, svc_dest_ex)]


    ## insert every collection_id execute_extend()
    def execute_extend(self):
        isvc = self.db.mycursor.lastrowid
        all_collection_id = self.db.select("SELECT DISTINCT(`collection_id`) FROM `PROBES`;")
        list_data = map(lambda item: (item[0], isvc, 'Active'), all_collection_id)
        self.db.insert('RUNNING_SERVICES', list_data)


class DeleteMethod(Method):

    def prepare_statement(self):
        self.sql = "DELETE FROM `{table}`".format(table=self.table)
        try:
            self.prepare_condition()
        except Exception as e:
            self.log_error(e)

    def prepare_condition(self):
        pass

    def execute_sql(self, sql):
        # print self.sql
        self.db.mycursor.execute(sql)
        self.db.connection.commit()


class DeleteDestination(DeleteMethod):
    table = 'DESTINATIONS'

    def prepare_condition(self):
        idest = self.verify_input(length=11, restrict='[0-9]', attribute='destination id', value=self.argument.getvalue('del[idest]', False))
        self.sql += " WHERE `destination_id`='{idest}';".format(idest=idest)


class DeleteService(DeleteMethod):
    table = 'SERVICES'

    def prepare_condition(self):
        isvc = self.verify_input(length=11, restrict='[0-9]', attribute='service id', value=self.argument.getvalue('del[isvc]', False))
        self.sql += " WHERE `service_id`='{isvc}';".format(isvc=isvc)


class DeleteProbe(DeleteMethod):
    table = 'PROBES'

    def prepare_condition(self):
        ipb = self.verify_input(length=11, restrict='[0-9]', attribute='probe id', value=self.argument.getvalue('del[ipb]', False))
        self.sql += " WHERE `probe_id`='{ipb}';".format(ipb=ipb)


class DeleteUser(DeleteMethod):
    table = 'user'

    def prepare_condition(self):
        self.sql += " WHERE `username`='{username}'".format(username=self.argument["del[uid]"].value)


class PatchMethod(Method):

    def prepare_statement(self):
        self.sql = "UPDATE `{table}` SET ".format(table=self.table)
        try:
            self.prepare_value()
        except Exception as e:
            self.log_error(e)
        try:
            self.prepare_condition()
        except Exception as e:
            self.log_error(e)

    def prepare_value(self):
        if self.argument.has_key('key[]') and self.argument.has_key('value[]'):
            attribute = self.argument.getvalue('key[]')
            attribute_key = self.argument.getvalue('value[]')
            if not isinstance(attribute, list):
                attribute = attribute.split(',')
                attribute_key = attribute_key.split(',')
            # self.sql += ', '.join(map(lambda key, value: "`{key}`='{value}'".format(key=self.dictionary[key], value=value), attribute, attribute_key))
            self.sql += ', '.join(map(lambda key, value: "`{key}`='{value}'".format(key=self.dictionary[key], value=self.option[key](value=value)), attribute, attribute_key))


    def prepare_condition(self):
        pass

    def execute_sql(self, sql):
        self.output_type = 'plain'
        self.output_flag = True
        self.output = self.sql
        # print self.sql
        # self.db.mycursor.execute(sql)
        # self.db.connection.commit()

# length, restrict, attribute, value=None
class UpdateProbe(PatchMethod):
    dictionary = GetProbe.dict_attribute
    table = 'PROBES'
    temp = Method(None, None)
    option = {
        'pb_nom': partial(temp.verify_update, 32, '[a-zA-Z0-9-_.\s]', 'probe name'),
        'madr': partial(temp.verify_update, 32, "(?:[0-9a-fA-F]:?)", 'mac address'),
        'icoll': partial(temp.verify_update, 248, "[a-zA-Z0-9-_.]", 'collection id'),
        'ipadr': partial(temp.verify_update, 32, "[a-zA-Z0-9-_.]", 'ip address'),
        'pb_stat': partial(temp.verify_update, 1, "(?:Active|Deactive|Idle|1|2|3)", 'probe status'),
    }

    def prepare_condition(self):
        ipb = self.argument["cond[ipb]"].value
        self.sql += " WHERE `probe_id`='{ipb}';".format(ipb=ipb)


class UpdateService(PatchMethod):
    dictionary = GetService.dict_attribute
    table = 'SERVICES'
    temp = Method(None, None)
    often_pattern = "[a-zA-Z0-9\s~!@#$%^&?*()+`={}|\[\];':.\\\/]"
    option = {
        'nsvc': partial(temp.verify_update, 32, '[a-zA-Z0-9\_\-]', 'service name'),
        'trans_prot': partial(temp.verify_update, 1, '(?:tcp|udp|other|1|2|3)', 'transport_protocol'),
        'f_cmd': partial(temp.verify_update, 256, often_pattern, 'file_command'),
        'fn': partial(temp.verify_update, 64, '[a-zA-Z0-9\_\-]', 'file_name'),
        'u_cmd': partial(temp.verify_update, 2083, often_pattern, 'udp_command'),
        'svc_desc': partial(temp.verify_update, 2083, often_pattern, 'service_description'),
        'svc_dest_ex': partial(temp.verify_update, 2083, often_pattern, 'destination_example'),
    }

    def prepare_condition(self):
        isvc = self.argument["cond[isvc]"].value
        self.sql += " WHERE `service_id`='{isvc}';".format(isvc=isvc)


class UpdateDestination(PatchMethod):
    dictionary = GetDestination.dict_attribute
    table = 'DESTINATIONS'
    temp = Method(None, None)
    option = {
        'isvc': partial(temp.verify_update, 11, '[0-9]', 'service_id'),
        'ndest': partial(temp.verify_update, 248, '[a-zA-Z0-9\_\-\.\:\?\=\/]', 'destination_name'),
        'ptdest': partial(temp.verify_update, 5, '[0-9]', 'destination_port'),
        'dest_desc': partial(temp.verify_update, 2083, '[a-zA-Z0-9\s~!@#$%^&?*()+`={}|\[\];\':.\\\/]', 'destination_description'),
    }

    def prepare_condition(self):
        idest = self.argument["cond[idest]"].value
        self.sql += " WHERE `destination_id`='{idest}';".format(idest=idest)


class UpdateRunningService(PatchMethod):
    dictionary = GetRunningService.dict_attribute
    table = 'RUNNING_SERVICES'
    temp = Method(None, None)
    option = {
        'rning_svc_stat': partial(temp.verify_update, 1, '(?:Active|Deactive|1|2)', 'running service status')
    }

    def prepare_condition(self):
        icoll = self.argument["cond[icoll]"].value
        isvc = self.argument["cond[isvc]"].value
        self.sql += " WHERE `collection_id`='{icoll}' and `service_id`='{isvc}';".format(icoll=icoll, isvc=isvc)

class UpdateRunningDestination(PatchMethod):
    dictionary = GetRunningDestination.dict_attribute
    table = 'RUNNING_DESTINATIONS'
    temp = Method(None, None)
    option = {
        'rning_dest_stat': partial(temp.verify_update, 1, '(?:Active|Deactive|1|2)', 'running destination status')
    }

    def prepare_condition(self):
        icoll = self.argument["cond[icoll]"].value
        idest = self.argument["cond[idest]"].value
        self.sql += " WHERE `collection_id`='{icoll}' and `destination_id`='{idest}';".format(icoll=icoll, idest=idest)


class UpdateUser(PatchMethod):
    dictionary = GetUser.dict_attribute
    table = 'user'

    def prepare_condition(self):
        uid = self.argument["cond[uid]"].value
        self.sql += " WHERE `username`='{uid}';".format(uid=uid)


if __name__ == '__main__':
    # print('Status: HTTP/1.0 404 Not Found\r\n')
    # print('Content-Type: text/html\r\n\r\n')
    # print('<html><head></head><body><h1>404 Not Found</h1></body></html>')

    print "Access-Control-Allow-Origin: *"
    print "Access-Control-Allow-Headers: X-HTTP-Method-Override"

    # print "Status: 200 OK\r\n"
    # print "Content-Type: text/html\r\n\r\n"

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
        'tst': GetTestResult,
        'rning_svc': GetRunningService,
        'rning_dest': GetRunningDestination,
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
        'rning_svc': UpdateRunningService,
        'rning_dest': UpdateRunningDestination,
        'persty': UpdateUser,

    }

    def do_it():
        try:
            check_override = environ['HTTP_X_HTTP_METHOD_OVERRIDE'].lower()
        except:
            check_override = None

        if method_main == 'post':
            if check_override == 'get':
                example = dict_tlb[tlb](argument, environ)
            else:
                example = dict_tlb_post[tlb](argument, environ)
        elif method_main == 'patch':
            example = dict_tlb_update[tlb](argument, environ)
        elif method_main == 'delete':
            example = dict_tlb_del[tlb](argument, environ)

        try:
            if example.output_flag:
                print "Status: 200 OK\r"
                if example.output_type == 'json':
                    print "Content-Type: application/json\n"
                elif example.output_type == 'plain':
                    print "Content-Type: text/html\n"
                print example.output
        except:
            print "Status: 400 Bad Request\r\n"
            print "Content-Type: text/html\r\n\r\n"

    # def do_it():
    #     #     try:
    #     #         check_override = environ['HTTP_X_HTTP_METHOD_OVERRIDE'].lower()
    #     #     except:
    #     #         check_override = None
    #     #
    #     #     if method_main == 'post':
    #     #         if check_override == 'get':
    #     #             # print "Content-Type: text/html\n"
    #     #             print "Content-Type: application/json\n"
    #     #             example = dict_tlb[tlb](argument, environ)
    #     #         else:
    #     #             print "Content-Type: text/html\n"
    #     #             example = dict_tlb_post[tlb](argument, environ)
    #     #     elif method_main == 'patch':
    #     #         print "Content-Type: text/html\n"
    #     #         example = dict_tlb_update[tlb](argument, environ)
    #     #     elif method_main == 'delete':
    #     #         print "Content-Type: text/html\n"
    #     #         example = dict_tlb_del[tlb](argument, environ)


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
        verbs += " ORDER BY " + ', '.join(map(lambda item: "`{attr}` {sort}".format(attr=dict_attribute[item],
                                                                                    sort=argument.getvalue(
                                                                                        'order[{item}]'.format(
                                                                                            item=item))) if argument.has_key(
            'order[{xxx}]'.format(xxx=item)) else 'null', dict_attribute))
        print verbs
        # verbs += ", ".join(map(lambda item: , ))


    do_it()
    # tester()
