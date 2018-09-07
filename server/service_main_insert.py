#!/usr/bin/python

print "Content-type: text/html\n\n"
print """
<div class="container"><br>
	<div class="container">
        <div class="notification">
            <p class="title is-4"><strong>INSERT </strong> Service </p>
            <strong>STEP 1: </strong>Insert New Service at here.<br><br>
            <FORM method="GET" action="../cgi-bin/hello.py" name="Form">
                <div class="control">
                    <input class="input" type="text" placeholder="Service Name" name="service_name" id="service_name" required>
                    <br>
                    <br>
                    <input class="input" type="text" placeholder="File Name (example: XXXService.py)" name="file_name" id="file_name" required>
                </div>
                <br>
                <!-- <input class="button is-info" type="submit" value="submit" id="insert"> -->
                <a class="button is-link" id="start">insert</a>
            </FORM>
        </div>
    </div>
    <br>
    <div class="container">
        <div class="notification" id="output">
            wait for your information, <strong>service_id</strong> is important to coding.
        </div>
    </div>
    <br>
    <div class="container">
        <div class="notification">
            <form enctype="multipart/form-data" action="../cgi-bin/upload.py" method=post>
                <strong>STEP 2: </strong>Writing code and upload file .py at here (update)
                <br>
                <br>
                <div class="file has-name is-fullwidth">
                    <label class="file-label">
                        <input class="file-input" type="file" name="file" id="file" accept=".py, .txt">
                        <span class="file-cta">
                            <span class="file-icon">
                                <i class="fas fa-upload"></i>
                            </span>
                            <span class="file-label">
                                Choose a file...
                            </span>
                        </span>
                        <span class="file-name" id="filename">
                        </span>
                    </label>
                </div>
                <br>
                <a class="button is-link" id="upload_btn">upload</a>
                <!-- <input type="submit" class="button is-link" id="upload" value="upload"></a> -->
            </form>
        </div>
    </div>
    <br>
    <div class="container">
        <div class="notification" id="output_upload">
            wait for your upload, <strong> file </strong> is important to monitor service.
        </div>
    </div>
</div>

<script type="text/javascript">

    var file = document.getElementById("file");
    file.onchange = function() {
        if (file.files.length > 0) {
            document.getElementById('filename').innerHTML = file.files[0].name;
        }
};


$(function() {

    function insert_service() {

        var a=document.forms["Form"]["service_name"].value;
        var b=document.forms["Form"]["file_name"].value;
        if (a==null || a=="",b==null || b=="")
        {
            alert("Please Fill All service name or file name Required Field");
            return false;
        }

        var service_name = $("#service_name").val();
        var file_name = $("#file_name").val();

        $.ajax({
            url: 'service_insert.py',
            type: 'post',
            data: {
                'service_name': service_name,
                'file_name': file_name
            },
            success: function(response) {
                console.log(service_name);
                console.log(file_name);
                $('#service_name').val('');
                $('#file_name').val('');
                $("#output").html(response);
            },
            error: function(request, ajaxOptions, thrownError) {
                $("#output").html(request.responseText);
            }
        });
    }

    function upload_file() {
        // var form = $('form')[0]; // You need to use standard javascript object here
        // var formData = new FormData(form);
        // var form = $('form').get(0); 
        var formData = new FormData();
        formData.append('file', $('#file')[0].files[0]);

        $.ajax({
            url: 'service_upload.py',
            type: 'post',
            processData: false,
            contentType: false,
            data: formData,
            success: function(response) {
                console.log(file);
                $('#file').val('');
                $("#output_upload").html(response);
            },
            error: function(request, ajaxOptions, thrownError) {
                $("#output_upload").html(request.responseText);
            }
        });
    }

    function distribute_file() {
        $.ajax({
            url: 'service_distribute.py',
            success: function(response) {
                console.log("Success distribute file");
            },
            error: function(request, ajaxOptions, thrownError) {
                $("#output_upload").html(request.responseText);
            }
        });
    }


    $("#start").click(function() {
        output = insert_service();
    });

    $("#upload_btn").click(function() {
        output_upload = upload_file();
        distribute_upload = distribute_file();
    });
});
</script>
"""
