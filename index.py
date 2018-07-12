#!/Applications/XAMPP/xamppfiles/htdocs/python/venv/bin/python
import cgi
from easysnmp import Session


class Router:

    def __init__(self, host, community, version):
        self.host = host
        self.community = community
        self.version = version
        self.session = Session(hostname=self.host,
                               community=self.community, version=self.version)

    def walkthrough(self, oid):
        items = self.session.walk(oid)
        return items


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
print '<p class="subtitle">Fill ip address of router that you want to monitor.</p>'
print '<p><input name="ipaddress" class="input is-rounded" type="text" placeholder="ex. 192.168.10.1"/></p><br>'
print '<p class="subtitle">Fill oid in MIB-II that you want to monitor.</p>'
print '<p><input name="oid" class="input is-rounded" type="text" placeholder="system or 1.6.3.9.1"/></p><br>'
print '''
<table class="table is-fullwidth">
<tr>
<th><label class="checkbox"><input type="checkbox" name="system" value="system">  System</label></th>
<th><label class="checkbox"><input type="checkbox" name="icmp" value="icmp">    ICMP</label></th>
</tr>
<tr>
<th><label class="checkbox"><input type="checkbox" name="snmp" value="snmp">    SNMP</label></th> 
<th><label class="checkbox"><input type="checkbox" name="udp" value="udp"> UDP</label></th>
</tr>
<tr>
<th><label class="checkbox"><input type="checkbox" name="aaa" > ALL</label></th>
<th><label class="checkbox"><input type="checkbox" name="bbb" > ALL...</label></th>
</tr>
</table>
'''

print '<p><input type="submit" class="button is-primary" value="submit" />'
print '</form>'

list = []

form = cgi.FieldStorage()

#Get value from textfeild
if form.getvalue("ipaddress"):
    ipaddress = form.getvalue('ipaddress')
    print '<br><h1> You want to monitor router that contain ip address <strong>' + ipaddress + '.</strong> Wait a min ... </h1><br>'
if form.getvalue("oid"):
    oid = form.getvalue('oid')

#Get value from checkbox
if form.getvalue("system"):
    list.append("system")

if form.getvalue("icmp"):
    list.append("icmp")

if form.getvalue("snmp"):
    list.append("snmp")

if form.getvalue("udp"):
    list.append("udp")

if form.getvalue("aaa"):
    list.append("hello")

if form.getvalue("bbb"):
    list.append("world")

print list



print '''
<br>
<table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
  <tr>
    <th>OID</th>
    <th>Description</th> 
  </tr> '''

router = Router(ipaddress, 'public', 2)
info = router.walkthrough(oid)

for item in info:
    print '<tr>' \
          '<td>'+item.oid+'</td>' \
                          '<td>'+item.value+'</td>'
    # print '<p> {:.<50} <strong> {} </strong>'.format(item.oid, item.value)
print '</table>'
print '</div>'
print '</section>'
print '</body>'
print '</html>'
