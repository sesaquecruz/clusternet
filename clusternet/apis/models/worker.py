from typing import Any, Dict, List

from clusternet.apis.models.container import ContainerModel
from clusternet.apis.models.helpers import get_ipv4_address
from clusternet.apis.models.tunnel import TunnelModel


class WorkerModel:
    id: int
    name: str
    ip: str
    controller_ip: str
    controller_port: int
    url: str
    is_running: bool
    containers: List[ContainerModel]
    tunnels: List[TunnelModel]

    def __init__(self, id: int, name: str, ip: str, controller_ip: str, controller_port: int, 
        url: str, is_running: bool,
        containers: List[ContainerModel] = [], 
        tunnels: List[TunnelModel] = []
    ):
        self.id              = id
        self.name            = name
        self.ip              = get_ipv4_address(ip)
        self.controller_ip   = get_ipv4_address(controller_ip)
        self.controller_port = controller_port
        self.url             = url
        self.is_running      = is_running
        self.containers      = containers
        self.tunnels         = tunnels

    @property
    def switch(self) -> str:
        return f's{self.id+1}'

    def start(self):
        self.is_running = True
    
    def stop(self):
        self.is_running = False

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return WorkerModel(**data) 

    def to_dict(self) -> Dict[str, Any]:
        containers = list(map(lambda container: container.to_dict(), self.containers))
        tunnels    = list(map(lambda tunnel: tunnel.to_dict(), self.tunnels))
        
        return {
            'id': self.id,
            'name': self.name,
            'switch': self.switch,
            'ip': self.ip,
            'controller_ip': self.controller_ip,
            'controller_port': self.controller_port,
            'url': self.url,
            'is_running': self.is_running,
            'containers': containers,
            'tunnels': tunnels
        }



class AddWorkerModel:
    name: str
    ip: str
    controller_ip: str
    controller_port: int
    url: str
    is_running: bool

    def __init__(self, name: str, ip: str, controller_ip: str, controller_port: int, 
        is_running: bool = False) -> None:
        self.set_name(name)
        self.set_ip(ip)
        self.set_controller_ip(controller_ip)
        self.set_controller_port(controller_port)
        self.set_url()
        self.set_is_running(is_running)

    def set_name(self, name: str):
        if(name == ''): raise Exception('Param name must be non empty')
        self.name = name
    
    def set_ip(self, ip: str):
        self.ip = get_ipv4_address(ip)

    def set_controller_ip(self, ip: str):
        self.controller_ip = get_ipv4_address(ip)

    def set_controller_port(self, port: int):
        self.controller_port = port

    def set_url(self):
        self.url = f'http://{self.ip}:5000' 

    def set_is_running(self, is_running: bool):
        self.is_running = is_running

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return AddWorkerModel(**data)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'ip': self.ip,
            'controller_ip': self.controller_ip,
            'controller_port': self.controller_port,
            'url': self.url,
            'is_running': self.is_running
        }
