#!/usr/bin/python

print "Content-type: text/html\n\n"
print
print """
<br><div class="container">
    <div class="container">
        <div class="tabs is-toggle is-fullwidth">
            <ul>
                <li id="insert_service">
                    <a>
                        <span class="icon is-small"><i class="far fa-plus-square"></i></span>
                        <span> Insert </span>
                    </a>
                </li>
                <li id="delete_service">
                    <a>
                        <span class="icon is-small"><i class="far fa-trash-alt" ></i></span>
                        <span> Delete </span>
                    </a>
                </li>
            </ul>
        </div>
    </div>
    <div class="container" id="output_service"></div>
</div>

<script type="text/javascript">
$(document).ready(function() {

    $("#insert_service").on('click', function() {
    $("div.tabs.is-toggle.is-fullwidth ul li").removeClass("is-active")
        $("#insert_service").addClass("is-active")
        $("#service_db").addClass("is-active")
        $.ajax({
            url: 'service_main_insert.py',
            type: 'post',
            success: function(response) {
                $("#output_service").html(response);
                console.log('Success')
            }
        });
    });

    $("#delete_service").on('click', function() {
    $("div.tabs.is-toggle.is-fullwidth ul li").removeClass("is-active")
        $("#delete_service").addClass("is-active")
        $("#service_db").addClass("is-active")
        $.ajax({
            url: 'service_delete.py',
            type: 'post',
            success: function(response) {
                $("#output_service").html(response);
                console.log('Success')
            }
        });
    });

});
</script>
"""
