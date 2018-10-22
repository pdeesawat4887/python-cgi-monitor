import socket
import time
import main.database as mariadb

def udp_work(destination, destination_port):

    udp_cmd = "Hello UDP Server"

    stdout = "status={status_final}"

    msg_from_client = udp_cmd
    bytes_to_send = str.encode(msg_from_client)
    server_address_port = (destination, destination_port)
    buffer_size = 1024

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.settimeout(1)

    start_time = time.time()
    UDPClientSocket.sendto(bytes_to_send, server_address_port)

    try:
        msg_from_server = UDPClientSocket.recvfrom(buffer_size)
        end_time = time.time()
        status_final = 1
        stdout += ', rtt={rtt}'.format(rtt=end_time - start_time)
    except:
        status_final = 3
    finally:
        UDPClientSocket.close()

    return stdout.format(status_final=status_final)

output = udp_work('127.0.0.1', 20001)

info_test_result = []
probe_id = 'abc123'
service_id = '1'
start_date = time.strftime('%Y-%m-%d %H:%M:%S')
destination_id = '1'


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

    map(lambda item: dict_result.update({item.split('=')[0]: float(
        item.split('=')[1]) if 'none' not in item.lower() else None}), results)

    pattern = (None, probe_id, service_id, start_date, destination_id, dict_result['status'],
               dict_result['rtt'], dict_result['download'], dict_result['upload'], dict_result['other'],
               dict_result['other_description'], dict_result['other_unit'])

    info_test_result.append(pattern)

parse_parameter(destination_id, output)


db = mariadb.MySQLDatabase()
db.insert('TESTRESULTS', info_test_result)

# print info_test_result