#!/usr/bin/env python
import mysql.connector as mariadb


class Display:

    @staticmethod
    def header():
        print '''Content-type: text/html\n
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Monitoring</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.1/css/bulma.min.css">
    <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="../canvasjs.min.js"></script>
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.1.1/css/all.css" integrity="sha384-O8whS3fhG2OnA5Kas0Y9l3cfpmYjapjI0E4theH4iuMD+pLhbf6JI0jIMfYcK3yZ"
        crossorigin="anonymous">
</head>'''

    @staticmethod
    def nav_bar():
        print '''<nav class="navbar is-dark">
    <div class="container is-fluid">
        <div class="navbar-brand">
            <a class="navbar-item" href="../cgi-bin/view.py">
                Monitoring
            </a>
            <div class="navbar-burger" data-target="navMenu">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
        <div id="navMenu" class="navbar-menu">
            <div class="navbar-start">
                <a class="navbar-item" href="../cgi-bin/inventory.py">
                    Inventorys
                </a>
            </div>
        </div>
    </div>
</nav>
<script>
    $(document).ready(function () {
        // Check for click events on the navbar burger icon
        $(".navbar-burger").click(function () {
            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            $(".navbar-burger").toggleClass("is-active");
            $(".navbar-menu").toggleClass("is-active");
        });
    });
</script>'''

    @staticmethod
    def footer():
        print '''
</html>'''

    @staticmethod
    def title_service(configure_id):
        destination, status = Display.get_service_status(configure_id)
        print '''<section class="hero is-light is-bold">
    <div class="hero-body">
        <div class="container has-text-centered">
            <!-- Main container -->
            <nav class="level">
                <!-- Left side -->
                <div class="level-left">
                    <div class="level-item">
                        <h2 class="title">
                            ''' + destination + '''
                        </h2>'''
        if (status == 0):
            print '''                        <span class="icon is-large"><i class="fas fa-lg fa-check-circle has-text-success"></i></span>'''
        else:
            '''                        <span class="icon is-large"><i class="fas fa-lg fa-times-circle has-text-danger"></i></span>'''
        print '''                    </div>
                </div>
                <!-- Right side -->
                <div class="level-right">
                    <div class="level-item has-text-centered">
                        <div>
                            <p class="heading">Choose your time period:</p>
                            <div class="tabs is-toggle is-toggle-rounded is-small">
                                <ul>
                                    <li class="is-active" id="day">
                                        <a>
                                            <span class="icon is-small"><i class="far fa-clock"></i></span>
                                            <span>1 Day</span>
                                        </a>
                                    </li>
                                    <li id="week">
                                        <a>
                                            <span class="icon is-small"><i class="fas fa-calendar"></i></span>
                                            <span>1 Week</span>
                                        </a>
                                    </li>
                                    <li id="month">
                                        <a>
                                            <span class="icon is-small"><i class="fas fa-calendar-alt"></i></span>
                                            <span>1 Month</span>
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </nav>
        </div>
    </div>
</section>
<script>
    $(document).ready(function () {
        // Check for click events on the navbar burger icon
        $("#day").click(function () {
            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            $("#day").addClass("is-active");
            $("#week").removeClass("is-active");
            $("#month").removeClass("is-active");
        });
        $("#week").click(function () {
            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            $("#day").removeClass("is-active");
            $("#week").addClass("is-active");
            $("#month").removeClass("is-active");
        });
        $("#month").click(function () {
            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            $("#day").removeClass("is-active");
            $("#week").removeClass("is-active");
            $("#month").addClass("is-active");
        });
    });
</script>'''

    @staticmethod
    def title_probe(id):
        probe_name = Display.get_anything('probe_name', 'probe', 'probe_id', id)
        probe_status = Display.get_anything('status', 'probe', 'probe_id', id)
        print '''<section class="hero is-light is-bold">
    <div class="hero-body">
        <div class="container has-text-centered">
            <!-- Main container -->
            <nav class="level">
                <!-- Left side -->
                <div class="level-left">
                    <div class="level-item">
                        <h2 class="title">
                            {}
                        </h2>'''.format(probe_name)
        if (probe_status == 0):
            print '''                        <span class="icon is-large"><i class="fas fa-lg fa-check-circle has-text-success"></i></span>'''
        else:
            '''                        <span class="icon is-large"><i class="fas fa-lg fa-times-circle has-text-danger"></i></span>'''
        print '''                    </div>
                </div>
                <!-- Right side -->
                <div class="level-right">
                    <div class="level-item has-text-centered">
                        <div>
                            <p class="heading">Choose your time period:</p>
                            <div class="tabs is-toggle is-toggle-rounded is-small">
                                <ul>
                                    <li class="is-active" id="day">
                                        <a>
                                            <span class="icon is-small"><i class="far fa-clock"></i></span>
                                            <span>1 Day</span>
                                        </a>
                                    </li>
                                    <li id="week">
                                        <a>
                                            <span class="icon is-small"><i class="fas fa-calendar"></i></span>
                                            <span>1 Week</span>
                                        </a>
                                    </li>
                                    <li id="month">
                                        <a>
                                            <span class="icon is-small"><i class="fas fa-calendar-alt"></i></span>
                                            <span>1 Month</span>
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </nav>
        </div>
    </div>
</section>
<script>
    $(document).ready(function () {
        // Check for click events on the navbar burger icon
        $("#day").click(function () {
            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            $("#day").addClass("is-active");
            $("#week").removeClass("is-active");
            $("#month").removeClass("is-active");
        });
        $("#week").click(function () {
            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            $("#day").removeClass("is-active");
            $("#week").addClass("is-active");
            $("#month").removeClass("is-active");
        });
        $("#month").click(function () {
            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            $("#day").removeClass("is-active");
            $("#week").removeClass("is-active");
            $("#month").addClass("is-active");
        });
    });
</script>'''

    @staticmethod
    def section_container_start():
        print '''<section class="section">
    <div class="container">
        <div class="columns">
            <div class="column">'''

    @staticmethod
    def section_container_end():
        print '''            </div>
        </div>
    </div>
</section>'''

    @staticmethod
    def section_container_probe_start():
        print '''<section class="section">
    <div class="container has-text-centered">
        <div class="columns is-multiline is-centered">'''

    @staticmethod
    def section_container_probe_end():
        print '''        </div>
    </div>
</section>'''

    @staticmethod
    def get_anything(query, table, where=None, id=None):
        mariadb_connection = mariadb.connect(user='root', password='root', database='project')
        cursor = mariadb_connection.cursor()
        if where:
            cursor.execute("select {} from {} where {} = '{}';".format(query, table, where, id))
        else:
            cursor.execute("select {} from {};".format(query, table))
        result = cursor.fetchone()[0]
        return result

    @staticmethod
    def get_anything_list(query, table, where=None, id=None):
        result_list = []
        mariadb_connection = mariadb.connect(user='root', password='root', database='project')
        cursor = mariadb_connection.cursor()
        if where:
            cursor.execute("select {} from {} where {} = '{}';".format(query, table, where, id))
        else:
            cursor.execute("select {} from {};".format(query, table))
        for i in cursor:
            result_list.insert(0, str(i[0]))
        return result_list

    @staticmethod
    def get_count_anything(query, table, where=None, id=None):
        mariadb_connection = mariadb.connect(user='root', password='root', database='project')
        cursor = mariadb_connection.cursor()
        if where:
            cursor.execute("select count({}) from {} where {} = '{}';".format(query, table, where, id))
        else:
            cursor.execute("select count({}) from {};".format(query, table))
        count_result = cursor.fetchone()[0]
        return count_result

    @staticmethod
    def get_service_status(configure_id):
        mariadb_connection = mariadb.connect(user='root', password='root', database='project')
        cursor = mariadb_connection.cursor()
        cursor.execute(
            "select configuration.destination, availability_service.status, availability_service.time from configuration join availability_service on configuration.configure_id = availability_service.configure_id where configuration.configure_id = {} order by availability_service.time desc limit 1;".format(
                configure_id))
        destination, status = str(cursor.fetchone()), int(cursor.fetchone()[1])
        return destination, status

    @staticmethod
    def get_speedtest(id, location):
        speedtest_ping = []
        speedtest_download = []
        speedtest_upload = []
        speedtest_time = []
        speedtest_location = location
        speedtest_probe_name = Display.get_anything('probe_name', 'probe', 'probe_id', id)
        mariadb_connection = mariadb.connect(user='root', password='root', database='project')
        cursor = mariadb_connection.cursor()
        cursor.execute(
            "select probe.probe_name, performance_service.ping, performance_service.download, performance_service.upload, performance_service.location, performance_service.time from performance_service join probe on performance_service.probe_id = probe.probe_id where probe.probe_id = '{}' and location = '{}';".format(
                id, location))
        for i in cursor:
            speedtest_ping.insert(0, i[1])
            speedtest_download.insert(0, i[2])
            speedtest_upload.insert(0, i[3])
            speedtest_time.insert(0, str(i[5]))
        return speedtest_probe_name, speedtest_ping, speedtest_download, speedtest_upload, speedtest_location, speedtest_time

    @staticmethod
    def get_probe_avg_response_time_service(configure_id):
        probe_name_list = Display.get_anything_list('probe_name', 'probe')
        destination = Display.get_anything('destination', 'configuration', 'configure_id', configure_id)
        response_time = []
        for i in probe_name_list:
            mariadb_connection = mariadb.connect(user='root', password='root', database='project')
            cursor = mariadb_connection.cursor()
            cursor.execute(
                "select probe.probe_name, round(avg(availability_service.response_time), 2) from configuration join availability_service join probe on configuration.configure_id = availability_service.configure_id where availability_service.probe_id = probe.probe_id and probe.probe_name = '{}' and configuration.configure_id = {};".format(
                    i, configure_id))
            for j in cursor:
                response_time.insert(0, j[1])
        return destination, probe_name_list, response_time

    @staticmethod
    def get_service_response_time(configure_id):
        destination = Display.get_anything('destination', 'configuration', 'configure_id', configure_id)
        datetime = []
        response_time = []
        mariadb_connection = mariadb.connect(user='root', password='root', database='project')
        cursor = mariadb_connection.cursor()
        cursor.execute(
            "select response_time, time from availability_service where configure_id = {} order by time desc;".format(
                configure_id))
        for i in cursor:
            response_time.insert(0, i[0])
            datetime.insert(0, str(i[1]))
        return destination, response_time, datetime

    @staticmethod
    def all_response_time_service_graph(configure_id):
        destination, response_time, datetime = Display.get_service_response_time(configure_id)
        print '''                <p class="subtitle">Aggregate average response time on <strong>{}</strong> from all Locations over the past 1 day</p>'''.format(
            destination)
        print '''                <div class="box">
                    <div class="chart-container" style="position: relative; height: 40vh; width: 98%;">
                        <canvas id="total_all"></canvas>
                    </div>
                    <script>
                        new Chart(document.getElementById("total_all"), {
                            type: 'line',
                            data: {'''
        print '''                                labels: {}, //list date here'''.format(datetime)
        print '''                                datasets: [{'''
        print '''                                    data: {}, //list download here'''.format(response_time)
        print '''                                    label: "Response time",
                                    borderColor: "#5F9EA0",
                                    backgroundColor: "#5F9EA0",
                                    borderWidth: 1,
                                    pointBackgroundColor: "#FFFAFA",
                                    pointBorderColor: "#5F9EA0",
                                    pointBorderWidth: 1,
                                    pointRadius: 3
                                }]
                            },
                            options: {
                                responsive: true,
                                maintainAspectRatio: false,
                                title: {
                                    display: true,
                                    text: 'Response time (ms)'
                                },
                                legend: {
                                    display: false
                                },
                                tooltips: {
                                    intersect: false
                                },
                                scales: {
                                    xAxes: [{
                                        display: true,
                                        scaleLabel: {
                                            display: true,
                                            labelString: 'Datetime'
                                        }
                                    }]
                                }
                            }
                        });
                    </script>
                </div>'''

    @staticmethod
    def display_probe():
        probe_id_list = Display.get_probe_id_list()
        probe_name_list = Display.get_probe_name_list()
        for i in range(len(probe_name_list)):
            print '''            <div class="column is-narrow is-3" id="{}">'''.format(probe_id_list[i])
            print '''                <div class="box">
                    <div class="content">
                        <h3 class="content">
                            '{}'
                        </h3>'''.format(probe_name_list[i])
            print '''                        <hr style="margin-top: -3%">
                        <p class="content">DNS Status :&nbsp;
                            <span class="icon is-small">
                                <i class="fas fa-exclamation-circle has-text-warning"></i>
                            </span>
                        </p>
                        <p class="content">Web Status :&nbsp;
                            <span class="icon is-small">
                                <i class="fas fa-times-circle has-text-danger"></i>
                            </span>
                        </p>
                        <p class="content">Mail Status :&nbsp;
                            <span class="icon is-small">
                                <i class="fas fa-check-circle has-text-success"></i>
                            </span>
                        </p>
                    </div>
                </div>
            </div>'''

    @staticmethod
    def avg_response_time_graph(configure_id):
        destination, probe_name_list, response_time = Display.get_probe_avg_response_time_service(configure_id)
        print '''                <div class="box">
                    <div id="chartContainer2" style="height: 370px; max-width: 920px; margin: 0px auto;"></div>
                    <script>
                            var chart = new CanvasJS.Chart("chartContainer2", {
                                animationEnabled: true,
                                theme: "light2", // "light1", "light2", "dark1", "dark2"
                                title: {'''
        print '''                                    text: "Average response time on {} per Location over the past 1 day",'''.format(
            destination)
        print '''                                    fontFamily: "Roboto",
                                    fontSize: 16
                                                },
                                axisY: {
                                    title: "Response time (ms)",
                                    titleFontFamily: "Roboto",
                                    titleFontSize: 14,
                                    titleFontWeight: "lighter"
                                },
                                data: [{
                                    type: "column",
                                    yValueFormatString: "#.# ms",
                                    dataPoints: ['''
        for i in range(len(probe_name_list)):
            print '''                                       {'''
            print '''                                           y: {}, label: "{}"'''.format(
                response_time[i], probe_name_list[i])
            print '''                                       },'''
        print '''                                   ]
                                }]
                            });
                            chart.render();
                    </script>
                </div>'''

    @staticmethod
    def response_time_graph(configure_id):
        destination, response_time, datetime = Display.get_service_response_time(configure_id)
        print '''<div class="box">
                    <div id="chartContainer3" style="height: 370px; max-width: 920px; margin: 0px auto;"></div>
                    <script>
                            var chart = new CanvasJS.Chart("chartContainer3", {
                                animationEnabled: true,
                                theme: "light2", // "light1", "light2", "dark1", "dark2"
                                title: {'''
        print '''                                    text: "Aggregate average response time on {} from all Locations over the past 1 day",'''.format(
            destination)
        print '''                                    fontFamily: "Roboto",
                                    fontSize: 16
                                        },
                                axisX: {
                                    valueFormatString: "D MMM, YYYY H:mm:ss",
                                    crosshair: {
                                        snapToDataPoint: true
                                    },
                                    titleFontFamily: "Roboto",
                                    titleFontSize: 14,
                                    titleFontWeight: "lighter"
                                },
                                axisY: {
                                    title: "Response time (ms)",
                                    titleFontFamily: "Roboto",
                                    titleFontSize: 14,
                                    titleFontWeight: "lighter"
                                },
                                data: [{
                                    type: "line",
                                    xValueFormatString: "D MMM, YYYY H:mm:ss",
                                    markerType: "square",
                                    yValueFormatString: "#.# ms",
                                    dataPoints: ['''
        for i in range(len(response_time)):
            print '''                                       {'''
            print '''                                           x: new Date({}), y: {}'''.format(
                datetime[i].replace(' ', ', ').replace('-', ', ').replace(':', ', '), response_time[i])
            print '''                                       },'''
        print '''                                   ]
                                }]
                            });
                            chart.render();
                    </script>
                </div>'''

    @staticmethod
    def speedtest_result_graph(id, location):
        speedtest_probe_name, speedtest_ping, speedtest_download, speedtest_upload, speedtest_location, speedtest_time = Display.get_speedtest(
            id, location)
        print '''                <div class="box">
                    <div id="chartContainer1" style="height: 370px; max-width: 920px; margin: 0px auto;"></div>
                    <script>
                            var chart = new CanvasJS.Chart("chartContainer1", {
                                animationEnabled: true,
                                theme: "light2",
                                title: {'''
        print '''                                   text: "Speedtest to {}",'''.format(speedtest_location)
        print '''                                    fontFamily: "Roboto",
                                    fontSize: 16
                                                },
                                axisX: {
                                    valueFormatString: "D MMM, YYYY H:mm:ss",
                                    crosshair: {
                                        snapToDataPoint: true
                                    },
                                    titleFontFamily: "Roboto",
                                    titleFontSize: 14,
                                    titleFontWeight: "lighter"
                                },
                                axisY: {
                                    title: "Speed (Mbps)",
                                    titleFontFamily: "Roboto",
                                    titleFontSize: 14,
                                    titleFontWeight: "lighter"
                                },
                                toolTip: {
                                    shared: true,
                                    fontFamily: "Roboto"
                                },
                                legend: {
                                    cursor: "pointer",
                                    verticalAlign: "bottom",
                                    horizontalAlign: "left",
                                    dockInsidePlotArea: true,
                                    itemclick: toogleDataSeries
                                },
                                data: [{
                                    type: "line",
                                    showInLegend: true,
                                    name: "Download",
                                    markerType: "square",
                                    xValueFormatString: "D MMM, YYYY H:mm:ss",
                                    yValueFormatString: "#.# Mbps",
                                    color: "#F08080",
                                    dataPoints: ['''
        for i in range(len(speedtest_ping)):
            print '''                                       {'''
            print '''                                           x: new Date({}), y: {}'''.format(
                speedtest_time[i].replace(' ', ', ').replace('-', ', ').replace(':', ', '), speedtest_download[i])
            print '''                                       },'''
        print '''                                   ]
                                },
                                {
                                    type: "line",
                                    showInLegend: true,
                                    name: "Upload",
                                    lineDashType: "dash",
                                    yValueFormatString: "#.# Mbps",
                                    dataPoints: ['''
        for i in range(len(speedtest_ping)):
            print '''                                       {'''
            print '''                                           x: new Date({}), y: {}'''.format(
                speedtest_time[i].replace(' ', ', ').replace('-', ', ').replace(':', ', '), speedtest_upload[i])
            print '''                                       },'''
        print '''                                   ]
                                }]
                            });
                            chart.render();
                            function toogleDataSeries(e) {
                                if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
                                    e.dataSeries.visible = false;
                                } else {
                                    e.dataSeries.visible = true;
                                }
                                chart.render();
                            }
                    </script>
                </div>'''


content = Display()
content.header()
content.nav_bar()
# content.title_service(1)
content.title_probe('a2999bffbb046ced')
# content.section_container_probe_start()
content.section_container_start()
# content.display_probe()
content.avg_response_time_graph(1)
content.response_time_graph(1)
# content.speedtest_result_graph('a2999bffbb046ced', 'Singapore')
# content.avg_response_time_service_graph(3)
# content.all_response_time_service_graph(3)
# content.section_container_probe_end()
content.section_container_end()
content.footer()
