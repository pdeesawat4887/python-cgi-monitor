#!/usr/bin/python

print "Content-type: text/html\n\n"

import cgi
import main.database as mariadb


def get_running_service():
    database = mariadb.MySQLDatabase()
    query_sql = """select running_service.probe_id, probe_name, running_service.service_id, service_name, running
    from running_service
    inner join service on running_service.service_id=service.service_id
    inner join probe on running_service.probe_id=probe.probe_id;"""

    database.mycursor.execute(query_sql)
    return database.mycursor.fetchall()

list_running = get_running_service()

print """
<div class="container"><br>
    <div class="notification">
        <div class="container">
            <p class="title is-4"><strong>Update Active Service </strong></p>
            <div class="columns is-centered">
                <table class="table is-hoverable is-bordered is-striped is-narrow" id="thisTable2" style="table-layout:fixed;">
                    <thead>
                        <tr>
                            <th class="has-text-centered" style="width:200px">Probe Name</th>
                            <th class="has-text-centered" style="width:300px">Service Name</th>
                            <th class="has-text-centered" style="width:300px">Operation</th>
                            <th class="has-text-centered" style="width:300px">Status</th>
                        </tr>
                    </thead>
                    <tbody> """
for running in list_running:
    probe_id = running[0]
    probe_name = running[1]
    service_id = running[2]
    service_name = running[3]
    status = running[4]
    active = None
    deactive = None

    if int(status) == 0:
        active = 'selected'
    else:
        deactive = 'selected'
    print """

    <tr ><td class="has-text-centered">{}</td><td class="has-text-centered">{}</td>
    <td class="has-text-centered"><select name=TypeList id="id_{}_{}">
    <span>
    <option style="margin-right: 5px" value="{}" {}>Active</option><option value="{}" {}>Deactive</option></select>
    
    <input class="button is-info is-small" type="button" onclick="update_row('{}', '{}')" value="update" style="margin-left: 5px">
    </span>
    </td><td id="response_{}_{}"></td></tr>""".format(probe_name, service_name, probe_id, service_id, 0, active, 1, deactive, probe_id, service_id, probe_id, service_id)

print """
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<script>

function update_row(probe_id, service_id) 
{
    var status_service = $("#id_"+probe_id+"_"+service_id).val();
    var probe_id = probe_id;
    var service_id = service_id;

        $.ajax({
            url: 'running_update.py',
            type: 'post',
            data: {
                'probe_id': probe_id,
                'service_id': service_id,
                'status_service': status_service
            },
            success: function(response) {

                console.log(probe_id);
                console.log(service_id);
                console.log(status_service);

                $("#response_"+probe_id+"_"+service_id).html(response);
            },
            error: function(request, ajaxOptions, thrownError) {
                $("#response_"+probe_id+"_"+service_id).html(request.responseText);
            }
        });

    var div2 = $("#response_"+probe_id+"_"+service_id);
    div2.show(0).delay(3000).hide(0);

}
</script>
"""
