#!/usr/bin/python

import main.probe as probe
import os

class Worker(probe.Probe):

    def __init__(self):
        probe.Probe.__init__(self)
        self.mapping_service = dict(self.select('service', None, 'service_id', 'file_name'))

    def get_active_service(self):
        list_service = []

        condition = "probe_id = %s and running = '0'"
        temp_service = self.select('running_service', condition, 'service_id', probe_id=self.id)

        for service_id in temp_service:
            list_service.append(service_id[0])
        return list_service

    def working_active_service(self, service_id):

        command = "python " + self.path + '/' + self.mapping_service[int(service_id)]
        os.system(command)

    def work(self):
        list_service = self.get_active_service()

        for service in list_service:
            self.working_active_service(service)

if __name__ == '__main__':
    worker = Worker()
    worker.work()
