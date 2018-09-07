#!/usr/bin/python
import mysql.connector as mariadb

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
    probe_active_count = get_count_anything('probe_id', 'probe', 'status', '0')
    probe_down_count = get_count_anything('probe_id', 'probe', 'status', '1')
    service_count = get_count_anything('service_id', 'service')
    warning_count = get_warning_count_performance_service()[0] + \
                    get_warning_count_availability_service()[0]
    print '''                    <section class="info-tiles">
                        <div class="tile is-ancestor has-text-centered">
                            <div class="tile is-parent">
                                <article class="tile is-child box">'''
    print '''                                    <p class="title has-text-success">{}</p>'''.format(probe_active_count)
    print '''                                    <p class="subtitle">Active Probes</p>
                                </article>
                            </div>
                            <div class="tile is-parent">
                                <article class="tile is-child box">'''
    print '''                                    <p class="title has-text-grey-light">{}</p>'''.format(probe_down_count)
    print '''                                    <p class="subtitle">Down Probes</p>
                                </article>
                            </div>
                            <div class="tile is-parent">
                                <article class="tile is-child box">'''
    print '''                                    <p class="title has-text-info">{}</p>'''.format(service_count)
    print '''                                    <p class="subtitle">Services</p>
                                </article>
                            </div>
                            <div class="tile is-parent">
                                <article class="tile is-child box">'''
    print '''                                    <p class="title has-text-danger">{}</p>'''.format(warning_count)
    print '''                                    <p class="subtitle">Warning</p>
                                </article>
                            </div>
                        </div>
                    </section>'''


def section_warning():
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
    for i in get_warning_availability_service():
        print '''                                                    <tr>'''
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            i[0])
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            i[1])
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(i[2].upper())
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            i[3])
        print '''                                                        <td class="has-text-centered">Warning</td>'''
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(i[5])
        print '''                                                    </tr>'''
    for i in get_warning_performance_service():
        print '''                                                    <tr>'''
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(i[0])
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            i[1])
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(i[2].upper())
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            i[3])
        print '''                                                        <td class="has-text-centered">Warning</td>'''
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(i[5])
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
    for i in get_probe():
        print '''                                                    <tr>'''
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(i[1])
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(i[2])
        if (i[3] == 0):
            print '''                                                        <td class="has-text-centered"><span class="icon"><i class="fas fa-lg fa-check-circle has-text-success"></i></span></td>'''
        else:
            print '''                                                        <td class="has-text-centered"><span class="icon"><i class="fas fa-lg fa-times-circle has-text-danger"></i></span></td>'''
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
    for i in get_service():
        print '''                                                    <tr>'''
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(
            i[1].upper())
        print '''                                                        <td class="has-text-centered">{}</td>'''.format(get_count_service_destination(i[1]))
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


def get_service():
    mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
                                         host='192.168.254.31')
    cursor = mariadb_connection.cursor()
    cursor.execute("select service_id, service_name from service;")
    result = cursor.fetchall()
    return result


def get_probe():
    mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
                                         host='192.168.254.31')
    cursor = mariadb_connection.cursor()
    cursor.execute("select probe_id, probe_name, ip_address, `status` from probe;")
    result = cursor.fetchall()
    return result


def get_anything(column_name, table, where=None, value=None):
    mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
                                         host='192.168.254.31')
    cursor = mariadb_connection.cursor()
    if where:
        cursor.execute("select {} from {} where {} = '{}';".format(column_name, table, where, value))
    else:
        cursor.execute("select {} from {};".format(column_name, table))
    result = cursor.fetchone()[0]
    return result


def get_anything_list(column_name, table, where=None, value=None):
    result_list = []
    mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
                                         host='192.168.254.31')
    cursor = mariadb_connection.cursor()
    if where:
        cursor.execute("select {} from {} where {} = '{}';".format(column_name, table, where, value))
    else:
        cursor.execute("select {} from {};".format(column_name, table))
    for i in cursor:
        result_list.append(str(i[0]))
    return result_list


def get_count_anything(column_name, table, where=None, value=None):
    mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
                                         host='192.168.254.31')
    cursor = mariadb_connection.cursor()
    if where:
        cursor.execute("select count({}) from {} where {} = '{}';".format(column_name, table, where, value))
    else:
        cursor.execute("select count({}) from {};".format(column_name, table))
    count_result = cursor.fetchone()[0]
    return count_result

def get_count_service_destination(service_type):
    mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
                                         host='192.168.254.31')
    cursor = mariadb_connection.cursor()
    cursor.execute(
        "select count(destination) from destination join service on destination.service_id = service.service_id where service.service_name = '{}';".format(service_type));
    result = cursor.fetchone()[0]
    return result

def get_count_availability_service():
    mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
                                         host='192.168.254.31')
    cursor = mariadb_connection.cursor()
    cursor.execute(
        "select count(destination_id) from destination join service on destination.service_id = service.service_id where destination.service_id not in (5, 6);")
    result = cursor.fetchone()[0]
    return result


def get_count_performance_service():
    mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
                                         host='192.168.254.31')
    cursor = mariadb_connection.cursor()
    cursor.execute(
        "select count(destination_id) from destination join service on destination.service_id = service.service_id where destination.service_id in (5, 6);")
    result = cursor.fetchone()[0]
    return result


def get_warning_availability_service():
    mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
                                         host='192.168.254.31')
    cursor = mariadb_connection.cursor()
    cursor.execute(
        "select probe.ip_address, probe.probe_name, service.service_name, destination.destination, availability_service.`status`, availability_service.time from destination join service join availability_service join probe on destination.service_id = service.service_id and availability_service.destination_id = destination.destination_id and probe.probe_id = availability_service.probe_id where availability_service.status != 0 order by availability_service.time desc;")
    result = cursor.fetchall()
    return result


def get_warning_performance_service():
    mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
                                         host='192.168.254.31')
    cursor = mariadb_connection.cursor()
    cursor.execute(
        "select probe.ip_address, probe.probe_name, service.service_name, destination.destination, performance_service.download, performance_service.time from destination join service join performance_service join probe on destination.service_id = service.service_id and performance_service.destination_id = destination.destination_id and probe.probe_id = performance_service.probe_id where performance_service.download = 0 order by performance_service.time desc;")
    result = cursor.fetchall()
    return result


def get_warning_count_availability_service():
    mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
                                         host='192.168.254.31')
    cursor = mariadb_connection.cursor()
    cursor.execute(
        "select count(lastest_service.destination) from (select service.service_name, destination.destination, availability_service.`status`, availability_service.response_time, availability_service.time from destination join service join availability_service on destination.service_id = service.service_id and availability_service.destination_id = destination.destination_id order by availability_service.time desc) as lastest_service where lastest_service.status != 0;")
    result = cursor.fetchall()[0]
    return result


def get_warning_count_performance_service():
    mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
                                         host='192.168.254.31')
    cursor = mariadb_connection.cursor()
    cursor.execute(
        "select count(lastest_service.destination) from (select service.service_name, destination.destination, performance_service.download, performance_service.time from destination join service join performance_service on destination.service_id = service.service_id and performance_service.destination_id = destination.destination_id order by performance_service.time desc) as lastest_service where lastest_service.download = 0;")
    result = cursor.fetchall()[0]
    return result

section_welcome()
section_status()
section_warning()
section_display()