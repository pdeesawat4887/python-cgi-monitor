#!/usr/bin/python

import cgi
import cgitb
import os
import sys

print "Content-Type: text/html\n"

UPLOAD_DIR = '../upload'


def save_uploaded_file():
    form = cgi.FieldStorage()
    if not form.has_key('file'):
        print """<p class="title is-6">Not found parameter: file</p>"""
        return

    form_file = form['file']
    if not form_file.file:
        print """<p class="title is-6">Not found parameter: file</p>"""
        return

    if not form_file.filename:
        print """<p class="title is-6">Not found parameter: file</p>"""
        return

    uploaded_file_path = os.path.join(
        UPLOAD_DIR, os.path.basename(form_file.filename))
    with file(uploaded_file_path, 'wb') as fout:
        while True:
            chunk = form_file.file.read(100000)
            if not chunk:
                break
            fout.write(chunk)
    print '<p class="title is-6">Completed file upload {} </p>'.format(form_file.filename)

if __name__ == '__main__':
    cgitb.enable()
    save_uploaded_file()
