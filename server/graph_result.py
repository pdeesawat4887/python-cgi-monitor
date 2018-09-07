#!/usr/bin/python
# import mysql.connector as mariadb
import main.database as mariadb
import cgi

print '''Content-type: text/html\n'''


def performance_result(probe_id, service_type, range_day):
    probe_name = get_probe_info(probe_id)[0]
    list_performance = get_list_performance_service(service_type)
    for item in list_performance:
        performance_item, ping, download, upload, time = get_performance_result(
            probe_id, service_type, item, range_day)
        if (len(performance_item.split('.')) > 1):
            tmp = performance_item
            if (tmp.split('.')[1] == 'youtube'):
                performance_item = tmp.split('.')[1]
                id_video = tmp.split('.')[2].split('?')[1].split('=')[1].replace('-', '')
            elif (tmp.split('.')[1] == 'pornhub'):
                performance_item = tmp.split('.')[1]
                id_video = tmp.split('.')[3].split('?')[1].split('=')[1]
            elif (tmp.split('.')[1] == 'dailymotion'):
                performance_item = tmp.split('.')[1]
                id_video = tmp.split('.')[2].split('/')[2]
            elif (tmp.split('.')[0].split('/')[2] == 'vimeo'):
                performance_item = tmp.split('.')[0].split('/')[2]
                id_video = tmp.split('.')[1].split('/')[1]
        else:
            performance_item = performance_item.replace(' ', '')
            id_video = None
        print '''        <section class="section" id="performance_graph" style="margin-bottom: -30px;">
            <div class="container has-text-centered">
                <div class="columns is-centered">
                    <div class="column is-10">
                        <div class="box" style="background-color: #e5e6e4">'''
        print '''                            <div id="{}" style="height: 370px; width: 99%; margin: 0px auto;"></div>'''.format(
            service_type + '_' + performance_item.lower() + '_' + id_video if id_video else service_type + '_' + performance_item.lower())
        print '''                            <script>'''
        print '''                                var chart_{} = new CanvasJS.Chart("{}",'''.format(
            service_type + '_' + performance_item.lower() + '_' + id_video if id_video else service_type + '_' + performance_item.lower(),
            service_type + '_' + performance_item.lower() + '_' + id_video if id_video else service_type + '_' + performance_item.lower())
        print '''                                    {
                                        animationDuration: 800,
                                        animationEnabled: true,
                                        zoomEnabled: true,
                                        theme: "light2",
                                        backgroundColor: "#e5e6e4",
                                        title: {
                                            fontFamily: "Roboto",
                                            fontSize: 20,'''
        print '''                                            text: "Performance Result from {} to {} in {} day(s)"'''.format(
            probe_name,
            performance_item.upper() + ' (Video ID: ' + id_video + ')' if id_video else performance_item.upper(),
            range_day)
        print '''                                        },
                                        axisX: {
                                            labelMaxWidth: 75,
                                            labelFontFamily: "Roboto",
                                            labelFontWeight: "normal",
                                            valueFormatString: "D MMM, YYYY H:mm:ss",
                                            crosshair: {
                                                enabled: true,
                                                snapToDataPoint: true,
                                                label: ""
                                            }
                                        },
                                        axisY: {
                                            labelFontFamily: "Roboto",
                                            labelFontWeight: "normal",
                                            includeZero: false
                                        },
                                        legend: {
                                            fontFamily: "Roboto",
                                            fontWeight: "lighter",
                                            verticalAlign: "top",
                                            horizontalAlign: "right",
                                            cursor: "pointer",
                                            dockInsidePlotArea: true,
                                            itemclick: toogleDataSeries
                                        },
                                        toolTip: {
                                            shared: true,
                                            borderColor: "#17202a",
                                            fontFamily: "Roboto",
                                            fontWeight: "lighter"
                                        },
                                        subtitles: [{
                                            fontFamily: "Roboto",
                                            text: "Speed in Mbps"
                                        }],
                                        data: [{
                                            name: "Download",
                                            type: "spline",
                                            xValueFormatString: "D MMM, YYYY H:mm:ss",
                                            indexLabelFontFamily: "Roboto",
                                            markerType: "circle",
                                            showInLegend: true,
                                            dataPoints: ['''
        if performance_item:
            for i in range(len(ping)):
                date = time[i].split(' ')[0].split('-')
                times = time[i].split(' ')[1].split(':')
                year = int(date[0])
                month = int(date[1]) - 1
                day = int(date[2])
                hour = int(times[0])
                minute = int(times[1])
                second = int(times[2])
                print '''                                                {'''
                print '''                                                    x: new Date({}, {}, {}, {}, {}, {}), y: {}'''.format(
                    year, month, day, hour, minute, second, download[i])
                if (i == len(ping) - 1):
                    print '''                                                }'''
                else:
                    print '''                                                },'''
            print '''                                            ]
                                        },'''
        if (service_type == 'speedtest'):
            print '''                                        {
                                            name: "Upload",
                                            type: "spline",
                                            indexLabelFontFamily: "Roboto",
                                            markerType: "circle",
                                            showInLegend: true,
                                            dataPoints: ['''
            for i in range(len(ping)):
                date = time[i].split(' ')[0].split('-')
                times = time[i].split(' ')[1].split(':')
                year = int(date[0])
                month = int(date[1]) - 1
                day = int(date[2])
                hour = int(times[0])
                minute = int(times[1])
                second = int(times[2])
                print '''                                                {'''
                print '''                                                    x: new Date({}, {}, {}, {}, {}, {}), y: {}'''.format(
                    year, month, day, hour, minute, second, upload[i])
                if (i == len(ping) - 1):
                    print '''                                                }'''
                else:
                    print '''                                                },'''
            print '''                                            ]
                                        }'''
        print '''                                        ]
                                    });'''
        print '''                                chart_{}.render();'''.format(
            service_type + '_' + performance_item.lower() + '_' + id_video if id_video else service_type + '_' + performance_item.lower())
        print '''                                function toogleDataSeries(e) {
                                    if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
                                        e.dataSeries.visible = false;
                                    } else {
                                        e.dataSeries.visible = true;
                                    }'''
        print '''                                    chart_{}.render();'''.format(
            service_type + '_' + performance_item.lower() + '_' + id_video if id_video else service_type + '_' + performance_item.lower())
        print '''                                }
                            </script>
                        </div>
                    </div>
                </div>
            </div>
        </section>'''


def availability_result(probe_id, service_type, range_day):
    probe_name = get_probe_info(probe_id)[0]
    list_availability = get_list_availability_service(service_type)
    print '''        <section class="section" id="availability_graph">
            <div class="container has-text-centered">
                <div class="columns is-multiline is-centered">
                    <div class="column is-10">
                        <div class="box" style="background-color: #e5e6e4">
                            <div id="avg_responsetime" style="height: 370px; width: 99%; margin: 0px auto;"></div>
                            <script>
                                var chart_avg_responsetime = new CanvasJS.Chart("avg_responsetime",
                                    {
                                        animationDuration: 800,
                                        animationEnabled: true,
                                        zoomEnabled: true,
                                        theme: "light2",
                                        backgroundColor: "#e5e6e4",
                                        title: {
                                            fontFamily: "Roboto",
                                            fontSize: 20,'''
    print '''                                            text: "Average response time from {} to {} Service(s) in {} day(s)"'''.format(
        probe_name, service_type.upper(), range_day)
    print '''                                        },
                                        axisX: {
                                            labelFontFamily: "Roboto",
                                            labelFontWeight: "normal",
                                            //valueFormatString: "D MMM, YYYY H:mm:ss",
                                            interval: 1,
                                            crosshair: {
                                                //enabled: true,
                                                snapToDataPoint: true,
                                                //label: ""
                                            }
                                        },
                                        axisY: {
                                            labelFontFamily: "Roboto",
                                            labelFontWeight: "normal",
                                            minimum: 0,
                                            viewportMinimum: 0,
                                            includeZero: true
                                        },
                                        legend: {
                                            fontFamily: "Roboto",
                                            fontWeight: "lighter",
                                            verticalAlign: "top",
                                            horizontalAlign: "right",
                                            cursor: "pointer",
                                            dockInsidePlotArea: true
                                        },
                                        toolTip: {
                                            shared: true,
                                            content: "{name}: {y} ms",
                                            borderColor: "#17202a",
                                            fontFamily: "Roboto",
                                            fontWeight: "lighter"
                                        },
                                        dataPointWidth: 10,
                                        subtitles: [{
                                            fontFamily: "Roboto",
                                            text: "Response Time in ms"
                                        }],
                                        data: [{
                                            name: "Response time",
                                            type: "bar",
                                            xValueType: "number",
                                            indexLabelFontFamily: "Roboto",
                                            markerType: "circle",
                                            showInLegend: false,
                                            dataPoints: ['''
    for item in range(len(list_availability)):
        destination_name = list_availability[item]
        average_responsetime = get_availability_result(probe_id, service_type, destination_name, range_day)
        print '''                                                {'''
        print '''                                                    y: {}, label: "{}", color: "{}"'''.format(
            average_responsetime, destination_name,
            '#2E8B57' if average_responsetime < 100 else '#FF8C00' if average_responsetime < 1000 else '#B22222')
        if (item == len(list_availability) - 1):
            print '''                                                }'''
        else:
            print '''                                                },'''
    print '''                                            ]
                                        }]
                                    });
                                chart_avg_responsetime.render();
                            </script>
                        </div>
                    </div>
                </div>
            </div>
        </section>'''


def get_probe_info(probe_id):
    # mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
    #                                      host='192.168.254.31')
    # cursor = mariadb_connection.cursor()
    # cursor.execute("select probe_name, ip_address, mac_address,`status` from probe where probe_id = '{}';".format(probe_id))
    # probe_info = cursor.fetchone()
    db = mariadb.MySQLDatabase()
    db.mycursor.execute(
        "select probe_name, ip_address, mac_address,`status` from probe where probe_id = '{}';".format(probe_id))
    probe_info = db.mycursor.fetchone()
    return probe_info


def get_list_performance_service(service_type):
    # mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
    #                                      host='192.168.254.31')
    # cursor = mariadb_connection.cursor()
    # if (service_type == 'speedtest'):
    #     cursor.execute(
    #         "select distinct performance_service.location from service join destination join performance_service join running_service on service.service_id = running_service.service_id and service.service_id = destination.service_id and destination.destination_id = performance_service.destination_id where service.service_name = '{}' and performance_service.download != 0;".format(
    #             service_type))
    # else:
    #     cursor.execute(
    #         "select distinct destination.destination from service join destination join performance_service join running_service on service.service_id = running_service.service_id and service.service_id = destination.service_id and destination.destination_id = performance_service.destination_id where service.service_name = '{}' and performance_service.download != 0;".format(
    #             service_type))
    # for i in cursor:
    #     if (i[0] != 'NULL'):
    #         list_location.insert(0, i[0])
    list_location = []
    db = mariadb.MySQLDatabase()
    if (service_type == 'speedtest'):
        db.mycursor.execute(
            "select distinct performance_service.location from service join destination join performance_service join running_service on service.service_id = running_service.service_id and service.service_id = destination.service_id and destination.destination_id = performance_service.destination_id where service.service_name = '{}' and performance_service.download != 0;".format(
                    service_type))
    else:
        db.mycursor.execute(
            "select distinct destination.destination from service join destination join performance_service join running_service on service.service_id = running_service.service_id and service.service_id = destination.service_id and destination.destination_id = performance_service.destination_id where service.service_name = '{}' and performance_service.download != 0;".format(
                service_type))
    for i in db.mycursor:
        if (i[0] != 'NULL'):
            list_location.insert(0, i[0])
    return list_location


def get_list_availability_service(service_type):
    # mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
    #                                      host='192.168.254.31')
    # cursor = mariadb_connection.cursor()
    # cursor.execute(
    #     "select distinct destination.destination from destination join service join availability_service join running_service on service.service_id = running_service.service_id and destination.service_id = service.service_id and destination.destination_id = availability_service.destination_id where service.service_name = '{}' and availability_service.status = 0;".format(
    #         service_type))
    # for i in cursor:
    #     if (i[0] != 'NULL'):
    #         list_destination.insert(0, i[0])
    list_destination = []
    db = mariadb.MySQLDatabase()
    db.mycursor.execute("select distinct destination.destination from destination join service join availability_service join running_service on service.service_id = running_service.service_id and destination.service_id = service.service_id and destination.destination_id = availability_service.destination_id where service.service_name = '{}' and availability_service.status = 0;".format(
            service_type))
    for i in db.mycursor:
        if (i[0] != 'NULL'):
            list_destination.insert(0, i[0])
    return list_destination


def get_availability_result(probe_id, service_type, availability_item, day):
    # mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
    #                                      host='192.168.254.31')
    # cursor = mariadb_connection.cursor()
    # cursor.execute(
    #     "select round(avg(availability_service.response_time), 2) from availability_service join destination join service join probe on availability_service.destination_id = destination.destination_id and availability_service.probe_id = probe.probe_id and destination.service_id = service.service_id where availability_service.probe_id = '{}' and service.service_name = '{}' and destination.destination = '{}' and availability_service.status = 0 and availability_service.time >= now() + interval  - {} day and availability_service.time < now() + interval 0 day;".format(
    #         probe_id, service_type, availability_item, day))
    # average_responsetime = cursor.fetchone()[0]
    db = mariadb.MySQLDatabase()
    db.mycursor.execute(
        "select round(avg(availability_service.response_time), 2) from availability_service join destination join service join probe on availability_service.destination_id = destination.destination_id and availability_service.probe_id = probe.probe_id and destination.service_id = service.service_id where availability_service.probe_id = '{}' and service.service_name = '{}' and destination.destination = '{}' and availability_service.status = 0 and availability_service.time >= now() + interval  - {} day and availability_service.time < now() + interval 0 day;".format(
            probe_id, service_type, availability_item, day))
    average_responsetime = db.mycursor.fetchone()[0]
    return average_responsetime


def get_performance_result(probe_id, service_type, performance_item, range_day):
    # mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
    #                                      host='192.168.254.31')
    # cursor = mariadb_connection.cursor()
    # if (service_type == 'speedtest'):
    #     cursor.execute(
    #         "select performance_service.ping, performance_service.download, performance_service.upload, performance_service.time from performance_service join destination join service join probe on performance_service.destination_id = destination.destination_id and performance_service.probe_id = probe.probe_id and destination.service_id = service.service_id where probe.probe_id = '{}' and service.service_name = '{}' and performance_service.location = '{}' and performance_service.download != 0 and performance_service.time >= now() + interval  - {} day and performance_service.time < now() + interval 0 day;".format(
    #             probe_id, service_type, performance_item, range_day))
    # else:
    #     cursor.execute(
    #         "select performance_service.ping, performance_service.download, performance_service.upload, performance_service.time from performance_service join destination join service join probe on performance_service.destination_id = destination.destination_id and performance_service.probe_id = probe.probe_id and destination.service_id = service.service_id where probe.probe_id = '{}' and service.service_name = '{}' and destination.destination = '{}' and performance_service.download != 0 and performance_service.time >= now() + interval  - {} day and performance_service.time < now() + interval 0 day;".format(
    #             probe_id, service_type, performance_item, range_day))
    # for i in cursor:
    #     ping.insert(0, i[0])
    #     download.insert(0, i[1])
    #     upload.insert(0, i[2])
    #     time.insert(0, str(i[3]))
    # return performance_item, ping, download, upload, time
    performance_item = performance_item
    ping = []
    download = []
    upload = []
    time = []
    db = mariadb.MySQLDatabase()
    if (service_type == 'speedtest'):
        db.mycursor.execute(
            "select performance_service.ping, performance_service.download, performance_service.upload, performance_service.time from performance_service join destination join service join probe on performance_service.destination_id = destination.destination_id and performance_service.probe_id = probe.probe_id and destination.service_id = service.service_id where probe.probe_id = '{}' and service.service_name = '{}' and performance_service.location = '{}' and performance_service.download != 0 and performance_service.time >= now() + interval  - {} day and performance_service.time < now() + interval 0 day;".format(
                    probe_id, service_type, performance_item, range_day))
    else:
        db.mycursor.execute(
            "select performance_service.ping, performance_service.download, performance_service.upload, performance_service.time from performance_service join destination join service join probe on performance_service.destination_id = destination.destination_id and performance_service.probe_id = probe.probe_id and destination.service_id = service.service_id where probe.probe_id = '{}' and service.service_name = '{}' and destination.destination = '{}' and performance_service.download != 0 and performance_service.time >= now() + interval  - {} day and performance_service.time < now() + interval 0 day;".format(
                probe_id, service_type, performance_item, range_day))
    for i in db.mycursor:
            ping.insert(0, i[0])
            download.insert(0, i[1])
            upload.insert(0, i[2])
            time.insert(0, str(i[3]))
    return performance_item, ping, download, upload, time




# performance_result('ba27ebfffe15598a', 'video', '1')
# availability_result('ba27ebfffe15598a', 'website', '1')

form = cgi.FieldStorage()
data = form.getvalue('data')
tmp = data.split('_')
probe_id = tmp[0]
service_type = tmp[1]
range_day = tmp[2]

if (service_type == 'speedtest' or service_type == 'video'):
    performance_result(probe_id, service_type, range_day)
else:
    availability_result(probe_id, service_type, range_day)
