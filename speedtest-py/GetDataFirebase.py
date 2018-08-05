import firebase

url = 'https://pythontestcode.firebaseio.com/'
connection = firebase.FirebaseApplication(url)

node = []

see = 'download'

result = connection.get('/AmnatCharoen/speedtest/Bangkok', None)

print result

for i in result:
    print result[i][see][0]