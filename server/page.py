#!/usr/bin/python

print '''Content-type: text/html\n'''

def header():
    print '''<!DOCTYPE html>
<html class="has-navbar-fixed-top" lang="en" style="height: 100%;">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Monitoring</title>
    <link rel="stylesheet" href="../css/bulma.css">
    <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="../css/canvasjs.min.js"></script>
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.1.1/css/all.css" integrity="sha384-O8whS3fhG2OnA5Kas0Y9l3cfpmYjapjI0E4theH4iuMD+pLhbf6JI0jIMfYcK3yZ"
        crossorigin="anonymous">
</head>'''

def footer():
    print '''        <script>
            $(document).ready(function () {
                $.ajax({
                    url: 'dashboard.py',
                    type: 'post',
                    success: function (response) {
                        $("#display").html(response);
                    }
                });
                $("#dashboard").on('click', function () {
                    $.ajax({
                        url: 'dashboard.py',
                        type: 'post',
                        success: function (response) {
                            $("#display").html(response);
                        }
                    });
                });          
                $("#list_probe").on('click', function () {
                    $.ajax({
                        url: 'list_probe.py',
                        type: 'post',
                        success: function (response) {
                            $("#display").html(response);
                        }
                    });
                });
                $("#inventory").on('click', function () {
                    $.ajax({
                        url: '../snmp.html',
                        type: 'post',
                        success: function (response) {
                            $("#display").html(response);
                        }
                    });
                });
                $("#admin").on('click', function () {
                    $.ajax({
                        url: 'admin.py',
                        type: 'post',
                        success: function (response) {
                            $("#display").html(response);
                        }
                    });
                });
            });
        </script>
</body>

</html>'''

def navbar():
    print '''<body style="min-height: 100%; background-color: #dfab7a">
    <nav class="navbar is-fixed-top is-dark">
        <div class="container is-fluid">
            <div class="navbar-brand">
                <a class="navbar-item" id="dashboard">
                <span class="icon is-medium">
                    <i class="fas fa-desktop"></i>
                </span>
                <spam>
                    Dashboard
                </span>
                </a>
                <div class="navbar-burger" data-target="navMenu">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
            <div id="navMenu" class="navbar-menu">
                <div class="navbar-start">
                    <a class="navbar-item" id="list_probe">
                    <span class="icon is-medium">
                        <i class="fas fa-project-diagram"></i>
                    </span>
                    <span>
                        Probes
                    </span>
                    </a>
                    <a class="navbar-item" id="inventory">
                    <span class="icon is-medium">
                        <i class="fas fa-search"></i>
                    </span>
                    <span>
                        Inventory
                    </span>
                    </a>
                </div>
                <div class="navbar-end">
                    <a class="navbar-item" id="admin">
                    <span class="icon is-medium">
                        <i class="fas fa-user-circle"></i>
                    </span>
                    <span>
                        Admin
                    </span>
                    </a>
                </div>
            </div>
        </div>
    </nav>'''

def container():
    print '''    <section class="section" id="display">
    </section>'''

header()
navbar()
container()
footer()