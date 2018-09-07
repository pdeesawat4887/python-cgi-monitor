#!/usr/bin/python
# import mysql.connector as mariadb
import main.database as mariadb

print '''Content-type: text/html\n'''


def list_probe():
    list_probe = get_list_probe()
    print '''        <section class="section" id="probe_list">
            <div class="container has-text-centered">
                <div class="columns is-multiline is-centered">'''
    for probe in list_probe:
        list_service = get_list_service(probe[0])
        print '''                    <div class="column is-narrow is-3">
                        <a>
                            <div class="box" id="{}">
                                <div class="content">
                                    <h3 class="title is-5">{}</h3>
                                    <p class="is-6">MAC : {}</p>
                                    <p class="is-6">IP : {}</p>
                                    <hr>
                                    <p class="subtitle is-6">Probe Status :'''.format(probe[0], probe[1],
                                                                                      probe[3].upper(),
                                                                                      probe[2])
        if (probe[4] == 0):
            print '''                                       Online'''
        else:
            print '''                                       Offline'''
        print '''                                    </p>
                                    <hr>'''
        for service in list_service:
            status = round(get_status_service(probe[0], service[0]), 2)
            print '''                                    <p class="subtitle is-7 has-text-centered">{} Status : {}%</p>'''.format(
                service[0].upper(), status)
        print '''                                </div>
                            </div>
                        </a>
                     </div>'''

    print '''                </div>
            </div>
        </section>
        <script>
            $(document).ready(function () {'''
    for probe in list_probe:
        print '''                $("#{}").on('click', function () '''.format(probe[0])
        print '''                {
                    $.ajax({
                        url: 'probe_info.py',
                        type: 'post',
                        data: {
                            probe_id: this.id
                        },
                        success: function (response) {
                            $("#display").html(response);
                        }
                    });
                });'''
    print '''            });
        </script>'''


def get_list_probe():
    # mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
    #                                      host='192.168.254.31')
    # cursor = mariadb_connection.cursor()
    # cursor.execute(
    #     "select probe.probe_id, probe.probe_name, probe.ip_address, probe.mac_address, probe.`status` from probe")
    # list_probe = cursor.fetchall()
    db = mariadb.MySQLDatabase()
    list_probe = db.select("probe", None, "probe_id", "probe_name", "ip_address", "mac_address", "`status`")
    return list_probe


def get_list_service(probe_id):
    # mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
    #                                      host='192.168.254.31')
    # cursor = mariadb_connection.cursor()
    # cursor.execute(
    #     "select service_name from service join running_service on service.service_id = running_service.service_id where running_service.probe_id = '{}' and running_service.running = 0;".format(
    #         probe_id))
    # list_service = cursor.fetchall()
    db = mariadb.MySQLDatabase()
    db.mycursor.execute(
        "select service_name from service join running_service on service.service_id = running_service.service_id where running_service.probe_id = '{}' and running_service.running = 0;".format(
            probe_id))
    list_service = db.mycursor.fetchall()
    return list_service


def get_status_service(probe_id, service_type):
    # mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
    #                                      host='192.168.254.31')
    # cursor = mariadb_connection.cursor()
    # cursor.execute(
    #     "select count(performance_service.time) from performance_service join destination join service join running_service on service.service_id = running_service.service_id and performance_service.destination_id = destination.destination_id and service.service_id = destination.service_id where performance_service.probe_id = '{}' and service.service_name = '{}' and running_service.running = 0;".format(
    #         probe_id, service_type))
    # all_count = cursor.fetchone()[0]
    # if (all_count != 0):
    #     cursor.execute(
    #         "select count(performance_service.time) from performance_service join destination join service join running_service on service.service_id = running_service.service_id and performance_service.destination_id = destination.destination_id and service.service_id = destination.service_id where performance_service.probe_id = '{}' and service.service_name = '{}' and running_service.running = 0 and ((performance_service.ping != 0 and performance_service.download < 50 and performance_service.upload < 10) or (performance_service.ping = 0 and performance_service.download < 4 and performance_service.upload = 0));".format(
    #             probe_id, service_type))
    #     warning_count = cursor.fetchone()[0]
    #     if (all_count == 0 and warning_count == 0):
    #         percentage = 100
    #     else:
    #         percentage = float(warning_count) / float(all_count) * 100
    # else:
    #     cursor.execute(
    #         "select count(availability_service.time) from availability_service join destination join service join running_service on service.service_id = running_service.service_id and availability_service.destination_id = destination.destination_id and service.service_id = destination.service_id where availability_service.probe_id = '{}' and service.service_name = '{}' and running_service.running = 0;".format(
    #             probe_id, service_type))
    #     all_count = cursor.fetchone()[0]
    #     cursor.execute(
    #         "select count(availability_service.time) from availability_service join destination join service join running_service on service.service_id = running_service.service_id and availability_service.destination_id = destination.destination_id and service.service_id = destination.service_id where availability_service.probe_id = '{}' and service.service_name = '{}' and availability_service.`status` != 0 and availability_service.response_time = 0 and running_service.running = 0;".format(
    #             probe_id, service_type))
    #     warning_count = cursor.fetchone()[0]
    #     if (all_count == 0 and warning_count == 0):
    #         percentage = 100
    #     else:
    #         percentage = float(warning_count) / float(all_count) * 100
    db = mariadb.MySQLDatabase()
    db.mycursor.execute(
        "select count(performance_service.time) from performance_service join destination join service join running_service on service.service_id = running_service.service_id and performance_service.destination_id = destination.destination_id and service.service_id = destination.service_id where performance_service.probe_id = '{}' and service.service_name = '{}' and running_service.running = 0;".format(
            probe_id, service_type))
    total_all = db.mycursor.fetchone()[0]
    if (total_all != 0):
        db.mycursor.execute(
            "select count(performance_service.time) from performance_service join destination join service join running_service on service.service_id = running_service.service_id and performance_service.destination_id = destination.destination_id and service.service_id = destination.service_id where performance_service.probe_id = '{}' and service.service_name = '{}' and running_service.running = 0 and ((performance_service.ping != 0 and performance_service.download < 50 and performance_service.upload < 10) or (performance_service.ping = 0 and performance_service.download < 4 and performance_service.upload = 0));".format(
                probe_id, service_type))
        total_warning = db.mycursor.fetchone()[0]
        if (total_all == 0 and total_warning == 0):
            percentage = 100
        else:
            percentage = float(total_warning) / float(total_all) * 100
    else:
        db.mycursor.execute(
            "select count(availability_service.time) from availability_service join destination join service join running_service on service.service_id = running_service.service_id and availability_service.destination_id = destination.destination_id and service.service_id = destination.service_id where availability_service.probe_id = '{}' and service.service_name = '{}' and running_service.running = 0;".format(
                probe_id, service_type))
        total_all = db.mycursor.fetchone()[0]
        db.mycursor.execute(
            "select count(availability_service.time) from availability_service join destination join service join running_service on service.service_id = running_service.service_id and availability_service.destination_id = destination.destination_id and service.service_id = destination.service_id where availability_service.probe_id = '{}' and service.service_name = '{}' and availability_service.`status` != 0 and availability_service.response_time = 0 and running_service.running = 0;".format(
                probe_id, service_type))
        total_warning = db.mycursor.fetchone()[0]
        if (total_all == 0 and total_warning == 0):
            percentage = 100
        else:
            percentage = float(total_warning) / float(total_all) * 100
    return 100 - percentage


# get_status_service('ba27ebfffe15598a', 'speedtest')

list_probe()
