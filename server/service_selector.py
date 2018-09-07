#!/usr/bin/python
# import mysql.connector as mariadb
import main.database as mariadb
import cgi

print '''Content-type: text/html\n'''


def probe_selector(probe_id, day):
    probe_info = get_anything("probe_name, ip_address, mac_address,`status`", "probe",
                              "probe_id = '{}'".format(probe_id))
    list_service = get_list_anything("service.service_name",
                                     "service join running_service on service.service_id = running_service.service_id",
                                     "running_service.probe_id = '{}' and running_service.running = 0 order by service.service_name desc".format(
                                         probe_id))

    print '''        <section class="section" id="list_service" style="margin-top: -80px; margin-bottom: -60px;">
            <div class="container is-fluid">
                <div class="columns is-centered">
                    <div class="tabs is-toggle is-fullwidth is-medium">
                        <ul>'''.format(probe_info[0])
    for service in list_service:
        print '''                            <li id="{}_{}_{}">
                                <a>
                                    <span>{}</span>
                                </a>
                            </li>'''.format(probe_id, service[0], day, service[0].upper())
    print '''                        </ul>
                    </div>
                </div>
            </div>
        </section>'''
    for service in list_service:
        print '''       <script>
            $("#{}_{}_{}").on('click', function ()'''.format(probe_id, service[0], day)
        print '''           {'''
        print '''           $("div.tabs.is-toggle.is-fullwidth.is-medium ul li").removeClass("is-active")
            $("#{}_{}_{}").addClass("is-active")'''.format(probe_id, service[0], day)
        print '''           $.ajax({
                url: 'graph_result.py',
                type: 'post',
                data: {
                    data: this.id
                },
                success: function (response) {
                    $("#content").html(response);
                }
            });
        });
    </script>'''
    print '''        <section class="section" id="content">
        </section>'''


def get_anything(column_name, table, where=None):
    db = mariadb.MySQLDatabase()
    if where:
        db.mycursor.execute("select {} from {} where {};".format(column_name, table, where))
    else:
        db.mycursor.execute("select {} from {};".format(column_name, table))
    result = db.mycursor.fetchone()
    return result


def get_list_anything(column_name, table, where=None):
    db = mariadb.MySQLDatabase()
    if where:
        db.mycursor.execute("select {} from {} where {};".format(column_name, table, where))
    else:
        db.mycursor.execute("select {} from {};".format(column_name, table))
    list_result = []
    for i in db.mycursor:
        list_result.insert(0, i)
    return list_result


# def get_probe_info(probe_id):
#     # mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
#     #                                      host='192.168.254.31')
#     # cursor = mariadb_connection.cursor()
#     # cursor.execute("select probe_name, ip_address, mac_address,`status` from probe where probe_id = '{}';".format(probe_id))
#     # probe_info = cursor.fetchone()
#     db = mariadb.MySQLDatabase()
#     db.mycursor.execute(
#         "select probe_name, ip_address, mac_address,`status` from probe where probe_id = '{}';".format(probe_id))
#     probe_info = db.mycursor.fetchone()
#     return probe_info

# def get_list_service(probe_id):
#     # mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
#     #                                      host='192.168.254.31')
#     # cursor = mariadb_connection.cursor()
#     # cursor.execute("select service_name from service join running_service on service.service_id = running_service.service_id where running_service.probe_id = '{}' and running_service.running = 0;".format(probe_id))
#     # list_service = cursor.fetchall()
#     db = mariadb.MySQLDatabase()
#     db.mycursor.execute(
#         "select service_name from service join running_service on service.service_id = running_service.service_id where running_service.probe_id = '{}' and running_service.running = 0;".format(
#             probe_id))
#     list_service = db.mycursor.fetchall()
#     return list_service

form = cgi.FieldStorage()
data = form.getvalue('data')
tmp = data.split('_')
probe_id = tmp[0]
range_day = tmp[1]
probe_selector(probe_id, range_day)
