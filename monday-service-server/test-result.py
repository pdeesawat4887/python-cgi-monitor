import main.database as mariadb
import time

probe_id = 'abc123'
service_id = '1'
start_date = time.strftime('%Y-%m-%d %H:%M:%S')
result = []


def parse_parameter(destination_id, stdout):  # be improve to return tuple of insert
    dict_result = {'status': None,
                   'rtt': None,
                   'download': None,
                   'upload': None,
                   'other': None,
                   'other_description': None,
                   'other_unit': None,
                   }

    results = stdout.replace(' ', '').replace('\n', '').split(',')

    map(lambda item: dict_result.update(
        {item.split('=')[0]: item.split('=')[1] if 'none' not in item.lower() else None}), results)

    pattern = (None, probe_id, service_id, start_date, destination_id, dict_result['status'],
               dict_result['rtt'], dict_result['download'], dict_result['upload'], dict_result['other'],
               dict_result['other_description'], dict_result['other_unit'])
    result.append(pattern)

destination_id = 1
stdouts = ["status=1, rtt=0.128",
           "status=1, rtt=21, download=100, upload= 50",
           "status=1, rtt=4, upload=6",
           "status=1, other=123456789, other_description=external_output, other_unit=sec"]

for i in stdouts:
    parse_parameter(destination_id, i)

db = mariadb.MySQLDatabase()
db.insert('TESTRESULTS', result)

