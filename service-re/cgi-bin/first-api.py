#!/usr/bin/python

from bottle import run, get, post ,request
employee  =  [{'name' : 'Sam','address':'Ranchi','Dept':'HR'},
              {'name': 'Sarah', 'address': 'Ranchi', 'Dept': 'MGR'},
              {'name': 'Arsh', 'address': 'Delhi', 'Dept': 'HR'}]

@get('/number')
def getAllEmployee():
    return{'employees':employee}

@get('/employee/<name>')
def get_Emp_by_name(name):
    the_emp = [emp for emp in employee if emp['name'] == name]
    return{'employee' : the_emp[0]}

run(reloader=True, debug=True)