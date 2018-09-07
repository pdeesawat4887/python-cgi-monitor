#!/usr/bin/python

def header():
    print '''Content-type: text/html\n
<!DOCTYPE html>
<html class="has-navbar-fixed-top" lang="en">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Monitoring</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.1/css/bulma.min.css">
    <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="../css/canvasjs.min.js"></script>
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.1.1/css/all.css" integrity="sha384-O8whS3fhG2OnA5Kas0Y9l3cfpmYjapjI0E4theH4iuMD+pLhbf6JI0jIMfYcK3yZ"
        crossorigin="anonymous">
</head>
<body>'''

def nav_bar():
    print '''<nav class="navbar is-fixed-top is-dark">
    <div class="container is-fluid">
        <div class="navbar-brand">
            <a class="navbar-item" id="dashboard">
                Dashboard
            </a>
            <div class="navbar-burger" data-target="navMenu">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
        <div id="navMenu" class="navbar-menu">
            <div class="navbar-start">
                <a class="navbar-item" id="probe">
                    Probes
                </a>
                <a class="navbar-item" id="service">
                    Services
                </a>
            </div>
            <div class="navbar-end">
                <a class="navbar-item" id="admin">
                    Admin
                </a>
            </div>
        </div>
    </div>
</nav>'''

def container():
    print '''<div class="container" id="content"></div>'''

def footer():
    print '''<script>
    $(document).ready(function () {
        // Check for click events on the navbar burger icon
        $(".navbar-burger").click(function () {
            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            $(".navbar-burger").toggleClass("is-active");
            $(".navbar-menu").toggleClass("is-active");
        });

        $("#probe").on('click', function () {
            $.ajax({
                url: 'probe_list.py',
                type: 'post',
                success: function (response) {
                    $("#content").html(response);
                    console.log('Success')
                }
            });
        });

        $("#admin").on('click', function () {
            $.ajax({
                url: 'admin.py',
                type: 'post',
                success: function (response) {
                    $("#content").html(response);
                    console.log('Success')
                }
            });
        });
    });
</script>
</body>

</html>'''



header()
nav_bar()
container()
footer()
