#!/Applications/XAMPP/xamppfiles/htdocs/python/venv/bin/python
import cgi


def main():
    print "Content-type: text/html\n"
    print "<h1>Hello</h1>"


def main2():
    f = open("C:/junk/t4.html", 'w')
    form = cgi.FieldStorage()
    f.write(str(len(form)))
    if form.has_key("firstname"):
        m = "<h1>Hello</h1>"
        f.write(m)
    else:
        f.write("hello")
        f.close()


main()

