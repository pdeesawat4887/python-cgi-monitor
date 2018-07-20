var ipList = [];

$(document).ready(function () {

    // var timer = null,
    //     interval = 3000,
    //     val = 0;

    $('#btn_AddToList').click(function () {
        var val = $('#ipaddress').val();
        ipList.push(val);
        // $('#ipList').html(list);
        document.getElementById("ipList").innerHTML = ipList;
        document.getElementById('ipaddress').value = '';
        // $('#txt_RegionName').val('').focus();
    });

    // $("#start").on('click', function () {
    //     if (timer !== null) return;
    //     timer = setInterval(myTimerFunc(), interval);
    // });
    //
    // $("#pause").on('click', function () {
    //     clearInterval(timer);
    //     timer = null;
    // });
});

$(function () {
    var timer = null,
        interval = 30000,
        value = 0;

    function timeInterval() {
        if (ipList === undefined || ipList.length == 0) {
            ipList.push($("#ipaddress").val());
        }
        console.log(ipList);
        var droplist = $("#droplist").val();
        var community = $("#community").val();
        if (community === "") {
            community = "public";
        }
        $.ajax({
            url: 'test.py',
            type: 'post',
            data: {
                'ipList': JSON.stringify(ipList),
                'community': community,
                'droplist': droplist
            },
            success: function (response) {
                console.log(ipList);
                $("#table").html(response);
            }, error: function (request, ajaxOptions, thrownError) {
                $("#table").html(request.responseText);
            }
        });
    }

    $("#start").click(function () {
        if (timer !== null) return;
        timer = timeInterval();
        timer = setInterval(function () {
            timeInterval()
        }, interval);

    });

    $("#stop").click(function () {
        clearInterval(timer);
        timer = null;
        document.getElementById('ipaddress').value = '';
        document.getElementById('droplist').value = '';
        ipList = []
    });
});