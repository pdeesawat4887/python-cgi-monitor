#!/usr/bin/python

import main.database as mariadb
print "Content-type: text/html\n\n"


class Destination(mariadb.MySQLDatabase):

    def __init__(self):
        mariadb.MySQLDatabase.__init__(self)

    def get_service(self):
        data = []
        list_service = []
        list_service = self.select(
            'service', None, 'service_id', 'service_name')
        return list_service

    def get_destination(self, service_id):
        query_sql = "SELECT destination_id, destination, destination_port FROM destination INNER JOIN service ON destination.service_id=service.service_id WHERE destination.service_id={}".format(
            service_id)
        self.mycursor.execute(query_sql)
        return self.mycursor.fetchall()

worker = Destination()
list_service = worker.get_service()

print """
<div class="container"><br>
    <div class="notification">
        <p class="title is-4"><strong>INSERT </strong> Destination </p>
        <form>
            <label class="label"> Select service type: </label>
            <span class="select">
                <select name=TypeList id="TypeList" ><br>"""
for service in list_service:
    print """<option value="{}">{}</option>""".format(service[0], service[1])
print """</select>
            </span><br><br>
            <label class="label">Insert destination: </label>
            <input class="input" type="text" placeholder="https://example.com or 10.10.10.10" id="destination">
            <br><br>
            <label class="label">Insert destination port: </label>
            <input class="input" type="text" placeholder="80" id="destination_port"><br><br>
            <a class="button is-info" id="insert_btn_dest">Insert</a><span id="output_insert_dest" style="margin-left:30px;"></span>
        </form>
    </div>
</div>"""

print"""
<br>
    <div class="container">
        <div class="notification">
            <table class="table is-hoverable is-fullwidth is-bordered is-striped is-narrow" id="thisTable" style="table-layout:fixed;">
                <thead>
                    <tr>
                        <th class="has-text-centered" style="width:100px">Service</th>
                        <th class="has-text-centered" style="width:100px">ID</th>
                        <th class="has-text-centered">Destination</th>
                        <th class="has-text-centered">Destination Port</th>
                        <th class="has-text-centered">operation</th>
                        <th class="has-text-centered">status</th>
                    </tr>
                </thead>
                <tbody> """
for service in list_service:
    myresult = worker.get_destination(service[0])
    print """<tr class="is-selected"><th class="has-text-centered" >{}</th><th></th><th></th><th></th><th></th><th></th></tr>""".format(service[1])
    for dest in myresult:
        dest_id = dest[0]
        dest_dest = dest[1]
        dest_port = dest[2]
        print """
        <tr>
        <td class="has-text-centered">{}</td>
        <td id="row_{}" class="has-text-centered" >{}</td>
        <td><input class="input" type="text" id="dest_{}" value="{}"></td>""".format(service[1], dest_id, dest_id, dest_id, dest_dest)
        print """
        <td><input class="input" type="text" id="port_{}" value="{}"></td>
        <td class="has-text-centered">
            <input style="margin-right: 5px" class="button is-info" type="button" onclick="edit_row('{}')" value="update">
            <input style="margin-left: 5px" class="button is-danger" type="button" onclick="del_row('{}')" value="delete">
        </td>
        <td id="update_status_{}" class="has-text-centered"></td>
        </tr>""".format(dest_id, dest_port, dest_id, dest_id, dest_id)
print """
        </div>
    </div>
</div>
"""

print """
<script>
function edit_row(no) 
{
    var dest=document.getElementById("dest_"+no).value;
    var port=document.getElementById("port_"+no).value;
    var d_id = document.getElementById("row_"+no).textContent;

        $.ajax({
            url: 'destination_update.py',
            type: 'post',
            data: {
                'd_id': d_id,
                'dest': dest,
                'port': port
            },
            success: function(response) {

                console.log(d_id);
                console.log(dest);
                console.log(port);

                $("#update_status_"+no).html(response);

                $.ajax({
                    url: 'destination.py',
                    type: 'post',
                    success: function(response) {
                        $("#alter").html(response);
                        console.log('Success after new')
                    }
                });
            },
            error: function(request, ajaxOptions, thrownError) {
                $("#update_status_"+no).html(request.responseText);
            }
        });

    var div2 = $("#update_status_"+no);
    div2.show();
    setTimeout(function() {
        div2.hide();
    }, 10000);

}

function del_row(no) 
{

    var del_id = document.getElementById("row_"+no).textContent;

        $.ajax({
            url: 'destination_delete.py',
            type: 'post',
            data: {
                'del_id': del_id,
            },
            success: function(response) {

                $('#dest_'+no).val('')
                $('#port_'+no).val('')
                console.log(del_id);

                $("#update_status_"+no).html(response);

                $.ajax({
                    url: 'destination.py',
                    type: 'post',
                    success: function(response) {
                        $("#alter").html(response);
                        console.log('Success after new')
                    }
                });
            },
            error: function(request, ajaxOptions, thrownError) {
                $("#update_status_"+no).html(request.responseText);
            }
        });

    var div2 = $("#update_status_"+no);
    div2.show();
    setTimeout(function() {
        div2.hide();
    }, 10000);

}
</script>

<script>
$(function() {

	function insert_destination() {
        var destination = $("#destination").val();
        var destination_port = $("#destination_port").val();
        var TypeList = $("#TypeList").val();

        $.ajax({
            url: 'destination_insert.py',
            type: 'post',
            data: {
                'destination': destination,
                'destination_port': destination_port,
                'TypeList': TypeList
            },
            success: function(response) {

                console.log(destination);
                console.log(TypeList);
                console.log(destination_port);

                $('#destination').val('');
                $('#destination_port').val('');
                $("#TypeList").val('');

                $("#output_insert_dest").html(response);

                $.ajax({
                    url: 'destination.py',
                    type: 'post',
                    success: function(response) {
                        $("#alter").html(response);
                        console.log('Success after new')
                    }
                });
            },
            error: function(request, ajaxOptions, thrownError) {
                $("#output_insert_dest").html(request.responseText);
            }
        });

    }


	$("#insert_btn_dest").click(function() {
        output_destination = insert_destination();
    });
});
</script>
"""
