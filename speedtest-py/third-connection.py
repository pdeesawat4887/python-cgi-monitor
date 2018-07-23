from firebase import firebase

def connection():
    connection = firebase.FirebaseApplication('https://pythonwithfirebase-catma.firebaseio.com')
    test = 'google'
    # connection.post('/speedtest/changmai', {'download':111, 'upload':222, 'ping':90, 'time':1827})
    connection.put('speedtest', 'Changrai/'+test, {'download':1111111, 'upload':2222222, 'ping':8080, 'time':1928376})

connection()