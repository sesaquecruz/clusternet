import socket
from mininet.net import Containernet
from mininet.node import Docker, Host


def get_hostname() -> str:
    return socket.gethostname()


class ContainernetWorker(Containernet):
    def __init__(self, **params):
        super().__init__(**params)
        self.is_running = False
    
    def getDocker(self, name: str) -> Docker:
        return self[name]

    def getHost(self, name: str) -> Host:
        return self[name]

    def start(self):
        super().start()
        self.is_running = True

    def stop(self):
        super().stop()
        self.is_running = False


worker = ContainernetWorker(topo=None, build=False)


class WorkerInstance:
    @staticmethod
    def instance():
        return worker

    @staticmethod
    def clear_instance():
        global worker
        worker = ContainernetWorker(topo=None, build=False)

