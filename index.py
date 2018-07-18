#!/Applications/XAMPP/xamppfiles/htdocs/python/venv/bin/python
import cgi
from easysnmp import Session
# import ntplib
from time import ctime


list_temp = []
first_dict = {}

def create_dict(dict, file):
    with open(file) as f:
        for line in f:
            key, value = line.strip().split()
            dict[key] = value


create_dict(first_dict, "oid_list.txt")

val = str(first_dict.__len__() - 1)

print "Content-type: text/html\n\n"

# Javascript use for checkbox all disable
print '''
<script type="text/javascript">
function check_all()
{
    for(i=0;i<''' + (val) + ''';i++)
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
print '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>'
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
print '<form method="POST" action="test-back.py" target="_blank">'
print '''
                <div class="columns">
                    <div class="column is-6">
                        <div class="field">
                            <label class="label">
                                Fill ip address of router that you want to monitor.
                            </label>
                            <div class="field is-grouped">
                                <div class="control is-expanded">
                                    <input id="ipaddress" name="ipaddress" class="input is-rounded" type="text" placeholder="ex. 192.168.10.1" />
                                </div>
                                <div class="control is-expanded">
                                    <a class="button is-link" id="add_fields">Add</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="columns">
                    <div class="column is-5">
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
                                    <input type="checkbox" name="interface" id="check_4"> interface
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
print '</div>'
print '</section>'
print '</body>'
print '</html>'
print '<script type="text/javascript">'
print '$(".example").html("' + val + '")'
print '</script>'
