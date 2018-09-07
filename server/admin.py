#!/usr/bin/python

print "Content-type: text/html\n\n"
print 
print """
<section class="section">
    <div class="container">
        <div class="tabs is-toggle is-fullwidth">
            <ul>
                <li id="destination_db">
                    <a>
                <span class="icon is-small"><i class="fas fa-map-marked-alt"></i></span>
                <span>
                    Destination
                </span>
            </a>
                </li>
                <li id="service_db">
                    <a>
                <span class="icon is-small"><i class="fas fa-desktop" ></i></span>
                <span> Service </span>
            </a>
                </li>
                <li id="running_active_db">
                    <a>
                <span class="icon is-small"><i class="fas fa-clipboard-list"></i></span>
                <span> Running Service</span>
            </a>
                </li>
            </ul>
        </div>
    </div>
    <div class="container" id="alter"></div>
</section>

<script type="text/javascript">
$(document).ready(function() {

    $("#destination_db").on('click', function() {
	$("div.tabs.is-toggle.is-fullwidth ul li").removeClass("is-active")
        $("#destination_db").addClass("is-active")
        $.ajax({
            url: 'destination.py',
            type: 'post',
            success: function(response) {
                $("#alter").html(response);
                console.log('Success')
            }
        });
    });

    $("#service_db").on('click', function() {
	$("div.tabs.is-toggle.is-fullwidth ul li").removeClass("is-active")
        $("#service_db").addClass("is-active")
        $.ajax({
            url: 'service.py',
            type: 'post',
            success: function(response) {
                $("#alter").html(response);
                console.log('Success')
            }
        });
    });

    $("#running_active_db").on('click', function() {
	$("div.tabs.is-toggle.is-fullwidth ul li").removeClass("is-active")
        $("#running_active_db").addClass("is-active")
        $.ajax({
            url: 'running.py',
            type: 'post',
            success: function(response) {
                $("#alter").html(response);
                console.log('Success')
            }
        });
    });
});
</script>
"""