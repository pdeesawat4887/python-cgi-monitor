#!/usr/bin/python

import cgi
from easysnmp import Session
import ast
import main.devices as walker
import main.interfaces_test as int_walker

print "Content-type: text/html\n\n"

CONVERT = 1048576


def snmp_walk(ip, community, oid):
    tester = walker.Device()
    if community != None:
        tester.community_string(community)
    return tester.walkthrongh(ip, oid)


def body_interface(ip):
    walk_int = int_walker.Interface()
    walk_int.loadDictionary('/var/www/cgi-bin/main/conf/mapping_int')
    walk_int.operation(ip, form_community, 2)
    print """
        <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
            <thead>
              <tr class="is-selected">
                <th class="has-text-centered">#</th>
                <th>Description</th>
                <th>Type</th>
                <th>Speed (Mbps)</th>
                <th>AdminStatus</th>
                <th>OperaStatus</th>
              </tr>
            </thead>
            <tbody>
    """
    for temp in range(len(walk_int.result_desc)):
        print"""
                <tr><td class="has-text-centered">{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>
        """.format(temp + 1, walk_int.result_desc[temp].value,
                   walk_int.typeList[
                       int(walk_int.result_Type[temp].value)],
                   round(float(walk_int.result_Speed[
                         temp].value) / CONVERT, 2),
                   walk_int.case[int(walk_int.result_Admin[temp].value)],
                   walk_int.case[int(walk_int.result_Opera[temp].value)])
    walk_int.__del__()
    print """</tbody>
        </table><br>"""


def body_other(ip, target):
    print """<table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
            <thead>
              <tr class="is-selected">
                <th>OID</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>"""
    result = snmp_walk(ip, form_community, target)
    for temp in result:
        print """<tr><td>{}</td><td>{}</td></tr>""".format(temp.oid, temp.value)
    result = []
    print"""
            </tbody>
        </table><br>"""


def header():
    print """<!DOCTYPE html>
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
</head>"""

form = cgi.FieldStorage()
form_ip_address = form.getvalue('ipaddress')
form_community = form.getvalue('community')
form_oid = form.getvalue('oid')
form_droplist = form.getvalue('droplist')

ip_list = form_ip_address.split(',')

main_func = []

if form_oid != None:
    oid_list = form_oid.split(',')
    main_func.extend(oid_list)
if form_droplist != None:
    main_func.append(form_droplist)

print """
<section class="section" id="display">
    <div class="container">
        <p class="title"><strong>Walking Result!</strong></p>
        <p class="title is-6"><strong>IP Address: {}</strong></p>
        <p class="title is-6"><strong>OID: {}</strong></p>""".format((', '.join(ip_list)), (', '.join(main_func)))
header()

for ip in ip_list:
    format_ip = ip.replace(' ', '')
    for target in main_func:
        format_target = target.replace(' ', '')
        print """<p class="title is-6"><strong>IP Address: {} OID: {}</strong></p>""".format(format_ip, format_target)
        if target != 'interfaces':
            body_other(format_ip, format_target)
        else:
            body_interface(format_ip)

print"""
    </div>
</section>"""