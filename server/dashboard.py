#!/usr/bin/python
# import mysql.connector as mariadb
import main.database as mariadb

print '''Content-type: text/html\n'''


def section_welcome():
    print '''    <section class="section">
        <div class="container is-fluid">
            <div class="columns is-centered">
                <div class="column">
                    <section class="hero is-small" style="margin-bottom: 2%; margin-top: -5%;">
                        <div class="hero-body">
                            <div class="container">
                                <h1 class="title">
                                    Hello, Admin.
                                </h1>
                                <h2 class="subtitle">
                                    I hope you are having a great day!
                                </h2>
                            </div>
                        </div>
                    </section>'''


def section_status():
    count_active_probe = get_count_anything("probe.probe_id", "probe", "probe.`status` = 0")
    count_down_probe = get_count_anything("probe.probe_id", "probe", "probe.`status` = 1")
    count_service = get_count_anything("service.service_id", "service")
    count_warning_availability_service = get_count_anything("lastest_service.destination",
                                                            "(select service.service_name, destination.destination, availability_service.`status`, availability_service.response_time, availability_service.time from destination join service join availability_service on destination.service_id = service.service_id and availability_service.destination_id = destination.destination_id order by availability_service.time desc) as lastest_service",
                                                            "lastest_service.status != 0 and lastest_service.response_time = 0")
    count_warning_performance_service = get_count_anything("lastest_service.destination",
                                                           "(select service.service_name, destination.destination, performance_service.ping, performance_service.download, performance_service.time from destination join service join performance_service on destination.service_id = service.service_id and performance_service.destination_id = destination.destination_id order by performance_service.time desc) as lastest_service",
                                                           "lastest_service.download = 0 and lastest_service.ping = 0")
    count_warning = count_warning_availability_service + count_warning_performance_service
    print '''                    <section class="info-tiles">
                        <div class="tile is-ancestor has-text-centered">
                            <div class="tile is-parent">
                                <article class="tile is-child box">'''
    print '''                                    <p class="title has-text-success">{}</p>'''.format(count_active_probe)
    print '''                                    <p class="subtitle">Active Probes</p>
                                </article>
                            </div>
                            <div class="tile is-parent">
                                <article class="tile is-child box">'''
    print '''                                    <p class="title has-text-grey-light">{}</p>'''.format(count_down_probe)
    print '''                                    <p class="subtitle">Down Probes</p>
                                </article>
                            </div>
                            <div class="tile is-parent">
                                <article class="tile is-child box">'''
    print '''                                    <p class="title has-text-info">{}</p>'''.format(count_service)
    print '''                                    <p class="subtitle">Services</p>
                                </article>
                            </div>
                            <div class="tile is-parent">
                                <article class="tile is-child box">'''
    print '''                                    <p class="title has-text-danger">{}</p>'''.format(count_warning)
    print '''                                    <p class="subtitle">Warning</p>
                                </article>
                            </div>
                        </div>
                    </section>'''


def section_warning():
    warning_availability_service = get_list_anything(
        "probe.ip_address, probe.probe_name, service.service_name, destination.destination, availability_service.`status`, availability_service.time",
        "destination join service join availability_service join probe on destination.service_id = service.service_id and availability_service.destination_id = destination.destination_id and probe.probe_id = availability_service.probe_id",
        "availability_service.status != 0 and availability_service.response_time = 0 order by availability_service.time asc")
    warning_performance_service = get_list_anything(
        "probe.ip_address, probe.probe_name, service.service_name, destination.destination, performance_service.download, performance_service.time",
        "destination join service join performance_service join probe on destination.service_id = service.service_id and performance_service.destination_id = destination.destination_id and probe.probe_id = performance_service.probe_id",
        "performance_service.download = 0 and performance_service.ping = 0 order by performance_service.time asc")
    print '''                   <section class="section">
                        <div class="columns is-centered">
                            <div class="column">
                                <div class="card">
                                    <header class="card-header">
                                        <p class="card-header-title">
                                            Warning
                                        </p>
                                        <a class="card-header-icon" aria-label="more options" id="warning_button">
                                            <span class="icon">
                                                <i class="fas fa-angle-down" aria-hidden="true"></i>
                                            </span>
                                        </a>
                                    </header>
                                    <div class="card-content" style="overflow: auto; height: 240px;" id="warning_content">
                                        <div class="content" style="margin-bottom: 20px;">
                                            <table class="table is-bordered is-narrow is-fullwidth">
                                                <thead>
                                                    <tr>
                                                        <th class="has-text-centered">Probe IP</th>
                                                        <th class="has-text-centered">Probe Name</th>
                                                        <th class="has-text-centered">Service Name</th>
                                                        <th class="has-text-centered">Destination Name</th>
                                                        <th class="has-text-centered">Destination Status</th>
                                                        <th class="has-text-centered">Time</th>
                                                    </tr>
                                                </thead>
                                                <tbody>'''
    for warning_info in warning_availability_service:
        print '''                                                    <tr>'''
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            warning_info[0])
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            warning_info[1])
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            warning_info[2])
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            warning_info[3])
        print '''                                                        <td class="has-text-centered">Warning</td>'''
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            str(warning_info[5]))
        print '''                                                    </tr>'''
    for warning_info in warning_performance_service:
        print '''                                                    <tr>'''
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            warning_info[0])
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            warning_info[1])
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            warning_info[2])
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            warning_info[3])
        print '''                                                        <td class="has-text-centered">Warning</td>'''
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            str(warning_info[5]))
        print '''                                                    </tr>'''
    print '''                                </tbody>
                                                             </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>'''


def section_display():
    list_probe = get_list_anything("probe_name, ip_address, `status`", "probe order by probe_name desc")
    list_service = get_list_anything("service_name", "service order by service_name desc")
    print '''                    <section class="section" style="margin-top: -4%;">
                        <div class="columns is-centered">
                            <div class="column is-6">
                                <div class="card">
                                    <header class="card-header">
                                        <p class="card-header-title">
                                            Probes
                                        </p>
                                        <a class="card-header-icon" aria-label="more options" id="probe_button">
                                            <span class="icon">
                                                <i class="fas fa-angle-down" aria-hidden="true"></i>
                                            </span>
                                        </a>
                                    </header>
                                    <div class="card-content" style="overflow: auto; height: 280px;" id="probe_content">
                                        <div class="content" style="margin-bottom: 20px;">
                                            <table class="table is-bordered is-narrow is-fullwidth">
                                                <thead>
                                                    <tr>
                                                        <th class="has-text-centered">Probe Name</th>
                                                        <th class="has-text-centered">Probe IP</th>
                                                        <th class="has-text-centered">Probe Status</th>
                                                    </tr>
                                                </thead>
                                                <tbody>'''
    for probe_info in list_probe:
        print '''                                                    <tr>'''
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            probe_info[0])
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            probe_info[1])
        if probe_info[2] == 0:
            print '''                                                        <td class="has-text-centered">Online</td>'''
            # print '''                                                        <td class="has-text-centered"><span class="icon"><i class="fas fa-lg fa-check-circle has-text-success"></i></span></td>'''
        else:
            print '''                                                        <td class="has-text-centered">Offline</td>'''
            # print '''                                                        <td class="has-text-centered"><span class="icon"><i class="fas fa-lg fa-times-circle has-text-danger"></i></span></td>'''
        print '''                                                    <tr>'''
    print '''                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="column is-6">
                                <div class="card">
                                    <header class="card-header">
                                        <p class="card-header-title">
                                            Services
                                        </p>
                                        <a class="card-header-icon" aria-label="more options" id="service_button">
                                            <span class="icon">
                                                <i class="fas fa-angle-down" aria-hidden="true"></i>
                                            </span>
                                        </a>
                                    </header>
                                    <div class="card-content" style="overflow: auto; height: 280px;" id="service_content">
                                        <div class="content" style="margin-bottom: 20px;">
                                            <table class="table is-bordered is-narrow is-fullwidth">
                                                <thead>
                                                    <tr>
                                                        <th class="has-text-centered">Service Name</th>
                                                        <th class="has-text-centered">Total Destination</th>
                                                    </tr>
                                                </thead>
                                                <tbody>'''
    for service in list_service:
        count_service_destination = get_count_anything("destination.destination_id",
                                                       "destination join service on destination.service_id = service.service_id",
                                                       "service.service_name = '{}'".format(service[0]))
        print '''                                                    <tr>'''
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            service[0].upper())
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            count_service_destination)
        print '''                                                    </tr>'''
    print '''                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
            </div>
        </div>
    </section>
</section>
<script>
    $(document).ready(function () {
        $(".navbar-burger").click(function () {
            $(".navbar-burger").toggleClass("is-active");
            $(".navbar-menu").toggleClass("is-active");
        });
        $("#warning_button").click(function () {
            $("#warning_content").toggle();
        });
        $("#probe_button").click(function () {
            $("#probe_content").toggle();
        });
        $("#service_button").click(function () {
            $("#service_content").toggle();
        });
    });
</script>'''


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


def get_count_anything(column_name, table, where=None):
    db = mariadb.MySQLDatabase()
    if where:
        db.mycursor.execute("select count({}) from {} where {};".format(column_name, table, where))
    else:
        db.mycursor.execute("select count({}) from {};".format(column_name, table))
    count_result = db.mycursor.fetchone()[0]
    return count_result


# count_availability_service = get_count_anything("destination.destination_id",
#                                                 "destination join service on destination.service_id = service.service_id",
#                                                 "destination.service_id not in (5, 6)")
# count_performance_service = get_count_anything("destination.destination_id",
#                                                "destination join service on destination.service_id = service.service_id",
#                                                "destination.service_id in (5, 6)")

# def get_service():
#     mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
#                                          host='192.168.254.31')
#     cursor = mariadb_connection.cursor()
#     cursor.execute("select service_id, service_name from service;")
#     result = cursor.fetchall()
#     return result

# def get_probe():
#     mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
#                                          host='192.168.254.31')
#     cursor = mariadb_connection.cursor()
#     cursor.execute("select probe_name, ip_address, `status` from probe;")
#     result = cursor.fetchall()
#     return result

# def get_list_probe():
#     # mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
#     #                                      host='192.168.254.31')
#     # cursor = mariadb_connection.cursor()
#     # cursor.execute("select probe_name, ip_address, mac_address,`status` from probe where probe_id = '{}';".format(probe_id))
#     # probe_info = cursor.fetchone()
#     db = mariadb.MySQLDatabase()
#     db.mycursor.execute(
#         "select probe_name, ip_address, `status` from probe;")
#     probe_info = db.mycursor.fetchone()
#     return probe_info
#
# def get_list_service():
#     # mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
#     #                                      host='192.168.254.31')
#     # cursor = mariadb_connection.cursor()
#     # cursor.execute("select service_name from service join running_service on service.service_id = running_service.service_id where running_service.probe_id = '{}' and running_service.running = 0;".format(probe_id))
#     # list_service = cursor.fetchall()
#     db = mariadb.MySQLDatabase()
#     db.mycursor.execute(
#         "select service_name from service;")
#     list_service = db.mycursor.fetchall()
#     return list_service

# def get_anything(column_name, table, where=None, value=None):
#     mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
#                                          host='192.168.254.31')
#     cursor = mariadb_connection.cursor()
#     if where:
#         cursor.execute("select {} from {} where {} = '{}';".format(column_name, table, where, value))
#     else:
#         cursor.execute("select {} from {};".format(column_name, table))
#     result = cursor.fetchone()[0]
#     return result


# def get_anything_list(column_name, table, where=None, value=None):
#     result_list = []
#     mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
#                                          host='192.168.254.31')
#     cursor = mariadb_connection.cursor()
#     if where:
#         cursor.execute("select {} from {} where {} = '{}';".format(column_name, table, where, value))
#     else:
#         cursor.execute("select {} from {};".format(column_name, table))
#     for i in cursor:
#         result_list.append(str(i[0]))
#     return result_list


# def get_count_anything(column_name, table, where=None, value=None):
#     mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
#                                          host='192.168.254.31')
#     cursor = mariadb_connection.cursor()
#     if where:
#         cursor.execute("select count({}) from {} where {} = '{}';".format(column_name, table, where, value))
#     else:
#         cursor.execute("select count({}) from {};".format(column_name, table))
#     count_result = cursor.fetchone()[0]
#     return count_result


# def get_count_service_destination(service_type):
#     mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
#                                          host='192.168.254.31')
#     cursor = mariadb_connection.cursor()
#     cursor.execute(
#         "select count(destination) from destination join service on destination.service_id = service.service_id where service.service_name = '{}';".format(service_type));
#     result = cursor.fetchone()[0]
#     return result

# def get_count_availability_service():
#     mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
#                                          host='192.168.254.31')
#     cursor = mariadb_connection.cursor()
#     cursor.execute(
#         "select count(destination_id) from destination join service on destination.service_id = service.service_id where destination.service_id not in (5, 6);")
#     result = cursor.fetchone()[0]
#     return result

# def get_count_performance_service():
#     mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
#                                          host='192.168.254.31')
#     cursor = mariadb_connection.cursor()
#     cursor.execute(
#         "select count(destination_id) from destination join service on destination.service_id = service.service_id where destination.service_id in (5, 6);")
#     result = cursor.fetchone()[0]
#     return result

# def get_warning_availability_service():
#     mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
#                                          host='192.168.254.31')
#     cursor = mariadb_connection.cursor()
#     cursor.execute(
#         "select probe.ip_address, probe.probe_name, service.service_name, destination.destination, availability_service.`status`, availability_service.time from destination join service join availability_service join probe on destination.service_id = service.service_id and availability_service.destination_id = destination.destination_id and probe.probe_id = availability_service.probe_id where availability_service.status != 0 order by availability_service.time desc;")
#     result = cursor.fetchall()
#     return result

# def get_warning_performance_service():
#     mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
#                                          host='192.168.254.31')
#     cursor = mariadb_connection.cursor()
#     cursor.execute(
#         "select probe.ip_address, probe.probe_name, service.service_name, destination.destination, performance_service.download, performance_service.time from destination join service join performance_service join probe on destination.service_id = service.service_id and performance_service.destination_id = destination.destination_id and probe.probe_id = performance_service.probe_id where performance_service.download = 0 order by performance_service.time desc;")
#     result = cursor.fetchall()
#     return result

# def get_warning_count_availability_service():
#     mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
#                                          host='192.168.254.31')
#     cursor = mariadb_connection.cursor()
#     cursor.execute(
#         "select count(lastest_service.destination) from (select service.service_name, destination.destination, availability_service.`status`, availability_service.response_time, availability_service.time from destination join service join availability_service on destination.service_id = service.service_id and availability_service.destination_id = destination.destination_id order by availability_service.time desc) as lastest_service where lastest_service.status != 0;")
#     result = cursor.fetchall()[0]
#     return result

# def get_warning_count_performance_service():
#     mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
#                                          host='192.168.254.31')
#     cursor = mariadb_connection.cursor()
#     cursor.execute(
#         "select count(lastest_service.destination) from (select service.service_name, destination.destination, performance_service.download, performance_service.time from destination join service join performance_service on destination.service_id = service.service_id and performance_service.destination_id = destination.destination_id order by performance_service.time desc) as lastest_service where lastest_service.download = 0;")
#     result = cursor.fetchall()[0]
#     return result

section_welcome()
section_status()
section_warning()
section_display()
