#!/usr/bin/python

import cgi
import bcrypt
import requests
import json

print 'Content-type: text/html\n'

# form = cgi.FieldStorage()
# username = form.getvalue('username')
# password = form.getvalue('password')
# role = form.getvalue('role')
username = "PythonTest"
password = "PythonPassword"
role = "Guest"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)
# condition = {"uid": username,
#              "pswrd": hashed,
#              "privil": "Admin"}
temp = {'val': {"uid": username,
             "pswrd": hashed,
             "privil": "Admin"}}
headers = {'Content-type': 'application/json'}
r = requests.post("http://172.16.30.176/api-man/persty", json=temp)
print r.text
# print r.json()
print "success"
