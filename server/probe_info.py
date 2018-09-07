#!/usr/bin/python
# import mysql.connector as mariadb
import main.database as mariadb
import cgi

print '''Content-type: text/html\n'''


def probe_header(probe_id):
    probe_info = get_anything("probe_name, ip_address, mac_address,`status`", "probe",
                              "probe_id = '{}'".format(probe_id))
    print '''        <section class="section" id="probe_header" style="margin-top: -3%;">
            <div class="container">
                <nav class="level">
                    <div class="level-left">
                        <div class="level-item">
                            <div>
                                <h2 class="title is-4">'''
    print '''                                   {}'''.format(probe_info[0])
    if (probe_info[3] == 0):
        print '''                                               <span class="icon is-medium"><i class="fas fa-check-circle has-text-success"></i></span>'''
    else:
        print '''                                               <span class="icon is-medium"><i class="fas fa-times-circle has-text-danger"></i></span>'''
    print '''                               </h2>'''
    print '''                                <p class="title is-6">{}</p>'''.format(probe_info[2].upper())
    print '''                                <p class="title is-6">{}</p>'''.format(probe_info[1])
    print '''                            </div>
                        </div>
                    </div>
                    <div class="level-right">
                        <div class="level-item has-text-centered">
                            <div>
                                <p class="heading">Choose your time period:</p>
                                <div class="tabs is-toggle is-toggle-rounded is-small">
                                    <ul>'''
    print '''                                        <li class="is-active" id="{}_1_day">'''.format(probe_id)
    print '''                                            <a>
                                                <span class="icon is-small"><i class="far fa-clock"></i></span>
                                                <span>1 Day</span>
                                            </a>
                                        </li>'''
    print '''                                        <li id="{}_7_day">'''.format(probe_id)
    print '''                                            <a>
                                                <span class="icon is-small"><i class="fas fa-calendar"></i></span>
                                                <span>1 Week</span>
                                            </a>
                                        </li>'''
    print '''                                        <li id="{}_30_day">'''.format(probe_id)
    print '''                                            <a>
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
        </section>
        <section class="section" id="selector">
        </section>'''
    print '''        <script>'''
    print '''        $(document).ready(function() {
                        $.ajax({
                url: 'service_selector.py',
                type: 'post',
                data: {'''
    print '''                   data: "{}_1"'''.format(probe_id)
    print '''                },
                success: function (response) {
                    $("#selector").html(response);
                }
            });
        });'''
    print '''        $("#{}_1_day").on('click', function ()'''.format(probe_id)
    print '''        {
            $("div.tabs.is-toggle.is-toggle-rounded.is-small ul li").removeClass("is-active")'''
    print '''            $("#{}_1_day").addClass("is-active")'''.format(probe_id)
    print '''            $.ajax({
                url: 'service_selector.py',
                type: 'post',
                data: {
                   data: this.id
                },
                success: function (response) {
                    $("#selector").html(response);
                }
            });
        });'''
    print '''        $("#{}_7_day").on('click', function ()'''.format(probe_id)
    print '''        {
            $("div.tabs.is-toggle.is-toggle-rounded.is-small ul li").removeClass("is-active")'''
    print '''            $("#{}_7_day").addClass("is-active")'''.format(probe_id)
    print '''            $.ajax({
                url: 'service_selector.py',
                type: 'post',
                data: {
                   data: this.id
                },
                success: function (response) {
                    $("#selector").html(response);
                }
            });
        });'''
    print '''        $("#{}_30_day").on('click', function ()'''.format(probe_id)
    print '''        {
            $("div.tabs.is-toggle.is-toggle-rounded.is-small ul li").removeClass("is-active")'''
    print '''            $("#{}_30_day").addClass("is-active")'''.format(probe_id)
    print '''            $.ajax({
                url: 'service_selector.py',
                type: 'post',
                data: {
                   data: this.id
                },
                success: function (response) {
                    $("#selector").html(response);
                }
            });
        });'''
    print '''        </script>'''


# def get_probe_info(probe_id):
#     # mariadb_connection = mariadb.connect(user='monitor', password='p@ssword', database='project',
#     #                                      host='192.168.254.31')
#     # cursor = mariadb_connection.cursor()
#     # cursor.execute("select probe_name, ip_address, mac_address, `status` from probe where probe_id = '{}';".format(probe_id))
#     # probe_info = cursor.fetchone()
#     db = mariadb.MySQLDatabase()
#     db.mycursor.execute(
#         "select probe_name, ip_address, mac_address,`status` from probe where probe_id = '{}';".format(probe_id))
#     probe_info = db.mycursor.fetchone()
#     return probe_info

def get_anything(column_name, table, where=None):
    db = mariadb.MySQLDatabase()
    if where:
        db.mycursor.execute("select {} from {} where {};".format(column_name, table, where))
    else:
        db.mycursor.execute("select {} from {};".format(column_name, table))
    result = db.mycursor.fetchone()
    return result


form = cgi.FieldStorage()
probe_id = form.getvalue('probe_id')
probe_header(probe_id)
