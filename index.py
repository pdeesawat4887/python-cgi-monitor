#!/usr/bin/env python
import cgi

from easysnmp import Session

print "Content-type: text/html\n\n"
print '<!DOCTYPE html>'
print '<html>'
print '<head>'
print '<meta charset="utf-8">'
print '<meta name="viewport" content="width=device-width, initial-scale=1">'
print '<title>AIT-CATMA</title>'
print '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.1/css/bulma.min.css">'
print '<script defer src="https://use.fontawesome.com/releases/v5.1.0/js/all.js"></script>'
print '</head>'
print '<body>'
print '<section class="section">'
print '<div class="container">'
print '<h1 class="title">'
print 'Hello SNMP at CATMA'

print '</h1>'
print '<p class="subtitle">'
print 'My first website with <strong>Bulma</strong>!'
print '</p>'
print '<br><br>'
print '<form method="POST" action="index.py">'
print '<p>Fill ip address of router that you want to monitor.</p><br>'
print '<p><input name="ipaddress" class="input is-rounded" type="text" placeholder="ex. 192.168.10.1"/></p><br>'
print '<p><input type="submit" class="button is-primary" values="submit" />'
print '</form>'


form = cgi.FieldStorage()
if form.getvalue("ipaddress"):
    ipaddress = form.getvalue('ipaddress')
    print '<br><h1> You want to monitor router that contain ip address <strong>'+ipaddress+'.</strong> Wait a min ... </h1><br>'

print '</div>'
print '</section>'
print '</body>'
print '</html>'



class Router:

    def __init__(self, host, community, version):
        self.host = host
        self.community = community
        self.version = version
        self.session =  Session(hostname=self.host,
                               community=self.community, version=self.version)

    # def walkthrough(self):
    #     pass