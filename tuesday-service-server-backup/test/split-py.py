youtube = """[youtube] 1O2NlSRb-6o: Downloading webpage\n
[youtube] 1O2NlSRb-6o: Downloading video info webpage\n
[download] Destination: /Applications/XAMPP/xamppfiles/htdocs/python/python-cgi-monitor/tuesday-service-server/video/sample.mp4\n
[download] 100% of 161.16MiB in 00:31\n
status=1, upload=4883634.9582\n"""

happy = "status=1, upload=4883634.9582\n"

# print happy.split('\n')[0]


def parse_parameter(stdout):  # be improve to return tuple of insert
    dict_result = {'status': None,
                   'rtt': None,
                   'download': None,
                   'upload': None,
                   'other': None,
                   'other_description': None,
                   'other_unit': None,
                   }

    stdout += '\n'
    results = stdout.split('\n')[0].replace(' ', '').split(',')

    print "----------------> result in parse parameter", results

    map(lambda item: dict_result.update({item.split('=')[0]: float(
        item.split('=')[1]) if 'none' not in item.lower() else None}), results)

    pattern = (None, dict_result['status'],
               dict_result['rtt'], dict_result['download'], dict_result['upload'], dict_result['other'],
               dict_result['other_description'], dict_result['other_unit'])

    print pattern

parse_parameter(youtube)
parse_parameter(happy)