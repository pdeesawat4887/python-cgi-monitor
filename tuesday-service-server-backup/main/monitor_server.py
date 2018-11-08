# /usr/bin/python

import database as maria
import requests


class Server:

    def __init__(self):
        self.db = maria.MySQLDatabase()

    def working_notify(self):
        static_sql = "SELECT (select `probe_name` from CLUSTERS join PROBES on CLUSTERS.probe_id=PROBES.probe_id WHERE CLUSTERS.cluster_id=test.cluster_id) as probe_name," \
                     "(select `ip_address` from CLUSTERS join PROBES on CLUSTERS.probe_id=PROBES.probe_id WHERE CLUSTERS.cluster_id=test.cluster_id) as ip_address, " \
                     "`start_date`, `service_name`, `service_description`, `destination_name`, `destination_port`, `round_trip_time`, `download`, `upload`, `other`, `other_unit`, `other_description`" \
                     "FROM TESTRESULTS test LEFT JOIN DESTINATIONS dest ON dest.destination_id=test.destination_id LEFT JOIN SERVICES svc ON svc.service_id=test.service_id " \
                     "WHERE `start_date` >= (NOW() - INTERVAL 10 MINUTE) and ({condition});"

        mapping_status = {'pass': '1', 'fail': '2', 'error': '3',}
        all_notify = self.db.select("SELECT * FROM NOTIFICATIONS")
        all_notify_description = [field[0] for field in self.db.mycursor.description]
        self.result = map(lambda notify: dict(zip(all_notify_description, notify)), all_notify)

        for attr in self.result:
            condition = []

            if attr['notify_status'] == 'Active':
                if attr['notify_result_status'] != None:
                    condition.append("`result_status`{sym_status}{res_stat}".format(sym_status=attr['notify_symbol_status'], res_stat=mapping_status[attr['notify_result_status']]))
                if attr['notify_rtt'] != None and attr['notify_symbol_rtt'] != None:
                    condition.append("`round_trip_time`{sym_rtt}{rtt}".format(sym_rtt=attr['notify_symbol_rtt'], rtt=attr['notify_rtt']))
                if attr['notify_download'] != None and attr['notify_symbol_download'] != None:
                    condition.append("`download`{sym_dl}{dl}".format(sym_dl=attr['notify_symbol_download'], dl=attr['notify_download']))
                if attr['notify_upload'] != None and attr['notify_symbol_upload'] != None:
                    condition.append("`upload`{sym_ul}{ul}".format(sym_ul=attr['notify_symbol_upload'], ul=attr['notify_upload']))
                if attr['notify_other'] != None and attr['notify_symbol_other'] != None:
                    condition.append("`other`{sym_other}{other}".format(sym_other=attr['notify_sym_other'], other=attr['notify_other']))

                sql_statement = static_sql.format(condition=' {operate} '.format(operate=attr['notify_condition']).join(condition))
                # print sql_statement
                output = self.db.select(sql_statement)
                output_description = [field[0] for field in self.db.mycursor.description]

                if output:
                    token = self.db.select("SELECT `token_value` FROM NOTIFY_TOKEN WHERE `token_id`='{tid}'".format(tid=attr['notify_token_id']))[0][0]
                    self.line_messenger(token=token, attribute=output_description ,list_result=output, notify_desc=attr['notify_description'])
                    print "Successfully Notify"
            else:
                print "Notification {notif_desc} Disable".format(notif_desc=attr['notify_description'])

    def line_messenger(self, token, attribute, list_result, notify_desc):

        ################################################################
        ################## prepare line notification ###################

        url = 'https://notify-api.line.me/api/notify'
        headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
        msg_header = "\nWarning! {info}\n".format(info=notify_desc if notify_desc != None else '')

        ################################################################

        ################################################################
        #################### prepare line message ######################

        first = map(lambda item: dict(zip(attribute, item)), list_result)
        output = map(lambda item: dict((k, v) for k, v in item.iteritems() if v is not None), first)

        for msg in output:
            re_msg = msg_header + '\n'.join(map(lambda key: "- {key}: {value}".format(key=key.capitalize().replace('_', ' '), value=msg[key]), msg))
            try:
                request = requests.post(url=url, headers=headers, data={'message': re_msg})
                request.close()
            except Exception as error:
                print "Error Notification:", error

        ################################################################

        ################################################################
        ########################### DEBUG HERE #########################

        # print "Attribute", attribute
        # print "LIST RESULT", list_result
        # print "FIRST", first
        # print "OUTPUT", output

        ################################################################

    def working_status_probe(self):
        sql_query = "SELECT `probe_id` FROM PROBES WHERE `last_updated` <= (NOW() - INTERVAL 1 HOUR);"
        sql_update = "UPDATE PROBES SET `probe_status`='Inactive' WHERE `probe_id`='{ipb}'"
        map(lambda item: self.db.mycursor.execute(sql_update.format(ipb=item[0])), self.db.select(sql_query))
        self.db.connection.commit()
        print 'Successfully Update Probe Status.'

if __name__ == '__main__':
    server = Server()
    # server.notify_working()
    server.monitor_probe()