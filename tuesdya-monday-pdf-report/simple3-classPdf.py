from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.textlabels import Label
from reportlab.lib.colors import PCMYKColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import main.database as mariadb
import time
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from reportlab.lib.validators import Auto
from random import randint

class PDFCreation:

    def __init__(self, table, file_name):
        self.tab = "&nbsp;&nbsp;&nbsp;&nbsp;"
        self.master_font = "Times-Roman"
        self.styles = getSampleStyleSheet()
        self.table = table
        self.file_name = file_name
        self.db = mariadb.MySQLDatabase()
        self.flowables = []
        self.create_pdf()


    def create_pdf(self):
        self.doc = SimpleDocTemplate(self.file_name,
                                     pagesize=A4,
                                     # pagesize=landscape(A4),
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

        self.sp_small_topi = ParagraphStyle('parrafos',
                                      alignment=TA_LEFT,
                                      fontSize=10,
                                      fontName="Times-Roman",
                                      leading=16)
        self.create_header()
        self.create_body()

        self.doc.build(self.flowables)

    def break_part(self, line):
        blank = Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;", style=self.sp_left)
        for row in range(int(line)):
            self.flowables.append(blank)

    def create_header(self):
        self.flowables.append(Paragraph("NETWORK ACTIVE MONITORING SYSTEM REPORT", style=self.sp_header))
        self.flowables.append(Paragraph(
            "<strong>DATE:</strong>&nbsp;&nbsp;&nbsp;&nbsp;{date}".format(date=time.strftime("%A %d %B %Y")),
            style=self.sp_left))
        self.flowables.append(
            Paragraph("<strong>REPORT TOPIC:</strong>&nbsp;&nbsp;&nbsp;&nbsp;{topic}".format(topic=self.table.upper()),
                      style=self.sp_left))

    def create_body(self):
        pass

    def create_table(self, length, data, align, row_height=24):
        row = len(data) - 1
        column = len(data[0]) - 1
        table = Table(data, colWidths=length, rowHeights=row_height, hAlign=align)
        table.setStyle(TableStyle([('ALIGN', (0, 0), (column, row), 'CENTER'),
                                   ('VALIGN', (0, 0), (column, row), 'MIDDLE'),
                                   ('FONTSIZE', (0, 0), (column, row), 8),
                                   ('INNERGRID', (0, 0), (column, row), 0.25, colors.black),
                                   ('BOX', (0, 0), (column, row), 0.25, colors.black),
                                   ('TEXTCOLOR', (0, 0), (column, row), colors.black), ]))
        return table

    def get_style(self):
        styles = getSampleStyleSheet()
        style = styles["Normal"]
        style.fontSize = 7
        style.fontName = "Times-Roman"
        style.alignment=TA_CENTER
        return style

    # def create_pie_chart(self, data_list, label_list, ):
    #     """"""
    #     print data_list
    #     print label_list
    #     data = [(item / (sum(data_list) * 1.0)) * 100 for item in data_list]
    #     u_color = [colors.lawngreen, colors.red, colors.gray]
    #     # color = [colors.lawngreen, colors.red, colors.gray]
    #     # u_master = [randint(0, 100) for i in range(4)]
    #     # u_color = [PCMYKColor(randint(0, u_master[0]), randint(0, u_master[1]), randint(0, u_master[2]), randint(0, u_master[3])) for i in range(3)]
    #     # print u_color
    #     # color = u_color
    #     d = Drawing()
    #     pie = Pie()
    #     pie.x = 180
    #     pie.y = 80
    #     pie.data = data
    #     pie.labels = label_list
    #     for i, color in enumerate(u_color): pie.slices[i].fillColor = color
    #     pie.slices.strokeWidth = 0.5
    #     pie.slices.popout = 1.5
    #     pie._seriesCount = 3
    #     pie.sideLabels = 1
    #
    #     legend = Legend()
    #     legend.alignment = 'right'
    #     legend.x = 0
    #     legend.y = 75
    #     legend.colorNamePairs = [(z, (x, '     {val:.2f}%'.format(val=y))) for x, y, z in zip(pie.labels, data, u_color)]
    #     d.add(legend)
    #     d.add(pie)
    #     return d

    def create_pie_chart(self, data_list, label_list, user_color=None):
        # print data_list
        # print label_list

        label_list = map(lambda item: item.upper(), label_list)

        data = [(item / (sum(data_list) * 1.0)) * 100 for item in data_list]

        if user_color != None:
            usage_color = user_color
        else:
            random_range = [randint(0, 100) for i in range(len(data_list))]
            usage_color = map(lambda item: PCMYKColor(randint(0, item), randint(0, item), randint(0, item), randint(0, item)), random_range)
            print user_color

        # u_color = [colors.lawngreen, colors.red, colors.gray]
        # color = [colors.lawngreen, colors.red, colors.gray]
        # u_master = [randint(0, 100) for i in range(4)]
        # u_color = [PCMYKColor(randint(0, u_master[0]), randint(0, u_master[1]), randint(0, u_master[2]), randint(0, u_master[3])) for i in range(3)]
        # print u_color
        # color = u_color

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
        # return d

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

    def before_table_log(self, table):
        log_sql = "SELECT `event_type`, count(`logging_id`) AS 'record' FROM LOGGING_EVENTS WHERE `event_table`='{tlb}' GROUP BY `event_type`;".format(tlb=table.upper())
        log_result = self.db.select(log_sql)

        if not log_result:
            self.flowables.append(Paragraph("<strong>EMPTY LOGGING</strong>", style=self.sp_small_topi))
        else:
            map(lambda item: self.flowables.append(Paragraph("<strong>{main} Logging:</strong>{tab}{val} record(s)".format(tab=self.tab, main=item[0].capitalize(), val=item[1]), style=self.sp_left)), log_result)

class PDFProbe(PDFCreation):

    def get_fk_cluster_information(self, status):

        happy = []
        x_axis = []

        sql_query_pb = """SELECT `probe_name`, (SELECT `cluster_id` FROM CLUSTERS WHERE CLUSTERS.probe_id=PROBES.probe_id) FROM PROBES WHERE `probe_status`={status}"""
        output_probe = self.db.select(sql_query_pb.format(status=status))

        all_svc = self.db.select("SELECT `service_id`, `service_name` FROM SERVICES")

        count = "SELECT COUNT(`result_id`) FROM TESTRESULTS WHERE `service_id`={isvc} and `cluster_id`={iclus};"

        for item in all_svc:
            isvc = item[0]
            x_axis.append(item[1])
            happy.append(tuple(
                map(lambda item: self.db.select(count.format(isvc=isvc, iclus=item[1]))[0][0] if item[1] != None else 0,
                    output_probe)))

        x_axis_probe = map(lambda item: item[0], output_probe)
        val = map(lambda item: sum(item), happy)

        if sum(val) != 0:
            self.create_bar(happy, x_axis_probe, x_axis)
        self.break_part(1)

    def create_bar(self, data_list, data_label, x_axis):

        print data_list
        print data_label
        print x_axis

        d = Drawing(width=180, height=200)
        bar = VerticalBarChart()
        bar.x = 150
        bar.y = 60
        bar.strokeColor = colors.black
        bar.barLabelFormat = '%s'
        bar.barLabels.nudge = 6
        bar.barLabels.fontSize = 6

        bar.categoryAxis.labels.dx = +5
        bar.categoryAxis.labels.dy = -7
        bar.categoryAxis.labels.boxAnchor = 'ne'
        bar.categoryAxis.labels.fontSize = 6
        bar.categoryAxis.labels.fontName = 'Helvetica'
        bar.categoryAxis.tickDown = 5
        bar.categoryAxis.categoryNames = data_label

        bar.valueAxis.forceZero = 1
        bar.valueAxis.labels.fontSize = 8
        bar.valueAxis.labels.fontName = 'Helvetica'
        bar.valueAxis.rangeRound = 'both'
        bar.valueAxis.valueMin = 0
        bar.valueAxis.visibleGrid = 1
        bar.valueAxis.visibleAxis = 1
        bar.valueAxis.labels.dx = -10

        bar.barSpacing = 2.5
        bar.groupSpacing = 10

        bar.data = data_list

        for i in range(len(data_list)):
            bar.bars[i].name = x_axis[i].upper()

        legend = Legend()
        legend.alignment = 'right'
        legend.boxAnchor = 'sw'
        legend.columnMaximum = 3
        legend.dx = 8
        legend.dxTextSpace = 4
        legend.dy = 6
        legend.fontSize = 8
        legend.fontName = 'Helvetica'
        legend.strokeColor = None
        legend.strokeWidth = 0
        legend.subCols.minWidth = 55
        legend.variColumn = 1
        legend.y = 1
        legend.deltay = 10
        legend.colorNamePairs = Auto(obj=bar)
        legend.autoXPadding = 65

        YLabel = Label()
        YLabel._text = ''
        YLabel.angle = 90
        YLabel.fontSize = 6
        YLabel.height = 0
        YLabel.maxWidth = 100
        YLabel.textAnchor = 'middle'
        YLabel.x = 12
        YLabel.y = 80

        d.add(bar)
        d.add(legend)
        d.add(YLabel)
        self.flowables.append(d)
        self.flowables.append(PageBreak())

    def get_probe_information(self, status):
        sql = "SELECT `probe_name`, `ip_address`, `mac_address`, `date_added`, `last_updated`, DATEDIFF(`last_updated`,`date_added`) as uptime FROM PROBES WHERE `probe_status`={status} order by `probe_name` ASC;"
        result = map(lambda item: list(item), self.db.select(sql.format(status=status)))
        option = {
            'probe_name': 'Probe Name',
            'ip_address': 'IP Address',
            'mac_address': 'MAC Address',
            'last_updated': 'Last Activity',
            'date_added': 'Installed Date',
            'uptime': 'Up time day(s)'
        }
        restrict = ['uptime']

        description = [field[0] for field in self.db.mycursor.description]
        probe_description = [option[field[0]] for field in self.db.mycursor.description]
        result.insert(0, probe_description)

        sql_width = "SELECT MAX(LENGTH(`{attribute}`)) FROM PROBES;"
        table_width = map(
            lambda item: (self.db.select(sql_width.format(attribute=item))[0][0]) * 5 if item not in restrict else len(
                option[item]) * 4, description)

        return table_width, result

    def get_probe_log(self):
        sql_log = "SELECT `user` AS 'User Modify', `event_type` AS 'Action', `event_name` AS 'Probe Name', `event_date` AS 'Time', DATEDIFF(NOW(),`event_date`) as 'days ago' FROM LOGGING_EVENTS WHERE `event_table`='PROBES' ORDER BY `event_date` ASC, `event_type`;"
        result_log = self.db.select(sql_log)
        description_log = [field[0] for field in self.db.mycursor.description]
        result_log.insert(0, description_log)
        tlb_0_width = max(map(lambda item: len(item[0]), result_log))
        tlb_1_width = max(map(lambda item: len(item[1]), result_log))
        tlb_2_width = max(map(lambda item: len(item[2]), result_log))
        table_log_width = [tlb_0_width, tlb_1_width, tlb_2_width, 20, 8]
        table_log_width = [i * 5 for i in table_log_width]

        return table_log_width, result_log

    def get_log_event_type(self, event_type):
        return self.db.select("SELECT COUNT(`logging_id`) FROM LOGGING_EVENTS WHERE `event_type`='{type}' AND `event_table`='PROBES'".format(type=event_type))[0][0]

    def create_body(self):
        tab = "&nbsp;&nbsp;&nbsp;&nbsp;"

        length, data_active = self.get_probe_information(status='1')
        active_header = Paragraph("<strong><font color='green'>ACTIVE</font> PROBE</strong>", style=self.sp_left)
        total_active = Paragraph(
            "<strong>TOTAL ACTIVE PROBE:</strong>{tab}{total}{tab}probe(s)".format(tab=tab, total=len(data_active) - 1),
            style=self.sp_left)
        table_active = self.create_table(length, data_active, 'LEFT')

        length_inactive, data_inactive = self.get_probe_information(status='2')
        inactive_header = Paragraph("<strong><font color='red'>INACTIVE</font> PROBE</strong>", style=self.sp_left)
        total_inactive = Paragraph("<strong>TOTAL INACTIVE PROBE:</strong>{tab}{total}{tab}probe(s)".format(tab=tab,
                                                                                                            total=len(
                                                                                                                data_inactive) - 1),
                                   style=self.sp_left)
        table_inactive = self.create_table(length_inactive, data_inactive, 'LEFT')

        length_idle, data_idle = self.get_probe_information(status='3')
        idle_header = Paragraph("<strong><font color='gray'>IDLE</font> PROBE</strong>", style=self.sp_left)
        total_idle = Paragraph(
            "<strong>TOTAL IDLE PROBE:</strong>{tab}{total}{tab}probe(s)".format(tab=tab, total=len(data_idle) - 1),
            style=self.sp_left)
        table_idle = self.create_table(length_idle, data_idle, 'LEFT')

        chart = self.create_pie_chart(data_list=[len(data_active) - 1, len(data_inactive) - 1, len(data_idle) - 1], label_list=['Active', 'Inactive', 'Idle'])


        ################################################### LOGGING ###################################################
        length_log, data_log = self.get_probe_log()
        log_header0 = Paragraph('<strong>PROBE LOGGING</strong>', style=self.sp_left)

        log_insert = Paragraph("<strong>Insert Logging:</strong>{tab}{count} record(s).".format(tab=tab,count=self.get_log_event_type('insert')), style=self.sp_small_topi)
        log_update = Paragraph("<strong>Update Logging:</strong>{tab}{count} record(s).".format(tab=tab,count=self.get_log_event_type('update')), style=self.sp_small_topi)
        log_delete = Paragraph("<strong>Delete Logging:</strong>{tab}{count} record(s).".format(tab=tab,count=self.get_log_event_type('delete')), style=self.sp_small_topi)
        # log_update = self.get_log_event_type('update')
        # log_delete = self.get_log_event_type('delete')

        log_header = Paragraph('<strong>DETAILS LOGGING ABOUT PROBE</strong>:{tab}{count} list(s)'.format(tab=tab, count=len(data_log)-1), style=self.sp_left)
        table_log = self.create_table(length_log, data_log, 'LEFT')

        self.break_part(1)
        self.flowables.append(chart)
        self.break_part(1)
        self.flowables.append(active_header)
        self.flowables.append(total_active)
        self.flowables.append(table_active)
        self.get_fk_cluster_information(1)
        # self.flowables.append(PageBreak())
        self.flowables.append(inactive_header)
        self.flowables.append(total_inactive)
        self.flowables.append(table_inactive)
        self.get_fk_cluster_information(2)
        # self.flowables.append(PageBreak())
        self.flowables.append(idle_header)
        self.flowables.append(total_idle)
        self.flowables.append(table_idle)
        self.get_fk_cluster_information(3)
        self.flowables.append(log_header0)
        # self.break_part(1)
        self.flowables.append(log_insert)
        self.flowables.append(log_update)
        self.flowables.append(log_delete)
        self.break_part(1)
        self.flowables.append(log_header)
        self.flowables.append(table_log)

class PDFService(PDFCreation):

    def get_service_type(self, protocol):
        sql_type = "SELECT COUNT(`service_id`) FROM SERVICES WHERE `transport_protocol`={protocol};".format(protocol=int(protocol) if type(protocol)==int else '"{}"'.format(protocol))
        return self.db.select(sql_type)[0][0]

    def create_body(self):
        sql_query = """SELECT `service_name` AS 'Name', `transport_protocol` AS 'Protocol', `file_name` AS 'File Name', `udp_command` AS 'UDP Msg.', `service_description` AS 'Description', 
                `destination_example` AS 'Example of Destination', 
                (SELECT `event_date` FROM LOGGING_EVENTS WHERE LOGGING_EVENTS.event_table='SERVICES' AND LOGGING_EVENTS.`event_name`=SERVICES.`service_name` ORDER BY `event_date` DESC LIMIT 1) AS 'Last Update',
                (SELECT COUNT(`destination_id`) FROM DESTINATIONS WHERE SERVICES.service_id=DESTINATIONS.service_id) AS 'Total Destination'
                FROM SERVICES WHERE `transport_protocol`='{trans_prot}';"""

        protocol_main = ['tcp', 'udp', 'other']
        protocol_num = map(lambda item: self.get_service_type(protocol=item), protocol_main)
        self.break_part(1)
        self.flowables.append(self.create_pie_chart(data_list=protocol_num, label_list=[protocol.upper() for protocol in protocol_main]))

        for key, val in zip(protocol_main, protocol_num):
            self.flowables.append(Paragraph("<strong>TOTAL {main} service:</strong>{tab}{val} service(s)".format(main=key.upper(), val=val, tab=self.tab), style=self.sp_left))
            self.create_table_with_sql(sql_query.format(trans_prot=key), max_height=32)
            self.break_part(1)

        # self.flowables.append(PageBreak())
        self.break_part(1)

        self.flowables.append(Paragraph("<strong>STATUS OF SERVICE</strong>", style=self.sp_left))
        self.break_part(1)
        running = "SELECT (SELECT `probe_name` FROM PROBES WHERE PROBES.probe_id=(SELECT `probe_id` FROM CLUSTERS WHERE CLUSTERS.cluster_id=RUNNING_SERVICES.cluster_id)) AS 'Probe Name', (SELECT `service_name` FROM SERVICES WHERE RUNNING_SERVICES.service_id=SERVICES.service_id) AS 'Service Name', `running_svc_status` AS 'Status' FROM RUNNING_SERVICES;"
        self.create_table_with_sql(running)

        # self.flowables.append(PageBreak())
        self.break_part(1)

        self.flowables.append(Paragraph("<strong>SUMMARY SERVICE AND TEST RESULTS</strong>", style=self.sp_left))
        self.break_part(1)
        test_result = """SELECT (SELECT `probe_name` FROM PROBES WHERE PROBES.probe_id=(SELECT `probe_id` FROM CLUSTERS WHERE CLUSTERS.cluster_id=x.cluster_id)) AS 'Probe Name'
                        ,(SELECT `service_name` FROM SERVICES WHERE x.service_id=SERVICES.service_id) AS 'Service Name'
                        , (select count(result_id) from TESTRESULTS y where result_status=1 and x.cluster_id=y.cluster_id and x.service_id=y.service_id) AS 'Pass'
                        , (select count(result_id) from TESTRESULTS y where result_status=2 and x.cluster_id=y.cluster_id and x.service_id=y.service_id) AS 'Fail'
                        , (select count(result_id) from TESTRESULTS y where result_status=3 and x.cluster_id=y.cluster_id and x.service_id=y.service_id) AS 'Error'
                        , COUNT(`result_id`) AS 'Amount Test' FROM TESTRESULTS x GROUP BY `cluster_id` , `service_id`"""
        self.create_table_with_sql(test_result)

        # self.flowables.append(PageBreak())
        self.break_part(1)

        logging_sql = "SELECT `user` AS 'User Modify', `event_type` AS 'Action', `event_name` AS 'Service Name', `event_date` AS 'Time', DATEDIFF(NOW(), `event_date`) AS 'Day Ago' FROM LOGGING_EVENTS WHERE `event_table`='SERVICES' ORDER BY 'Time' ASC;"
        self.flowables.append(Paragraph("<strong>SERVICE LOGGING</strong>", style=self.sp_left))
        self.before_table_log(table='SERVICES')
        self.break_part(1)
        self.create_table_with_sql(logging_sql)

class PDFDestination(PDFCreation):

    def get_destination_type(self):
        sql_query = "SELECT (SELECT `service_name` FROM SERVICES WHERE SERVICES.service_id=DESTINATIONS.service_id) AS 'Service Name', COUNT(`destination_id`) FROM DESTINATIONS GROUP BY `service_id`"
        result_query = self.db.select(sql_query)
        label = map(lambda item: item[0], result_query)
        data = map(lambda item: item[1], result_query)
        self.create_pie_chart(data_list=data, label_list=label)
        return label, data

    def create_body(self):
        dest_label, dest_data = self.get_destination_type()
        sql_condition = """SELECT `destination_name` AS 'Destination', `destination_port` AS 'Port'
                        , (SELECT `service_name` FROM SERVICES WHERE SERVICES.service_id=DESTINATIONS.service_id) AS 'Service Name', `destination_description` AS 'Description'
                        , (SELECT COUNT(`result_id`) FROM TESTRESULTS WHERE TESTRESULTS.destination_id=DESTINATIONS.destination_id) AS 'Amount Test'
                        , (SELECT COUNT(`result_id`) FROM TESTRESULTS WHERE result_status=1 AND TESTRESULTS.destination_id=DESTINATIONS.destination_id) AS 'Amount Pass'
                        , (SELECT COUNT(`result_id`) FROM TESTRESULTS WHERE result_status=2 AND TESTRESULTS.destination_id=DESTINATIONS.destination_id) AS 'Amount Fail'
                        , (SELECT COUNT(`result_id`) FROM TESTRESULTS WHERE result_status=3 AND TESTRESULTS.destination_id=DESTINATIONS.destination_id) AS 'Amount Error'
                        FROM DESTINATIONS WHERE `service_id`=(SELECT `service_id` FROM SERVICES WHERE SERVICES.`service_name`='{svc}') ORDER BY `service_id` ASC"""
        self.flowables.append(Paragraph("<strong>DESTINATION DETAIL</strong>",style=self.sp_left))

        for svc, val in zip(dest_label, dest_data):
            self.flowables.append(Paragraph("TOTAL DESTINATION(S) IN{tab}<strong>{svc}</strong>:{tab}{val} destination(s).".format(tab=self.tab, svc=svc.capitalize(), val=val), style=self.sp_small_topi))
            self.create_table_with_sql(sql_condition.format(svc=svc))
            self.break_part(1)

        running_dest = """SELECT (SELECT `probe_name` FROM PROBES WHERE PROBES.probe_id=(SELECT `probe_id` FROM CLUSTERS WHERE CLUSTERS.cluster_id=RUNNING_DESTINATIONS.cluster_id)) AS 'Probe Name'
                        , (SELECT `destination_name` FROM DESTINATIONS WHERE RUNNING_DESTINATIONS.destination_id=DESTINATIONS.destination_id) AS 'Destination Name'
                        , (SELECT `destination_port` FROM DESTINATIONS WHERE RUNNING_DESTINATIONS.destination_id=DESTINATIONS.destination_id) AS 'Port'
                        , (SELECT `destination_description` FROM DESTINATIONS WHERE RUNNING_DESTINATIONS.destination_id=DESTINATIONS.destination_id) AS 'Description'
                        ,`running_dest_status` AS 'Status' FROM RUNNING_DESTINATIONS;"""
        self.flowables.append(Paragraph("<strong>STATUS OF DESTINATION</strong>", style=self.sp_left))
        self.create_table_with_sql(running_dest)

        self.break_part(1)

        test_result = """SELECT (SELECT `probe_name` FROM PROBES WHERE PROBES.probe_id=(SELECT `probe_id` FROM CLUSTERS WHERE CLUSTERS.cluster_id=TESTRESULTS.cluster_id)) AS 'Probe Name'
                      , (SELECT `service_name` FROM SERVICES WHERE SERVICES.service_id=TESTRESULTS.service_id) AS 'Service Name'
                      , (SELECT `destination_name` FROM DESTINATIONS WHERE DESTINATIONS.destination_id=TESTRESULTS.destination_id) AS 'Destination Name'
                      , (SELECT `destination_port` FROM DESTINATIONS WHERE DESTINATIONS.destination_id=TESTRESULTS.destination_id) AS 'Port'
                      , (SELECT `destination_description` FROM DESTINATIONS WHERE DESTINATIONS.destination_id=TESTRESULTS.destination_id) AS 'Description'
                      , ROUND(AVG(`round_trip_time`), 3) AS 'Avg. RTT (ms)', ROUND(AVG(`download`)/POWER(10,6), 3) AS 'Avg. Download (Mbps)', ROUND(AVG(`upload`)/POWER(10,6), 3) AS 'Avg. Upload (Mbps)', AVG(`other`) AS 'Avg. Other Value'
                      FROM TESTRESULTS WHERE `result_status`=1 GROUP BY `cluster_id` , `destination_id`;"""
        self.flowables.append(Paragraph("<strong>SUMMARY DESTINATION AND TEST RESULTS</strong>", style=self.sp_left))
        self.create_table_with_sql(test_result, max_height=25)
        self.break_part(1)

class PDFLogging(PDFCreation):

    def create_log_bar_chart(self):
        sql_query = "SELECT COUNT(`logging_id`) FROM LOGGING_EVENTS WHERE `user`='{usr}' AND `event_type`='{type}'"
        event_action = ['insert', 'update', 'delete']
        all_user = map(lambda item: item[0], self.db.select("SELECT DISTINCT(`user`) FROM LOGGING_EVENTS;"))

        output = map(lambda item: map(lambda val: self.db.select(sql_query.format(usr=val, type=item))[0][0], all_user), event_action)
        self.create_bar_two(data_list=output, label_x_axis=all_user, contain=event_action)

    def create_bar(self, data_list, data_label, x_axis):
        d = Drawing(width=530, height=200)
        bar = VerticalBarChart()
        bar.x = 180
        bar.y = 60
        bar.strokeColor = colors.black
        bar.barLabelFormat = '%s'
        bar.barLabels.nudge = 6
        bar.barLabels.fontSize = 6

        bar.categoryAxis.labels.dx = +5
        bar.categoryAxis.labels.dy = -7
        bar.categoryAxis.labels.boxAnchor = 'ne'
        bar.categoryAxis.labels.fontSize = 6
        bar.categoryAxis.labels.fontName = 'Helvetica'
        bar.categoryAxis.tickDown = 5
        bar.categoryAxis.categoryNames = data_label

        bar.valueAxis.forceZero = 1
        bar.valueAxis.labels.fontSize = 8
        bar.valueAxis.labels.fontName = 'Helvetica'
        bar.valueAxis.rangeRound = 'both'
        bar.valueAxis.valueMin = 0
        bar.valueAxis.visibleGrid = 1
        bar.valueAxis.visibleAxis = 1
        bar.valueAxis.labels.dx = -10

        bar.barSpacing = 2.5
        bar.groupSpacing = 10

        bar.data = data_list

        for i in range(len(data_list)):
            bar.bars[i].name = x_axis[i].upper()

        legend = Legend()
        legend.alignment = 'right'
        legend.boxAnchor = 'sw'
        legend.columnMaximum = 3
        legend.dx = 8
        legend.dxTextSpace = 4
        legend.dy = 6
        legend.fontSize = 8
        legend.fontName = 'Helvetica'
        legend.strokeColor = None
        legend.strokeWidth = 0
        legend.subCols.minWidth = 55
        legend.variColumn = 1
        legend.y = 1
        legend.deltay = 10
        legend.colorNamePairs = Auto(obj=bar)
        legend.autoXPadding = 65

        YLabel = Label()
        YLabel.angle = 90
        YLabel.fontSize = 6
        YLabel.height = 0
        YLabel.maxWidth = 100
        YLabel.textAnchor = 'middle'
        YLabel.x = 12
        YLabel.y = 80
        YLabel._text = "User Modify"

        d.add(bar)
        d.add(legend)
        d.add(YLabel)
        self.flowables.append(d)
        self.flowables.append(PageBreak())

    def create_bar_two(self, data_list, label_x_axis, contain, bar_width=530, bar_height=200):
        d = Drawing(width=bar_width, height=bar_height)
        bar = VerticalBarChart()
        bar.x = bar.width
        bar.y = bar.height
        bar.strokeColor = colors.black
        bar.barLabelFormat = '%s'
        bar.barLabels.nudge = 7
        bar.barLabels.fontSize = 6

        ################# X AXIS PROPERTIES #################
        bar.categoryAxis.labels.dx = +6
        bar.categoryAxis.labels.boxAnchor = 'ne'
        bar.categoryAxis.labels.fontSize = 6.5
        bar.categoryAxis.labels.fontName = self.master_font
        bar.categoryAxis.tickDown = 5
        bar.categoryAxis.categoryNames = label_x_axis
        #####################################################

        ################# Y AXIS PROPERTIES #################
        bar.valueAxis.forceZero = 1
        bar.valueAxis.labels.fontSize = 8
        bar.valueAxis.labels.fontName = 'Helvetica'
        bar.valueAxis.rangeRound = 'both'
        bar.valueAxis.valueMin = 0
        bar.valueAxis.visibleGrid = 1
        bar.valueAxis.visibleAxis = 1
        bar.valueAxis.labels.dx = -10
        #####################################################

        bar.barSpacing = 2.5
        bar.groupSpacing = 10

        bar.data = data_list

        for i in range(len(data_list)):
            bar.bars[i].name = contain[i].upper()

        legend = Legend()
        legend.alignment = 'right'
        legend.boxAnchor = 'sw'
        legend.columnMaximum = 3
        legend.dx = 8
        legend.dxTextSpace = 4
        legend.dy = 6
        legend.fontSize = 8
        legend.fontName = 'Helvetica'
        legend.strokeColor = None
        legend.strokeWidth = 0
        legend.subCols.minWidth = 55
        legend.variColumn = 1
        legend.y = 1
        legend.deltay = 10
        legend.colorNamePairs = Auto(obj=bar)
        legend.autoXPadding = 65

        YLabel = Label()
        YLabel.angle = 90
        YLabel.fontSize = 6
        YLabel.height = 0
        YLabel.maxWidth = 100
        YLabel.textAnchor = 'middle'
        YLabel.x = 12
        YLabel.y = 80
        YLabel._text = "User Modify"

        d.add(bar)
        d.add(legend)
        d.add(YLabel)
        self.flowables.append(d)
        self.flowables.append(PageBreak())

    def create_body(self):
        log_table = ['PROBES','SERVICES','DESTINATIONS','RUNNING_SERVICES','RUNNING_DESTINATIONS','NOTIFY_TOKEN','NOTIFICATIONS','DASHBOARD']
        sql_amount = "SELECT COUNT(`logging_id`) FROM LOGGING_EVENTS WHERE `event_table`='{tlb}';"
        sql_log_detail = "SELECT `user` AS 'User Modify', `event_type` AS 'Action', `event_name` AS 'Service Name', `event_date` AS 'Time' FROM LOGGING_EVENTS WHERE `event_table`='{tlb}' ORDER BY 'Time' ASC;"

        # for item in log_table:
        #     total = self.db.select(sql_amount.format(tlb=item))[0][0]
        #     self.flowables.append(Paragraph("TOTAL {tlb} LOG:{tab}{val} record(s)".format(tab=self.tab, tlb=item.replace('_', ' '), val=total), style=self.sp_header))
        #     self.create_table_with_sql(sql=sql_log_detail.format(tlb=item), max_height=25)
        #     self.flowables.append(PageBreak())

        self.create_log_bar_chart()

if __name__ == '__main__':
    # pass
    # probe_report = PDFProbe('Probe', 'probe_report_gen1.pdf')
    # probe_report.get_Rfk_cluster_information(1)
    # service_report = PDFService('Service', 'service_report_gen1.pdf')
    # destination_report = PDFDestination('Destination', 'destination_report_gen1.pdf')
    log_report = PDFLogging('Logging Event', 'logging_report_gen1.pdf')
    # random_color()

