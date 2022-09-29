from mininet.net import Containernet
from mininet.node import Host


class ContainernetWorker(Containernet):
    def __init__(self, **params):
        super().__init__(**params)
        self.is_running = False
    
    def getHost(self, name: str) -> Host:
        return self[name]

    def start(self):
        self.is_running = True
        return super().start()
    
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

