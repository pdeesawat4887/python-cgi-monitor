from reportlab.graphics.charts import utils
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.textlabels import Label
from reportlab.lib.colors import PCMYKColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, mm
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, PageBreak, Image, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import main.database as mariadb
from reportlab.lib import utils
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from reportlab.lib.validators import Auto
from random import randint
import time
import datetime

class PDFCreation:

    def __init__(self, table, file_name, logo):
        self.tab = "&nbsp;&nbsp;&nbsp;&nbsp;"
        self.master_font = "Times-Roman"
        self.styles = getSampleStyleSheet()
        self.table = table
        self.file_name = file_name
        self.logo = logo
        self.db = mariadb.MySQLDatabase()
        self.flowables = []
        self.create_pdf()


    def create_pdf(self):
        self.doc = SimpleDocTemplate(self.file_name,
                                     pagesize=A4,
                                     rightMargin=20,
                                     leftMargin=30,
                                     topMargin=50,
                                     bottomMargin=18, )
        self.sp_header = ParagraphStyle('parrafos',
                                        alignment=TA_LEFT,
                                        fontSize=18,
                                        fontName="Times-Roman",
                                        leading=50)
        self.sp_left = ParagraphStyle('parrafos',
                                      alignment=TA_LEFT,
                                      fontSize=12,
                                      fontName="Times-Roman",
                                      leading=20)

        self.sp_topic = ParagraphStyle('parrafos',
                                            alignment=TA_LEFT,
                                            fontSize=12,
                                            fontName="Times-Roman",
                                            leading=16)

        self.sp_small_topi = ParagraphStyle('parrafos',
                                      alignment=TA_LEFT,
                                      fontSize=10,
                                      fontName="Times-Roman",
                                      leading=16)
        self.create_header()
        self.create_body()

        self.doc.build(self.flowables, onFirstPage=self.add_page_number, onLaterPages=self.add_page_number)

    def break_part(self, line):
        blank = Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;", style=self.sp_left)
        for row in range(int(line)):
            self.flowables.append(blank)

    def get_image(self, path, width=1*cm):
        img = utils.ImageReader(path)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        return Image(path, width=width, height=(width * aspect))

    def create_header(self):
        self.flowables.append(self.get_image(path=self.logo, width=5*cm))
        self.break_part(1)
        self.flowables.append(Paragraph("NETWORK ACTIVE MONITORING SYSTEM REPORT", style=self.sp_header))
        self.flowables.append(Paragraph(
            "<strong>DATE:</strong>&nbsp;&nbsp;&nbsp;&nbsp;{date}".format(date=time.strftime("%A %d %B %Y")),
            style=self.sp_left))
        self.flowables.append(
            Paragraph("<strong>REPORT TOPIC:</strong>&nbsp;&nbsp;&nbsp;&nbsp;{topic}".format(topic=self.table.upper()),
                      style=self.sp_left))

    def create_body(self):
        pass

    # def create_table(self, length, data, align, row_height=24):
    #     row = len(data) - 1
    #     column = len(data[0]) - 1
    #     table = Table(data, colWidths=length, rowHeights=row_height, hAlign=align)
    #     table.setStyle(TableStyle([('ALIGN', (0, 0), (column, row), 'CENTER'),
    #                                ('VALIGN', (0, 0), (column, row), 'MIDDLE'),
    #                                ('FONTSIZE', (0, 0), (column, row), 8),
    #                                ('INNERGRID', (0, 0), (column, row), 0.25, colors.black),
    #                                ('BOX', (0, 0), (column, row), 0.25, colors.black),
    #                                ('TEXTCOLOR', (0, 0), (column, row), colors.black), ]))
    #     return table

    def get_style(self):
        styles = getSampleStyleSheet()
        style = styles["Normal"]
        style.fontSize = 7
        style.fontName = "Times-Roman"
        style.alignment=TA_CENTER
        return style

    def create_pie_chart(self, data_list, label_list, user_color=None):

        label_list = map(lambda item: item.upper(), label_list)

        data = [(item / (sum(data_list) * 1.0)) * 100 for item in data_list]

        if user_color != None:
            usage_color = user_color
        else:
            random_range = [randint(0, 100) for i in range(len(data_list))]
            usage_color = map(lambda item: PCMYKColor(randint(0, item), randint(0, item), randint(0, item), randint(0, item)), random_range)
            print user_color

        d = Drawing()
        pie = Pie()
        pie.x = 200
        pie.y = 85
        pie.data = data
        pie.labels = label_list

        for i, color in enumerate(usage_color):
            pie.slices[i].fillColor = color

        pie.slices.strokeWidth = 0.5
        pie.slices.popout = 1.5
        pie._seriesCount = 3
        pie.sideLabels = 1

        legend = Legend()
        legend.alignment = 'right'
        legend.x = 0
        legend.y = 75
        legend.colorNamePairs = [(z, (x, '     {val:.2f}%'.format(val=y))) for x, y, z in zip(pie.labels, data, usage_color)]
        d.add(legend)
        d.add(pie)

        self.flowables.append(d)

    def prepare_data_table(self, sql):

        result_all = self.db.select(sql)
        description = [field[0] for field in self.db.mycursor.description]

        result_all = map(lambda item: map(lambda inner: Paragraph(str(inner), style=self.get_style()) if inner != None else '-', item), result_all)
        description_re = map(lambda item: Paragraph("<strong>{desc}</strong>".format(desc=str(item)), style=self.get_style()), description)
        result_all.insert(0, description_re)

        return result_all

    def create_table_with_sql(self, sql, max_width=530, max_height=16):
        output = self.prepare_data_table(sql)

        row = len(output) - 1
        column = len(output[0]) - 1

        width = [max_width/len(output[0]) for i in range(len(output))]
        height = [max_height for i in range(len(output))]

        table = Table(output, colWidths=width, rowHeights=height, hAlign='CENTER')
        table.setStyle(TableStyle([('ALIGN', (0, 0), (column, row), 'CENTER'),
                                   ('VALIGN', (0, 0), (column, row), 'MIDDLE'),
                                   ('FONTSIZE', (0, 0), (column, row), 8),
                                   ('INNERGRID', (0, 0), (column, row), 0.25, colors.black),
                                   ('BOX', (0, 0), (column, row), 0.25, colors.black),
                                   ('TEXTCOLOR', (0, 0), (column, row), colors.black), ]))

        self.flowables.append(table)

    # def before_table_log(self, table):
    #     log_sql = "SELECT `event_type`, count(`logging_id`) AS 'record' FROM LOGGING_EVENTS WHERE `event_table`='{tlb}' GROUP BY `event_type`;".format(tlb=table.upper())
    #     log_result = self.db.select(log_sql)
    #
    #     if not log_result:
    #         self.flowables.append(Paragraph("<strong>EMPTY LOGGING</strong>", style=self.sp_small_topi))
    #     else:
    #         map(lambda item: self.flowables.append(Paragraph("<strong>{main} Logging:</strong>{tab}{val} record(s)".format(tab=self.tab, main=item[0].capitalize(), val=item[1]), style=self.sp_left)), log_result)

    def add_page_number(self, canvas, doc):
        """
        Add the page number
        """
        page_num = canvas.getPageNumber()
        text = "%s" % page_num
        canvas.drawRightString(195*mm, 280*mm, text)

    def create_bar(self, data_list, label_x_axis, contain, y_label=None, x_label=None, bar_width=520, bar_height=100,
                   draw_width=520, draw_height=200, user_color=None, fontName="Times-Roman", fontSize=6, x_angle=0, bar_space=0):

        d = Drawing(width=draw_width, height=draw_height)
        bar = VerticalBarChart()
        bar.width=bar_width
        bar.height=bar_height
        bar.y = bar.height-(bar_height/4)
        bar.strokeColor = colors.black
        bar.barLabelFormat = '%s'
        bar.barLabels.nudge = 7
        bar.barLabels.fontSize = fontSize

        ################# X AXIS PROPERTIES #################
        bar.categoryAxis.labels.dx = 0
        bar.categoryAxis.labels.angle = x_angle
        bar.categoryAxis.labels.boxAnchor = 'autox'
        bar.categoryAxis.labels.fontSize = fontSize
        bar.categoryAxis.labels.fontName = self.master_font
        bar.categoryAxis.strokeWidth = 0.25
        bar.categoryAxis.tickDown = -(bar.height)
        bar.categoryAxis.categoryNames = label_x_axis

        labX = Label()
        labX.boxAnchor = 'ne'
        labX.dx = bar.width * 2.15
        labX.dy = bar.height
        labX.fontName = fontName
        labX.fontSize = fontSize
        labX.setText(x_label)
        d.add(labX)
        #####################################################

        ################# Y AXIS PROPERTIES #################
        bar.valueAxis.forceZero = 1
        bar.valueAxis.labels.fontSize = fontSize
        bar.valueAxis.labels.fontName = fontName
        bar.valueAxis.rangeRound = 'both'
        bar.valueAxis.valueMin = 0
        bar.valueAxis.visibleGrid = 1
        bar.valueAxis.visibleAxis = 1
        bar.valueAxis.labels.dx = -10

        labY = Label()
        labY.boxAnchor = 'autox'
        labY.dy = bar.y+(bar.height/1.5)
        labY.dx = bar.x-30
        labY.angle = 90
        labY.fontName = fontName
        labY.fontSize = fontSize
        labY.setText(y_label)
        d.add(labY)
        #####################################################

        bar.barSpacing = bar_space
        # bar.groupSpacing = 3

        bar.data = data_list

        if user_color != None:
            usage_color = user_color
        else:
            random_range = [randint(0, 100) for i in range(len(contain))]
            usage_color = map(lambda item: PCMYKColor(randint(0, item), randint(0, item), randint(0, item), randint(0, item)), random_range)

        for i in range(len(data_list)):
            bar.bars[i].name = contain[i].upper()
            bar.bars[i].fillColor = usage_color[i]

        legend = Legend()
        legend.alignment = 'right'
        legend.boxAnchor = 'sw'
        legend.dxTextSpace = 10
        legend.fontSize = fontSize
        legend.fontName = fontName
        legend.subCols.minWidth = 55
        legend.variColumn = 1
        legend.deltay = 15
        legend.x = bar.x
        legend.colorNamePairs = Auto(obj=bar)

        d.add(bar)
        d.add(legend)
        self.flowables.append(d)

class PDFProbe(PDFCreation):

    def get_fk_cluster_information(self, status):

        happy = []
        x_axis = []

        sql_query_pb = """SELECT `probe_name`, (SELECT `cluster_id` FROM CLUSTERS WHERE CLUSTERS.probe_id=PROBES.probe_id) FROM PROBES WHERE `probe_status`='{status}'"""
        output_probe = self.db.select(sql_query_pb.format(status=status))

        all_svc = self.db.select("SELECT `service_id`, `service_name` FROM SERVICES")

        count = "SELECT COUNT(`result_id`) FROM TESTRESULTS WHERE `service_id`={isvc} and `cluster_id`={iclus};"

        for item in all_svc:
            x_axis.append(item[1])
            happy.append(tuple(
                map(lambda val: self.db.select(count.format(isvc=item[0], iclus=val[1]))[0][0] if val[1] != None else 0,
                    output_probe)))

        x_axis_probe = map(lambda item: item[0], output_probe)
        val = map(lambda item: sum(item), happy)

        if sum(val) != 0:
            self.create_bar(happy, x_axis_probe, x_axis)
        self.break_part(1)

    def create_body(self):
        sql_status = """SELECT `probe_name` AS 'Probe Name', `ip_address` AS 'IP Address', `mac_address` AS 'MAC Address'
                      , DATE_FORMAT(`date_added`, '%d-%b-%Y') AS 'Installed Date', DATE_FORMAT(`last_updated`, '%d-%b-%Y %H:%m:%s') AS 'Last Updated Date'
                      , DATEDIFF(`last_updated`,`date_added`) as 'Uptime (day)'
                      , (SELECT COUNT(`result_id`) FROM TESTRESULTS WHERE `cluster_id`= (SELECT `cluster_id` FROM CLUSTERS WHERE PROBES.probe_id=CLUSTERS.probe_id AND `result_status`=1)) AS 'Pass Test (time)'
                      , (SELECT COUNT(`result_id`) FROM TESTRESULTS WHERE `cluster_id`= (SELECT `cluster_id` FROM CLUSTERS WHERE PROBES.probe_id=CLUSTERS.probe_id AND `result_status`=2)) AS 'Fail Test (time)'
                      , (SELECT COUNT(`result_id`) FROM TESTRESULTS WHERE `cluster_id`= (SELECT `cluster_id` FROM CLUSTERS WHERE PROBES.probe_id=CLUSTERS.probe_id AND `result_status`=3)) AS 'Error Test (time)'
                      , (SELECT COUNT(`result_id`) FROM TESTRESULTS WHERE `cluster_id`= (SELECT `cluster_id` FROM CLUSTERS WHERE PROBES.probe_id=CLUSTERS.probe_id)) AS 'Total Test (time)'
                      FROM PROBES WHERE `probe_status`='{status}' ORDER BY `probe_name` ASC;"""
        sql_count = "SELECT COUNT(`probe_id`) FROM PROBES WHERE `probe_status`='{status}';"
        probe_status = {
            'Active': ('Ready to work and still working now.', 'green', colors.lawngreen),
            'Idle': ('Ready to work, but NOT working until change status to ACTIVE.', 'gray', colors.gray),
            'Inactive': ('Cannot connected to probe longer than 1 hour.', 'red', colors.red)
        }

        probe_type_count = map(lambda item: self.db.select(sql_count.format(status=item))[0][0], probe_status)

        ################################################################################################################
        self.flowables.append(Paragraph("<strong>COLLECT PROBE INFORMATION WITH STATUS:</strong>", style=self.sp_left))
        map(lambda stat, val: self.flowables.append(Paragraph("{val}. {status}:{tab}{desc}".format(val=val, status=str(stat).upper(), tab=self.tab, desc=probe_status[stat][0]), style=self.sp_small_topi)), probe_status, [i for i in range(1, len(probe_status)+1)])
        self.break_part(1)
        ################################################################################################################
        self.flowables.append(Paragraph("<strong>PROBE STATUS CHART</strong>", style=self.sp_topic))
        self.flowables.append(self.create_pie_chart(data_list=probe_type_count, label_list=[protocol.upper() for protocol in probe_status], user_color=[ probe_status[i][2] for i in probe_status]))
        ################################################################################################################
        self.flowables.append(Paragraph("<strong>SUMMARY TEST RESULT EACH PROBE</strong>", style=self.sp_topic))
        self.break_part(1)
        map(lambda item: self.get_fk_cluster_information(status=item), probe_status)
        ################################################################################################################

        self.flowables.append(PageBreak())

        ################################################################################################################
        self.flowables.append(Paragraph("<strong>SUMMARY PROBE INFORMATION WITH TEST RESULT</strong>", style=self.sp_topic))
        self.break_part(1)
        for status,value in zip(probe_status, probe_type_count):
            self.flowables.append(Paragraph("TOTAL<font color='{color}'> {status}</font> PROBE:{tab}{val} PROBE(S)".format(color=probe_status[status][1], status=status.upper(), tab=self.tab, val=value), style=self.sp_left))
            self.create_table_with_sql(sql_status.format(status=status), max_height=30)
            self.break_part(1)
        ################################################################################################################

class PDFService(PDFCreation):

    def create_body_destination(self):
        self.flowables.append(
            Paragraph("<strong>REPORT TOPIC:</strong{tab}{topic}".format(tab=self.tab, topic='DESTINATION'), style=self.sp_left))

        sql_condition = """SELECT `destination_name` AS 'Destination', `destination_port` AS 'Port'
                                        , (SELECT `service_name` FROM SERVICES WHERE SERVICES.service_id=DESTINATIONS.service_id) AS 'Service Name', `destination_description` AS 'Description'
                                        , (SELECT COUNT(`result_id`) FROM TESTRESULTS WHERE result_status=1 AND TESTRESULTS.destination_id=DESTINATIONS.destination_id) AS 'Pass Test (time)'
                                        , (SELECT COUNT(`result_id`) FROM TESTRESULTS WHERE result_status=2 AND TESTRESULTS.destination_id=DESTINATIONS.destination_id) AS 'Fail Test (time)'
                                        , (SELECT COUNT(`result_id`) FROM TESTRESULTS WHERE result_status=3 AND TESTRESULTS.destination_id=DESTINATIONS.destination_id) AS 'Error Test (time)'
                                        , (SELECT COUNT(`result_id`) FROM TESTRESULTS WHERE TESTRESULTS.destination_id=DESTINATIONS.destination_id) AS 'Total Test (time)'
                                        FROM DESTINATIONS WHERE `service_id`=(SELECT `service_id` FROM SERVICES WHERE SERVICES.`service_name`='{svc}') ORDER BY `service_id` ASC"""
        self.flowables.append(Paragraph("<strong>TOTAL SERVICE RATIO</strong>", style=self.sp_topic))
        dest_label, dest_data = self.get_destination_type()

        self.flowables.append(Paragraph("<strong>SUMMARY DESTINATION INFORMATION</strong>", style=self.sp_topic))
        self.break_part(1)
        for svc, val in zip(dest_label, dest_data):
            self.flowables.append(Paragraph(
                "TOTAL DESTINATION(S) IN{tab}<strong>{svc}</strong>:{tab}{val} destination(s).".format(tab=self.tab,
                                                                                                       svc=svc.capitalize(),
                                                                                                       val=val),
                style=self.sp_small_topi))
            self.create_table_with_sql(sql_condition.format(svc=svc))
            self.break_part(1)

        running_dest = """SELECT (SELECT `probe_name` FROM PROBES WHERE PROBES.probe_id=(SELECT `probe_id` FROM CLUSTERS WHERE CLUSTERS.cluster_id=RUNNING_DESTINATIONS.cluster_id)) AS 'Probe Name'
                                        , (SELECT `destination_name` FROM DESTINATIONS WHERE RUNNING_DESTINATIONS.destination_id=DESTINATIONS.destination_id) AS 'Destination Name'
                                        , (SELECT `destination_port` FROM DESTINATIONS WHERE RUNNING_DESTINATIONS.destination_id=DESTINATIONS.destination_id) AS 'Port'
                                        , (SELECT `destination_description` FROM DESTINATIONS WHERE RUNNING_DESTINATIONS.destination_id=DESTINATIONS.destination_id) AS 'Description'
                                        ,`running_dest_status` AS 'Status' FROM RUNNING_DESTINATIONS;"""
        self.flowables.append(Paragraph("<strong>SUMMARY DESTINATION STATUS</strong>", style=self.sp_topic))
        self.break_part(1)
        self.create_table_with_sql(running_dest)

        self.break_part(1)

        test_result = """SELECT (SELECT `probe_name` FROM PROBES WHERE PROBES.probe_id=(SELECT `probe_id` FROM CLUSTERS WHERE CLUSTERS.cluster_id=TESTRESULTS.cluster_id)) AS 'Probe Name'
                                      , (SELECT `service_name` FROM SERVICES WHERE SERVICES.service_id=TESTRESULTS.service_id) AS 'Service Name'
                                      , (SELECT `destination_name` FROM DESTINATIONS WHERE DESTINATIONS.destination_id=TESTRESULTS.destination_id) AS 'Destination Name'
                                      , (SELECT `destination_port` FROM DESTINATIONS WHERE DESTINATIONS.destination_id=TESTRESULTS.destination_id) AS 'Port'
                                      , (SELECT `destination_description` FROM DESTINATIONS WHERE DESTINATIONS.destination_id=TESTRESULTS.destination_id) AS 'Description'
                                      , ROUND(AVG(`round_trip_time`), 3) AS 'Avg. RTT (ms)', ROUND(AVG(`download`)/POWER(10,6), 3) AS 'Avg. Download (Mbps)', ROUND(AVG(`upload`)/POWER(10,6), 3) AS 'Avg. Upload (Mbps)', AVG(`other`) AS 'Avg. Other Value'
                                      FROM TESTRESULTS WHERE `result_status`=1 GROUP BY `cluster_id` , `destination_id`;"""
        self.flowables.append(Paragraph("<strong>SUMMARY TEST RESULTS</strong>", style=self.sp_topic))
        self.break_part(1)
        self.create_table_with_sql(test_result, max_height=25)
        self.break_part(1)

    def create_body_service(self):
        sql_query = """SELECT `service_name` AS 'Name', `transport_protocol` AS 'Protocol', `file_name` AS 'File Name', `udp_command` AS 'UDP Msg.', `service_description` AS 'Description', 
                        `destination_example` AS 'Example of Destination', 
                        (SELECT `event_date` FROM LOGGING_EVENTS WHERE LOGGING_EVENTS.event_table='SERVICES' AND LOGGING_EVENTS.`event_name`=SERVICES.`service_name` ORDER BY `event_date` DESC LIMIT 1) AS 'Last Update',
                        (SELECT COUNT(`destination_id`) FROM DESTINATIONS WHERE SERVICES.service_id=DESTINATIONS.service_id) AS 'Total Destination'
                        FROM SERVICES WHERE `transport_protocol`='{trans_prot}';"""

        protocol_main_main = {
            'tcp':(PCMYKColor(93, 45, 0, 53), '#084278'),
            'udp':(PCMYKColor(0,66, 59, 45), '#8C2F39'),
            'other': (PCMYKColor(10, 13, 61, 4), '#DCD55F')
        }

        sql_type = "SELECT COUNT(`service_id`) FROM SERVICES WHERE `transport_protocol`={protocol};"
        protocol_num = map(lambda item: self.db.select(
            sql_type.format(protocol=int(item) if type(item) == int else '"{}"'.format(item)))[0][0], protocol_main_main)

        self.flowables.append(Paragraph("<strong>TOTAL TRANSPORT PROTOCOL RATIO</strong>", style=self.sp_topic))
        self.flowables.append(
            self.create_pie_chart(data_list=protocol_num, label_list=[i.upper() for i in protocol_main_main],
                                  user_color=[protocol_main_main[i][0] for i in protocol_main_main]))

        self.flowables.append(Paragraph("<strong>SUMMARY SERVICE INFORMATION</strong>", style=self.sp_topic))
        self.break_part(1)
        for key, val in zip(protocol_main_main, protocol_num):
            self.flowables.append(Paragraph(
                "TOTAL <strong><font color='{col}'>{main}</font></strong> service:{tab}{val} service(s)".format(main=key.upper(), val=val,
                                                                                     tab=self.tab, col=protocol_main_main[key][1]), style=self.sp_left))
            self.create_table_with_sql(sql_query.format(trans_prot=key), max_height=32)
            self.break_part(1)

        self.break_part(1)

        self.flowables.append(Paragraph("<strong>SUMMARY SERVICE STATUS</strong>", style=self.sp_topic))
        self.break_part(1)
        running = "SELECT (SELECT `probe_name` FROM PROBES WHERE PROBES.probe_id=(SELECT `probe_id` FROM CLUSTERS WHERE CLUSTERS.cluster_id=RUNNING_SERVICES.cluster_id)) AS 'Probe Name', (SELECT `service_name` FROM SERVICES WHERE RUNNING_SERVICES.service_id=SERVICES.service_id) AS 'Service Name', `running_svc_status` AS 'Status' FROM RUNNING_SERVICES;"
        self.create_table_with_sql(running)

        self.break_part(1)

        self.create_service_statistic_result()

    def create_service_statistic_result(self):
        self.flowables.append(Paragraph("<strong>SUMMARY SERVICE AND TEST STATISTICS</strong>", style=self.sp_topic))
        self.break_part(1)
        test_result = """SELECT (SELECT `probe_name` FROM PROBES WHERE PROBES.probe_id=(SELECT `probe_id` FROM CLUSTERS WHERE CLUSTERS.cluster_id=x.cluster_id)) AS 'Probe Name'
                                , (SELECT `service_name` FROM SERVICES WHERE x.service_id=SERVICES.service_id) AS 'Service Name'
                                , (select count(result_id) from TESTRESULTS y where result_status=1 and x.cluster_id=y.cluster_id and x.service_id=y.service_id) AS 'Pass Test (time)'
                                , (select count(result_id) from TESTRESULTS y where result_status=2 and x.cluster_id=y.cluster_id and x.service_id=y.service_id) AS 'Fail Test (time)'
                                , (select count(result_id) from TESTRESULTS y where result_status=3 and x.cluster_id=y.cluster_id and x.service_id=y.service_id) AS 'Error Test (time)'
                                , COUNT(`result_id`) AS 'Total Test (time)' FROM TESTRESULTS x GROUP BY `cluster_id` , `service_id`"""
        self.create_table_with_sql(test_result)

    def get_destination_type(self):
        sql_query = "SELECT (SELECT `service_name` FROM SERVICES WHERE SERVICES.service_id=DESTINATIONS.service_id) AS 'Service Name', COUNT(`destination_id`) FROM DESTINATIONS GROUP BY `service_id`"
        result_query = self.db.select(sql_query)
        label = map(lambda item: item[0], result_query)
        data = map(lambda item: item[1], result_query)
        self.create_pie_chart(data_list=data, label_list=label)
        return label, data

    def create_body(self):

        self.create_body_service()

        self.flowables.append(PageBreak())

        self.create_body_destination()

class PDFLogging(PDFCreation):

    def create_log_bar_chart(self):
        sql_query = "SELECT COUNT(`logging_id`) FROM LOGGING_EVENTS WHERE `user`='{usr}' AND `event_type`='{type}'"
        event_action = ['insert', 'update', 'delete']
        all_user = map(lambda item: item[0], self.db.select("SELECT DISTINCT(`user`) FROM LOGGING_EVENTS;"))
        sql_part_user = """SELECT `user` AS 'Username', `event_date` AS 'Last Logged Time'
                        , (SELECT COUNT(`logging_id`) FROM LOGGING_EVENTS WHERE user = '{usr}' AND `event_type`='insert') AS 'Total Insert Transaction'
                        , (SELECT COUNT(`logging_id`) FROM LOGGING_EVENTS WHERE user = '{usr}' AND `event_type`='update') AS 'Total Update Transaction'
                        , (SELECT COUNT(`logging_id`) FROM LOGGING_EVENTS WHERE user = '{usr}' AND `event_type`='delete') AS 'Total Delete Transaction'
                        , (SELECT COUNT(`logging_id`) FROM LOGGING_EVENTS WHERE user = '{usr}') AS 'Total Transaction'
                        FROM LOGGING_EVENTS WHERE user='{usr}' ORDER BY `event_date` DESC LIMIT 1"""
        part_user_data = map(lambda item: self.db.select(sql_part_user.format(usr=item))[0], all_user)
        part_user_desc = [field[0] for field in self.db.mycursor.description]
        output = map(lambda item: map(lambda val: self.db.select(sql_query.format(usr=val, type=item))[0][0], all_user), event_action)

        self.flowables.append(Paragraph("<strong>SUMMARY TRANSACTION OF EACH USER</strong>", style=self.sp_small_topi))
        self.create_bar(data_list=output, label_x_axis=all_user, contain=event_action, y_label='transaction(s)', x_label='user', user_color=[colors.lawngreen, colors.blue, colors.red], fontSize=8)
        self.break_part(1)
        self.create_table_with_data_description(list_data=part_user_data, list_description=part_user_desc,
                                                max_width=540)

    def create_table_with_data_description(self, list_data, list_description, max_width=530, max_height=16):
        result_all = map(lambda item: map(lambda inner: Paragraph(str(inner), style=self.get_style()) if inner != None else '-', item), list_data)
        description = map(lambda item: Paragraph("<strong>{desc}</strong>".format(desc=str(item)), style=self.get_style()), list_description)
        result_all.insert(0, description)

        row = len(result_all) - 1
        column = len(list_description) -1

        width = [max_width / len(result_all[0]) for i in range(len(result_all))]
        height = [max_height for i in range(len(result_all))]

        table = Table(result_all, colWidths=width, rowHeights=height, hAlign='CENTER')
        table.setStyle(TableStyle([('ALIGN', (0, 0), (column, row), 'CENTER'),
                                   ('VALIGN', (0, 0), (column, row), 'MIDDLE'),
                                   ('FONTSIZE', (0, 0), (column, row), 8),
                                   ('INNERGRID', (0, 0), (column, row), 0.25, colors.black),
                                   ('BOX', (0, 0), (column, row), 0.25, colors.black),
                                   ('TEXTCOLOR', (0, 0), (column, row), colors.black), ]))
        self.flowables.append(table)

    def get_log_time_interval(self):
        sql = """select DATE_FORMAT(event_date, '%Y-%m-%d %H:%00:00') AS 'start', DATE_FORMAT(event_date + INTERVAL 1 DAY, '%Y-%m-%d %H:%00:00') AS 'end'
              , (select count(logging_id) FROM LOGGING_EVENTS WHERE event_date between start and end and event_type='insert') AS 'Insert'
              , (select count(logging_id) FROM LOGGING_EVENTS WHERE event_date between start and end and event_type='update') AS 'Update'
              , (select count(logging_id) FROM LOGGING_EVENTS WHERE event_date between start and end and event_type='delete') AS 'Delete'
              from LOGGING_EVENTS
              GROUP BY UNIX_TIMESTAMP(event_date) DIV 86400"""
        ### 1296000 equal 15 days
        ### 86400 equal 1 day
        ### 604800 equal 1 week
        action = ['insert', 'update', 'delete']
        format1 = '%Y-%m-%d %H:%M:%S'
        format2 = '%d-%b'
        result = self.db.select(sql)
        result_description_date = map(lambda item: datetime.datetime.strptime(item[0], format1).strftime(format2), result)
        result_format = map(lambda index: map(lambda item: item[index], result), [i for i in range(2, len(action)+2)])

        self.flowables.append(Paragraph("<strong>SUMMARY TRANSACTION BY TIME AND TYPE OF TRANSACTION</strong>", style=self.sp_small_topi))
        self.create_bar(data_list=result_format, contain=action, label_x_axis=result_description_date, user_color=[colors.lawngreen, colors.blue, colors.red], y_label='transaction(s)', x_label='Date', x_angle=45)

    def create_body(self):
        log_table = {'PROBES': 'PROBE',
                     'SERVICES': 'SERVICE',
                     'DESTINATIONS': 'DEDSTINATION',
                     'RUNNING_SERVICES': 'STATUS SERVICE',
                     'RUNNING_DESTINATIONS': 'STATUS DESTINATION',
                     'NOTIFY_TOKEN': 'LINE TOKEN',
                     'NOTIFICATIONS': ' NOTIFICATION',
                     'DASHBOARD': 'DASHBOARD'
                     }

        log_rf_name = ['Probe Name', 'Service Name', 'Destination Name', 'Service Name', 'Destination Name', 'Token Description', 'Notification Name', 'Chart Name']
        sql_amount = "SELECT COUNT(`logging_id`) FROM LOGGING_EVENTS WHERE `event_table`='{tlb}';"
        sql_log_detail = "SELECT  `event_date` AS 'Logged Time', `user` AS 'Username', `event_type` AS 'Transaction', `event_name` AS '{ref_name}' FROM LOGGING_EVENTS WHERE `event_table`='{tlb}' ORDER BY 'Logged Time' ASC;"
        total_transaction = map(lambda item: self.db.select(sql_amount.format(tlb=item))[0][0], sorted(log_table))

        self.flowables.append(Paragraph("<strong>COLLECT LOG EVENT FROM:</strong>", style=self.sp_left))
        map(lambda table, val: self.flowables.append(Paragraph("{num}. {text}".format(text=table, num=val), style=self.sp_small_topi)), sorted(log_table), [i for i in range(1, len(log_table)+1)] )

        self.break_part(1)
        self.create_log_bar_chart()
        self.break_part(1)
        self.get_log_time_interval()

        self.flowables.append(PageBreak())

        for item, rf_name, total in zip(sorted(log_table), sorted(log_rf_name), total_transaction):
            self.flowables.append(Paragraph("TOTAL LOG FROM <strong>{tlb}</strong>:{tab}<strong>{val} transaction{word}</strong>".format(tab=self.tab, word='' if total <= 1 else 's', tlb=log_table[item], val=total), style=self.sp_small_topi))
            self.break_part(1)
            self.create_table_with_sql(sql=sql_log_detail.format(tlb=item, ref_name=rf_name), max_height=18)
            self.break_part(1)

if __name__ == '__main__':
    probe_report = PDFProbe('Probe', 'probe_report_gen1.pdf', 'both_logo.png')
    service_report = PDFService('Service', 'service_report_gen1.pdf', 'both_logo.png')
    log_report = PDFLogging('Logging Event', 'logging_report_gen1.pdf', 'both_logo.png')


