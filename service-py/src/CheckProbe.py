import __Distribution__
import ICMPService
import threading
import requests


class CheckProbe(__Distribution__.Server):

    def __init__(self):
        __Distribution__.Server.__init__(self)

    def check_ping(self, ip_address):
        ping = ICMPService.ICMPService()
        status, response = ping.get_status(destination=ip_address, port=None)
        return status

    def check_probe_alive(self, id, ip):

        if self.check_ping(ip) == 1:
            update_sql = "UPDATE probe SET status='{}' WHERE probe_id='{}'".format(1, id)
            self.mycursor.execute(update_sql)
            self.connection.commit()
            print 'probe id {} is Inactive'.format(id)

    def get_warning_from_baseline(self):

        query_sql_perf = "SELECT probe_name, ip_address, service_name, destination, destination_port, location, ping, download, upload, time" \
                         " FROM performance_service" \
                         " inner join destination on destination.destination_id=performance_service.destination_id" \
                         " inner join probe on performance_service.probe_id=probe.probe_id" \
                         " inner join service on destination.service_id=service.service_id" \
                         " where ((ping != 0 and (upload < {} or download < {})) or (ping = 0 and download < {}) )and (time < NOW() - INTERVAL {} MINUTE);".format(
            self.setting['upload_baseline'], self.setting['download_baseline'], self.setting['download_only'],
            self.setting['interval'])

        query_sql_avai = "SELECT probe_name, ip_address, service_name, destination, destination_port, response_time, time " \
                         "FROM availability_service " \
                         "inner join destination on destination.destination_id=availability_service.destination_id " \
                         "inner join probe on availability_service.probe_id=probe.probe_id " \
                         "inner join service on destination.service_id=service.service_id " \
                         "where (availability_service.status != 0 or response_time > {} ) and (time > NOW() - INTERVAL {} MINUTE);".format(
            self.setting['response_time'], self.setting['interval'])

        self.mycursor.execute(query_sql_perf)
        perf_result = self.mycursor.fetchall()

        self.mycursor.execute(query_sql_avai)
        avai_result = self.mycursor.fetchall()

        return avai_result, perf_result

    def notify_me(self, data, type):
        url = 'https://notify-api.line.me/api/notify'
        token = 'pyL4xY6ys303vg0bVnvd0DRco7UyILVo5dOXZGjBWD8'
        headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}

        for warning in data:
            print warning
            if type is 'performance':
                msg = '\nWARNING !!!\nProbe Name: {}\nIP Address: {}\nService: {}\nDestination: {}\nPort: {}\nLocation: {}\nPing: {}\nDownload: {}\nUpload: {}\nTime: {}\nPlease check your service'.format(
                    warning[0], warning[1], warning[2], warning[3], warning[4], warning[5], warning[6], warning[7],
                    warning[8], warning[9])
            else:
                msg = '\nWARNING !!!\nProbe Name: {}\nIP Address: {}\nService: {}\nDestination: {}\nPort: {}\nResponse Time: {}\nTime: {}\nPlease check your service'.format(
                    warning[0], warning[1], warning[2], warning[3], warning[4], warning[5], warning[6])

            request = requests.post(url, headers=headers, data={'message': msg})

    def main(self):

        threads = []
        for probe in self.all_probe:
            id = probe[0]
            ip = probe[1]

            self.check_probe_alive(id, ip)
            t = threading.Thread(target=self.check_probe_alive, args=(id, ip,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()


if __name__ == '__main__':
    checker = CheckProbe()
    # checker.main()
    availability, performance = checker.get_warning_from_baseline()
    checker.notify_me(data=availability, type='availability')
    checker.notify_me(data=performance, type='performance')
