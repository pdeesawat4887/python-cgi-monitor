#!/Applications/XAMPP/xamppfiles/htdocs/python/venv/bin/python

import cgi

print 'Content-type: text/html\n\n'
print '<!DOCTYPE html>'
print '<html>'
print '<head>'
print '<meta charset="utf-8">'
print '<meta name="viewport" content="width=device-width, initial-scale=1">'
print '<title>AIT-CATMA</title>'
print '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.1/css/bulma.min.css">'
print '<script defer src="https://use.fontawesome.com/releases/v5.1.0/js/all.js"></script>'
print '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>'
print '<script defer src="https://use.fontawesome.com/releases/v5.1.0/js/all.js"></script>'
print '</head>'
print '<body>'
print '<section class="section">'
print '<div class="container">'
print '<h1 class="title">'
print 'Test SNMP at CATMA'
print '</h1>'
print '<p class="subtitle">'
print 'My first website with <strong>Bulma</strong>!'
print '</p>'
print '<br><br>'

form = cgi.FieldStorage()

print form['ipaddress'].value
print form['oid'].value
print form['droplist'].value

print '<br><br>'
print '<div class="column" id="table"> jjj </div>'


print '</div>'
print '</section>'
print '</body>'
print '</html>'
