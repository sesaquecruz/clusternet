from typing import List

from mininet.net import Containernet
from mininet.node import Host, RemoteController

from clusternet.apis.models.container import ContainerModel
from clusternet.apis.presentation.protocols import HttpRequest


class ContainernetWorker(Containernet):
    def __init__(self, **params):
        super().__init__(**params)
        self.is_running = False
    
    def getHost(self, name: str) -> Host:
        return self[name]

    def create_containers(self, switch: str, containers: List[ContainerModel]):
        for container in containers:
            if(container.name in self): continue

            container_params = container.to_dict()
            container_params.pop('name')
            self.addDocker(container.name, **container_params)
            self.addLink(container.name, switch)


    def start(self, request: HttpRequest, containers: List[ContainerModel]):
        switch_name     = request.body['switch']
        controller_ip   = request.body['controller_ip']
        controller_port = request.body['controller_port']

        self.addController(name='c0', controller=RemoteController, ip=controller_ip, port=controller_port)
        self.addSwitch(name=switch_name)
        self.create_containers(switch_name, containers)
        super().start()
        self.is_running = True
    

    def stop(self):
        self.is_running = True
        return super().stop()


worker = ContainernetWorker(topo=None, build=False)


class WorkerInstance:
    @staticmethod
    def instance():
        return worker

    @staticmethod
    def clear_instance():
        global worker
        worker = ContainernetWorker(topo=None, build=False)

