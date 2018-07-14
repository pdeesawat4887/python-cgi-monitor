#!/Applications/XAMPP/xamppfiles/htdocs/python/venv/bin/python
import cgi
from easysnmp import Session
# import ntplib
from time import ctime

list = []
info = []
dict_oid = {}

# c = ntplib.NTPClient()
# response = c.request('pool.ntp.org')


def create_dict(dict, file):
    with open(file) as f:
        for line in f:
            key, value = line.strip().split()
            dict[key] = value


create_dict(dict_oid, "oid_list.txt")


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
# Javascrip use for checkbox all disable
print '''<script type="text/javascript">
function check_all()
{

    for(i=0;i<4;i++)
    {
        tmp_checkbox_id = "check_"+i;
            //alert(tmp_checkbox_id);
            if(document.getElementById("checkall").checked == true)
            {    
                //alert("hi");
                document.getElementById(tmp_checkbox_id).checked = true;
            }
            else
            {    
                //alert("bye");
                document.getElementById(tmp_checkbox_id).checked = false;
            }

    }
}
</script>'''

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
print '''
                <div class="columns">
                    <div class="column is-4">
                        <div class="field">
                            <label class="label">
                                Fill ip address of router that you want to monitor.
                            </label>
                            <div class="control">
                                <input name="ipaddress" class="input is-rounded" type="text" placeholder="ex. 192.168.10.1" />
                            </div>
                        </div>
                        <div class="field">
                            <label class="label">
                                Fill oid in MIB-II that you want to monitor.
                            </label>
                            <div class="control">
                                <input name="oid" class="input is-rounded" type="text" placeholder="system or 1.6.3.9.1" />
                            </div>
                        </div>
                    </div>
                </div>
'''
print '''
                <div class="columns">
                    <div class="column is-2">
                        <div class="field">
                            <div class="field-body">
                                <label class="checkbox">
                                    <input type="checkbox" name="system" id="check_0"> System
                                </label>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-body">
                                <label class="checkbox">
                                    <input type="checkbox" name="snmp" id="check_1"> SNMP
                                </label>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-body">
                                <label class="checkbox">
                                    <input type="checkbox" name="icmp" id="check_2"> ICMP
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="column is-2">
                        <div class="field">
                            <div class="field-body">
                                <label class="checkbox">
                                    <input type="checkbox" name="udp" id="check_3"> UDP
                                </label>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-body">
                                <label class="checkbox">
                                    <input type="checkbox" name="all" onclick="check_all()" id="checkall"> All
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="columns">
                    <div class="column">
                        <div class="field">
                            <div class="control">
                                <button class="button is-primary">Submit</button>
                            </div>
                        </div>
                    </div>
                </div>
'''
print '</form>'

form = cgi.FieldStorage()

# Get value from textfeild
if form.getvalue("ipaddress"):
    ipaddress = form.getvalue('ipaddress')
    print '<br><h1> You want to monitor router that contain ip address <strong>' + ipaddress + '.</strong> Wait a min ... </h1><br>'

if form.getvalue("oid"):
    oid = form.getvalue('oid')
    list.append(oid)

# Get value from checkbox
if form.getvalue("system"):
    list.append("system")

if form.getvalue("icmp"):
    list.append("icmp")

if form.getvalue("snmp"):
    list.append("snmp")

if form.getvalue("udp"):
    list.append("udp")

print '''
<br>
<table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
  <tr>
    <th>OID</th>
    <th>Description</th>
  </tr>
'''
walker = Router(ipaddress, 'public', 2)

temp_result = []

for oid_spec in list:
    temp_result.append(walker.walkthrough(oid_spec))

for item in temp_result:
    print '<tr class="is-selected"><td><strong>' + list[temp_result.index(item)].upper() + '</strong></td><td></td></tr>'
    for result in item:
        if result.value != '0' and result.value != '0.0.0.0':                                                           # Condition cut-off 0 result
            print '<tr>' \
                  '<td>' + result.oid + '</td>' \
                                        '<td>' + result.value + '</td>'
# Start thinking concept
# temp = []
# info = walker.walkthrough('1.3.6.1.2.1.2.1')
# info2 = walker.walkthrough('1.3.6.1.2.1.1.1')
#
# temp.append(info)
# temp.append(info2)
#
# print(temp)
#
# for i in temp:
#     for x in i:
#         print x.value

# for item in info:
#     print '<tr>' \
#           '<td>'+item.oid+'</td>' \
#                           '<td>'+item.value+'</td>'
# for item in info2:
#     print '<tr>' \
#           '<td>'+item.oid+'</td>' \
#                           '<td>'+item.value+'</td>'

print '</table>'
print '</div>'
print '</section>'
print '</body>'
print '</html>'
