#!/usr/bin/python

import main.database as database
import main.jwt_server as token
import os
import sys
import cgi
import re
import json
from datetime import date, datetime
import decimal
from functools import partial

class Method:
    def __init__(self, arg, environ):
        self.db = database.MySQLDatabase()
        self.sql = None
        self.attribute = None
        self.argument = arg
        self.environ = environ
        self.prepare_statement()
        try:
            self.execute_sql(self.sql)
        except Exception as e:
            self.log_error(e)

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

    def error_insert(self, status=400, explain='Bad Request', word=None, attr=None):
        self.output_flag = False
        print "Status: {status} {explain}\r".format(status=status, explain=explain)
        print "Content-Type: text/html\n"
        print "{word}: Error {attr}".format(word=word, attr=attr)
        exit()

    def error_update(self, status=400, explain='Bad Request', word=None):
        self.output_flag = False
        print "Status: {status} {explain}\r".format(status=status, explain=explain)
        print "Content-Type: text/html\n"
        print "Error: {word}".format(word=word)
        exit()

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

    def verify_input(self, length, restrict, value, attribute, unique=False):
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
            if unique:
                val = int(self.db.select("SELECT count(`{column}`) FROM {table} WHERE `{column}`='{value}';".format(column=attribute, table=self.table, value=value))[0][0])
                if val > 0:
                    return self.error_insert(word="Duplicate Unique key", attr=attribute)
                else:
                    return self.error_insert(attr=attribute, word="Max Length") if len(value) > int(length) else value if re.match("^{restrict}{{0,{limit}}}$".format(**format_reg), value) else self.error_insert(attr=attribute, word="Incorrect format")
            else:
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
        return self.error_insert(attr=attribute, word="Max Length") if len(value) > int(length) else value if re.match("^{restrict}{{0,{limit}}}$".format(**format_reg), value) else self.error_insert(attr=attribute, word="Incorrect format")

    def logging_statement(self, type=None, table=None, sql=None, user=None, **kwargs):
        id = self.db.mycursor.lastrowid
        mapping = {
            'PROBES': ('probe_name', 'probe_id'),
            'SERVICES': ('service_name', 'service_id'),
            'DESTINATIONS': ('destination_name', 'destination_id'),
            'RUNNING_SERVICES': ('distinct(select service_name from SERVICES where RUNNING_SERVICES.service_id=SERVICES.service_id)', 'id'),
            'RUNNING_DESTINATIONS': ('distinct(select destination_name from DESTINATIONS where RUNNING_DESTINATIONS.destination_id=DESTINATIONS.destination_id)', 'id'),
        }
        word = self.db.select("SELECT {select} FROM {table} WHERE {cond}='{val}';".format(
            select=mapping[table][0], table=table, cond=mapping[table][1], val=id))[0][0]

        sql_insert = 'INSERT INTO `LOGGING_EVENTS` VALUES ("Null", "{user}", "{ty}", "{tlb}", "{word}", "{sql}", NOW())'.format(
            user=self.argument.getvalue('log[user]', user), ty=type, tlb=table, word=word, sql=sql)
        self.db.mycursor.execute(sql_insert)
        self.db.connection.commit()


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
        'iclus': 'cluster_id',
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
        'n_svc': 'no_svc',
        'iclus': 'cluster_id',
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
        'n_dest': 'n_dest',
        'iclus': 'cluster_id',
        'idest': 'destination_id',
        'rning_dest_stat': 'running_dest_status',
        'ndest': '(select `destination_name` from `DESTINATIONS` where `RUNNING_DESTINATIONS`.`destination_id`=`DESTINATIONS`.`destination_id`) as ndest',
        'ptdest': "(select `destination_port` from `DESTINATIONS` where `RUNNING_DESTINATIONS`.`destination_id`=`DESTINATIONS`.`destination_id`) as ptdest",
        'desc_dest': "(select `destination_description` from `DESTINATIONS` where `RUNNING_DESTINATIONS`.`destination_id`=`DESTINATIONS`.`destination_id`) as desc_dest",
        'isvc': "(select `service_id` from `DESTINATIONS` where `RUNNING_DESTINATIONS`.`destination_id`=`DESTINATIONS`.`destination_id`) as isvc",
        'nsvc': "(select `service_name` from `SERVICES` where `SERVICES`.`service_id`=(select `service_id` from `DESTINATIONS` where `RUNNING_DESTINATIONS`.`destination_id`=`DESTINATIONS`.`destination_id`)) as nsvc"
    }

class GetCluster(GetMethod):
    table = 'CLUSTERS'
    dict_attribute = {
        'iclus': 'cluster_id',
        'ipb': 'probe_id',
        'clus_desc': 'cluster_description',
        'pb_nom': '(SELECT `probe_name` FROM PROBES WHERE CLUSTERS.probe_id=PROBES.probe_id) as pb_nom',
        'ipadr': '(SELECT `ip_address` FROM PROBES WHERE CLUSTERS.probe_id=PROBES.probe_id) as ipadr',
        'madr': '(SELECT `mac_address` FROM PROBES WHERE CLUSTERS.probe_id=PROBES.probe_id) as imadr',
        'pb_stat': '(SELECT `probe_status` FROM PROBES WHERE CLUSTERS.probe_id=PROBES.probe_id) as pb_stat',
        'last_ud': '(SELECT `last_updated` FROM PROBES WHERE CLUSTERS.probe_id=PROBES.probe_id) as last_ud',
        'd_add': '(SELECT `date_added` FROM PROBES WHERE CLUSTERS.probe_id=PROBES.probe_id) as d_add',
    }


class PostMethod(Method):

    def execute_sql(self, sql):
        try:
            self.db.execute_insert(self.table, sql)
            # self.logging_statement()
            self.execute_extend()
            self.db.connection.commit()

            self.output_type = 'plain'
            self.output_flag = True
            self.output = "Insert {table} Successfully".format(table=self.table)
        except Exception as e:
            self.log_error(e)

    def execute_extend(self):
        pass


class InsertDestination(PostMethod):
    table = 'DESTINATIONS'

    def prepare_statement(self):

        isvc = self.verify_input(length=11, restrict='[0-9]', attribute='service_id', value=self.argument.getvalue('val[isvc]', False))
        ndest = self.verify_input(length=248, restrict='[a-zA-Z0-9\_\-\.\:\?\=\/]', attribute='destination_name',value=self.argument.getvalue('val[ndest]', False))
        ptdest = self.verify_input(length=5, restrict='[0-9]', attribute='destination_port',value=self.argument.getvalue('val[ptdest]', False))
        dest_desc = self.verify_input(length=2083, restrict='[a-zA-Z0-9\s~!@#$%^&?*()+`={}|\[\];\':.\\\/-_]', attribute='destination_description', value=self.argument.getvalue('val[dest_desc]', None))
        self.sql = [(None, isvc, ndest, ptdest, dest_desc)]

    def execute_extend(self):
        idest = self.db.mycursor.lastrowid
        all_cluster_id = self.db.select("SELECT DISTINCT(`cluster_id`) FROM `CLUSTERS`;")
        if len(all_cluster_id) != 0:
            list_data = map(lambda item: (None, item[0], idest, 'Active'), all_cluster_id)
            self.db.execute_insert('RUNNING_DESTINATIONS', list_data)


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

        often_pattern = "[a-zA-Z0-9\s~!@#$%^&?*()+`={}|\[\];':.\\\/_-]"
        nsvc = self.verify_input(length=32, restrict='[a-zA-Z0-9\_\-]', attribute='service_name', value=self.argument.getvalue('val[nsvc]', False), unique=True)
        trans_prot = self.verify_input(length=1, restrict='(?:tcp|udp|other|1|2|3)', attribute='transport_protocol', value=self.argument.getvalue('val[trans_prot]', False))
        f_cmd = self.verify_input(length=256, restrict=often_pattern, attribute='file_command', value=self.argument.getvalue('val[f_cmd]', None))
        fn = self.verify_input(length=64, restrict='[a-zA-Z0-9\.\-\_]', attribute='file_name', value=self.argument.getvalue('val[fn]', None), unique=True)
        u_cmd = self.verify_input(length=2083, restrict=often_pattern, attribute='udp_message', value=self.argument.getvalue('val[u_cmd]', None))
        svc_desc = self.verify_input(length=2083, restrict=often_pattern, attribute='service_description', value=self.argument.getvalue('val[svc_desc]', None))
        svc_dest_ex = self.verify_input(length=2083, restrict=often_pattern, attribute='destination_example', value=self.argument.getvalue('val[svc_dest_ex]', False))
        self.sql = [(None, nsvc, trans_prot, f_cmd, fn, u_cmd, svc_desc, svc_dest_ex)]

    def execute_extend(self):
        isvc = self.db.mycursor.lastrowid
        all_cluster_id = self.db.select("SELECT DISTINCT(`cluster_id`) FROM `CLUSTERS`;")
        if len(all_cluster_id) != 0:
            list_data = map(lambda item: (None, item[0], isvc, 'Active'), all_cluster_id)
            self.db.execute_insert('RUNNING_SERVICES', list_data)

class InsertCluster(PostMethod):
    table = 'CLUSTERS'

    def prepare_statement(self):
        iclus = self.verify_input(length=11, restrict='[0-9]', attribute='cluster_id', value=self.argument.getvalue('val[iclus]', None))
        ipb = self.verify_input(length=32, restrict='[a-zA-Z0-9]', attribute='probe_id', value=self.argument.getvalue('val[ipb]', None))
        clus_desc = self.verify_input(length=2083, restrict='[a-zA-Z0-9\s~!@#$%^&?*()+`={}|\[\];\':.\\\/-_]', attribute='cluster description', value=self.argument.getvalue('val[clus_desc]', None))
        self.sql = [(iclus, ipb, clus_desc)]

    def execute_extend(self):
        cluster_id = self.db.mycursor.lastrowid
        all_isvc = self.db.select("SELECT DISTINCT(`service_id`) FROM `SERVICES`;")
        if len(all_isvc) != 0:
            list_data_svc = map(lambda item: (None, cluster_id, item[0], 'Active'), all_isvc)
            self.db.execute_insert('RUNNING_SERVICES', list_data_svc)
        all_idest = self.db.select("SELECT DISTINCT(`destination_id`) FROM `DESTINATIONS`;")
        if len(all_idest) != 0:
            list_data_dest = map(lambda item: (None, cluster_id, item[0], 'Active'), all_idest)
            self.db.execute_insert('RUNNING_DESTINATIONS', list_data_dest)


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
        if self.table == 'PROBES':
            self.db.foreign_key_func(func='disable')
        self.db.mycursor.execute(sql)
        self.db.foreign_key_func(func='enable')
        self.db.connection.commit()
        self.output_type = 'plain'
        self.output_flag = True
        self.output = "Delete row in {table} Successfully".format(table=self.table)


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
        ipb = self.verify_input(length=32, restrict='[a-zA-Z0-9]', attribute='probe id', value=self.argument.getvalue('del[ipb]', False))
        self.sql += " WHERE `probe_id`='{ipb}';".format(ipb=ipb)

class DeleteCluster(DeleteMethod):
    table = 'CLUSTERS'

    def prepare_condition(self):
        iclus = self.verify_input(length=11, restrict='[0-9]', attribute='cluster id', value=self.argument.getvalue('del[iclus]', False))
        self.sql += " WHERE `cluster_id`='{iclus}';".format(iclus=iclus)


class DeleteUser(DeleteMethod):
    table = 'user'

    def prepare_condition(self):
        self.sql += " WHERE `username`='{username}'".format(username=self.argument["del[uid]"].value)


class PatchMethod(Method):

    def checker(self, key, value):
        pass

    def verify_update(self, length, restrict, attribute, value=None):
        format_reg = {
            'limit': length,
            'restrict': restrict
        }
        value = str(value)
        if int(length) == 1:
            length = 8
        return self.error_insert(attr=attribute, word="Max Length") if len(value) > int(length) else value if re.match("^{restrict}{{0,{limit}}}$".format(**format_reg), value) else self.error_insert(attr=attribute, word="Incorrect format")

    def prepare_statement(self):
        self.sql = "UPDATE `{table}`".format(table=self.table)
        try:
            self.prepare_argument()
        except Exception as e:
            self.log_error(e)
        try:
            self.prepare_condition()
        except Exception as e:
            self.log_error(e)

    def prepare_argument(self):
        self.params_value = {}
        self.params_conditon = {}
        for key in self.argument.keys():
            if 'val' in key and self.argument[key].value != 'None':
                self.params_value[re.compile("=?\[(.*)\]").search(key).group(1)] = self.argument[key].value
            elif 'cond' in key:
                self.params_conditon[re.compile("=?\[(.*)\]").search(key).group(1)] = self.argument[key].value

    def prepare_condition(self):
        if len(self.params_value) > 0:
            self.sql += ' SET ' + ', '.join(map(lambda item: "`{key}`='{value}'".format(key=self.dictionary[item], value=self.checker(item, self.params_value[item])), self.params_value))
            if len(self.params_conditon) > 0:
                self.sql += ' WHERE ' + ' and '.join(map(lambda item: "`{condition}`='{val}'".format(condition=self.dictionary[item], val=self.checker(item, self.params_conditon[item])), self.params_conditon)) + ';'
            else:
                self.error_update(word="Missing condition for update")
        else:
            self.error_update(word="Missing data for update")

    def execute_sql(self, sql):
        self.db.mycursor.execute(sql)
        self.db.connection.commit()
        self.output_type = 'plain'
        self.output_flag = True
        self.output = "Update row in {tlb} Succesfully".format(tlb=self.table)

class UpdateProbe(PatchMethod):
    dictionary = GetProbe.dict_attribute
    table = 'PROBES'

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
                        return self.error_update(word="incorrect ip format")
                if max(ipList) < 256:
                    return ip_str
                else:
                    return self.error_update(word="incorrect range ip")
            else:
                return self.error_update(word="incorrect ip format")
        else:
            return self.error_update(word="incorrect ip format")

    def macFromatChk(self, mac):
        if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
            return mac
        else:
            return self.error_update(word="Invalid MAC Address Format")

    def checker(self, key, value):
        option = {
            'ipb': partial(self.verify_update, 32, "[a-zA-Z0-9\_\-]", 'probe_id'),
            'pb_nom': partial(self.verify_update, 32, "[a-zA-Z0-9\_\-]", 'probe_name'),
            'ipadr': partial(self.ipFormatChk),
            'madr': partial(self.macFromatChk),
            'pb_stat': partial(self.verify_update, 1, "(?:Active|Deactive|Idle|1|2|3)", 'probe_status'),
        }
        return option[key](value)


class UpdateService(PatchMethod):
    dictionary = GetService.dict_attribute
    table = 'SERVICES'

    def checker(self, key, value):
        often_pattern = "[a-zA-Z0-9\s~!@#$%^&?*()+`={}|\[\];':.\\\/]"
        option = {
            'isvc': partial(self.verify_update, 11, '[0-9]', 'service_id'),
            'nsvc': partial(self.verify_update, 32, '[a-zA-Z0-9\_\-]', 'service_name'),
            'trans_prot': partial(self.verify_update, 1, '(?:tcp|udp|other|1|2|3)', 'transport_protocol'),
            'f_cmd': partial(self.verify_update, 256, often_pattern, 'file_command'),
            'fn': partial(self.verify_update, 64, '[a-zA-Z0-9\.\-\_]', 'file_name'),
            'u_cmd': partial(self.verify_update, 2083, often_pattern, 'udp_command'),
            'svc_desc': partial(self.verify_update, 2083, often_pattern, 'service_description'),
            'svc_dest_ex': partial(self.verify_update, 2083, often_pattern, 'destination_example'),
        }
        return option[key](value)

class UpdateDestination(PatchMethod):
    dictionary = GetDestination.dict_attribute
    table = 'DESTINATIONS'

    def checker(self, key, value):
        option = {
            'idest': partial(self.verify_update, 11, '[0-9]', 'destination_id'),
            'isvc': partial(self.verify_update, 11, '[0-9]', 'service_id'),
            'ndest': partial(self.verify_update, 248, '[a-zA-Z0-9\_\-\.\:\?\=\/]', 'destination_name'),
            'ptdest': partial(self.verify_update, 5, '[0-9]', 'destination_port'),
            'dest_desc': partial(self.verify_update, 2083, '[a-zA-Z0-9\s~!@#$%^&?*()+`={}|\[\];\':.\\\/-_]', 'destination_description'),
        }
        return option[key](value)


class UpdateRunningService(PatchMethod):
    dictionary = GetRunningService.dict_attribute
    table = 'RUNNING_SERVICES'

    def checker(self, key, value):
        option = {
            'n_svc': partial(self.verify_update, 11, '[0-9]', 'no_svc'),
            'isvc': partial(self.verify_update, 11, '[0-9]', 'service_id'),
            'iclus': partial(self.verify_update, 11, '[0-9]', 'cluster_id'),
            'rning_svc_stat': partial(self.verify_update, 1, '(?:Active|Deactive|1|2|)', 'running_svc_status'),
            }
        return option[key](value)

class UpdateRunningDestination(PatchMethod):
    dictionary = GetRunningDestination.dict_attribute
    table = 'RUNNING_DESTINATIONS'

    def checker(self, key, value):
        option = {
            'n_dest': partial(self.verify_update, 11, '[0-9]', 'no_dest'),
            'idest': partial(self.verify_update, 11, '[0-9]', 'destination_id'),
            'iclus': partial(self.verify_update, 11, '[0-9]', 'cluster_id'),
            'rning_dest_stat': partial(self.verify_update, 1, '(?:Active|Deactive|1|2|)', 'running_dest_status'),
        }
        return option[key](value)

class UpdateCluster(PatchMethod):
    dictionary = GetCluster.dict_attribute
    table = 'CLUSTERS'
    temp = Method(None, None)
    def checker(self, key, value):
        option = {
            'iclus': partial(self.verify_update, 11, '[0-9]', 'cluster_id'),
            'ipb': partial(self.verify_update, 32, "[a-zA-Z0-9\_\-]", 'probe_id'),
            'clus_deesc': partial(self.verify_update, 1, '[a-zA-Z0-9\s~!@#$%^&?*()+`={}|\[\];\':.\\\/-_]', 'running_dest_status'),
        }
        return option[key](value)


class UpdateUser(PatchMethod):
    dictionary = GetUser.dict_attribute
    table = 'user'

    def prepare_condition(self):
        uid = self.argument["cond[uid]"].value
        self.sql += " WHERE `username`='{uid}';".format(uid=uid)


if __name__ == '__main__':
    print "Access-Control-Allow-Origin: *"
    print "Access-Control-Allow-Headers: X-HTTP-Method-Override"

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
        'clus': GetCluster,
    }
    dict_tlb_post = {
        'dest': InsertDestination,
        'persty': InsertUser,
        'svc': InsertService,
        'clus': InsertCluster,

    }
    dict_tlb_del = {
        'dest': DeleteDestination,
        'svc': DeleteService,
        'pb': DeleteProbe,
        'persty': DeleteUser,
        'clus': DeleteCluster,
    }
    dict_tlb_update = {
        'pb': UpdateProbe,
        'svc': UpdateService,
        'dest': UpdateDestination,
        'rning_svc': UpdateRunningService,
        'rning_dest': UpdateRunningDestination,
        'persty': UpdateUser,

    }

    def check_token():
        agent_token = environ['HTTP_AUTHORIZATION']
        jwt_token = token.JsonWebToken()
        jwt_token.decrypt_token(agent_token)


    def do_it():
        try:
            check_override = environ['HTTP_X_HTTP_METHOD_OVERRIDE'].lower()
        except:
            check_override = None

        if check_override == 'get':
            example = dict_tlb[tlb](argument, environ)
        else:
            check_token()
            if method_main == 'post':
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

    def tester_header():
        # import os
        #
        # print "Content-Type: text/html"
        # print "Cache-Control: no-cache"
        #
        # print "<html><body>"
        # for headername, headervalue in os.environ.iteritems():
        #     if headername.startswith("HTTP_"):
        #         print "<p>{0} = {1}</p>".format(headername, headervalue)
        # print "</html></body>"

        # argument = cgi.FieldStorage()
        # print argument
        # print "Content-Type: text/html\n"
        # print "Access-Control-Allow-Origin: *"
        # for a in environ:
        #     print 'Var: ', a, 'Value: ', os.getenv(a), '<br>'
        # print("all done")
        # print dir(os.environ), '<br>'
        # !/usr/local/bin/python
        print "Content-type: text/html"
        print
        print "<pre>"
        import os, sys
        from cgi import escape
        print "<strong>Python %s</strong>" % sys.version
        keys = os.environ.keys()
        keys.sort()
        for k in keys:
            print "%s\t%s" % (escape(k), escape(os.environ[k]))
        print "</pre>"


    def tester():
        print "Content-Type: text/html\n"
        print sys.stdin.read()
        # print "------------------------------------ <br>", argument, "<br>"
        # print "------------------------------------ <br>", argument.list, "<br>"
        # print "------------------------------------ <br>", argument.keys(), "<br>"
        # new = dict((key, value) for key, value in argument.list.iteritems() if 'val' in key)

        # print "------------------------------------ <br>", new, "<br>"

        # for i in range(len(argument.getvalue("key[]"))):
        #     print argument.getvalue("key[]")[i]
        #     print argument.getvalue("value[]")[i]
        print 'Hello -   ---------------------------------------------------------- <br><br>'

        params = {}
        for key in argument.keys():
            params[key] = argument[key].value

        print params
        # all_keys = argument.keys()
        # print type(all_keys)

        # dict_attribute = {
        #     'isvc': 'service_id',
        #     'nsvc': 'service_name',
        #     'fn': 'file_name',
        #     'cmd': 'command'
        # }
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

        # verbs = ""
        # verbs += " ORDER BY " + ', '.join(map(lambda item: "`{attr}` {sort}".format(attr=dict_attribute[item],
        #                                                                             sort=argument.getvalue(
        #                                                                                 'order[{item}]'.format(
        #                                                                                     item=item))) if argument.has_key(
        #     'order[{xxx}]'.format(xxx=item)) else 'null', dict_attribute))
        # print verbs
        # verbs += ", ".join(map(lambda item: , ))


    do_it()
    # tester()
    # tester_header()
