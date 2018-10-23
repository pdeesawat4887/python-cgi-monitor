import main.database as maria

def statement1():
    db = maria.MySQLDatabase()

    db.insert('PROBES', [('hello20', '', '','',3, 'NOW()', 'NOW()', None)])

    update = 'UPDATE PROBES SET collection_number="abc" where probe_id="hello20"'
    db.mycursor.execute(update)

    all_probe = db.select("SELECT distinct(collection_number) FROM PROBES")

    list_services = map(lambda item: item[0], db.select("SELECT `service_id` FROM SERVICES"))
    list_run_svc = map(lambda item: (all_probe[0][0], item, 2), list_services)
    # print list_run_svc
    db.insert('RUNNING_SERVICES', list_run_svc)


    list_destinations = map(lambda item: item[0], db.select("SELECT `destination_id` FROM DESTINATIONS"))
    list_run_dest = map(lambda item: (all_probe[0][0], item, 1), list_destinations)
    # print list_run_dest
    db.insert('RUNNING_DESTINATIONS', list_run_dest)


    db.mycursor.execute("set FOREIGN_KEY_CHECKS=0;")
    db.mycursor.execute("DELETE FROM PROBES WHERE probe_id='hello20'")
    db.mycursor.execute("set FOREIGN_KEY_CHECKS=1;")

    db.connection.commit()

def statement2():
    db = maria.MySQLDatabase()
    db.insert('PROBES', [('hello48', '', '', '', 3, 'NOW()', 'NOW()', None)])
    update1 = 'UPDATE PROBES SET collection_number="abc" where probe_id="hello48"'
    db.mycursor.execute(update1)
    db.connection.commit()

    update2 = 'UPDATE PROBES SET collection_number="newcollection.bkk" where probe_id="hello48"'
    db.mycursor.execute(update2)
    db.connection.commit()

# statement1()
# statement2()

db = maria.MySQLDatabase()
# output = db.select("SELECT * FROM PROBES WHERE probe_id='hello';")

# db.mycursor.execute("SELECT @@GLOBAL.foreign_key_checks;")
db.mycursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
db.mycursor.execute("DELETE FROM SERVICES WHERE service_id=3;")
db.mycursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
db.connection.commit()