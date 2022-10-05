
from typing import Any, Dict

from clusternet.apis.models.helpers import get_ipv4_address


class ContainerModel:
    id: int
    worker_id: int
    name: str
    ip: str
    dimage: str
    cpu_period: int
    cpu_quota: int
    mem_limit: int

    def __init__(self, id: int, worker_id: int, name: str, ip: str,
        dimage: str, cpu_period: int, cpu_quota: int, mem_limit: int) -> None:
        self.id         = id
        self.worker_id  = worker_id
        self.name       = name
        self.ip         = get_ipv4_address(ip)
        self.dimage     = dimage
        self.cpu_period = cpu_period
        self.cpu_quota  = cpu_quota
        self.mem_limit  = mem_limit
    

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return ContainerModel(**data) 

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'worker_id': self.worker_id,
            'name': self.name,
            'ip': self.ip,
            'dimage': self.dimage,
            'cpu_period': self.cpu_period,
            'cpu_quota': self.cpu_quota,
            'mem_limit': self.mem_limit
        }

    def __repr__(self) -> str:
        return f'ContainerModel(name={self.name}, ip={self.ip}, dimage={self.dimage})'


class AddContainerModel:
    worker_id: int
    name: str
    ip: str
    dimage: str
    cpu_period: int
    cpu_quota: int
    mem_limit: int

    def __init__(self, worker_id: int, name: str, ip: str,
        dimage: str, cpu_period: int, cpu_quota: int, mem_limit: int) -> None:
        self.set_worker_id(worker_id)
        self.set_name(name)
        self.set_ip(ip)
        self.set_docker_image(dimage)
        self.set_cpu_period(cpu_period)
        self.set_cpu_quota(cpu_quota)
        self.set_mem_limit(mem_limit)
    

    def set_worker_id(self, id: int):
        self.worker_id = id

    def set_name(self, name: str):
        if(name == ''): raise Exception('Param name must be non empty')
        self.name = name
    
    def set_ip(self, ip: str):
        self.ip = get_ipv4_address(ip)
    
    def set_docker_image(self, image: str):
        if(image == ''): raise Exception('Param dimage must be non empty')
        self.dimage = image
    
    def set_cpu_period(self, value: int):
        self.cpu_period = value

    def set_cpu_quota(self, value: int):
        self.cpu_quota = value
    
    def set_mem_limit(self, value: int):
        self.mem_limit = value

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return AddContainerModel(**data) 

    def to_dict(self) -> Dict[str, Any]:
        return {
            'worker_id': self.worker_id,
            'name': self.name,
            'ip': self.ip,
            'dimage': self.dimage,
            'cpu_period': self.cpu_period,
            'cpu_quota': self.cpu_quota,
            'mem_limit': self.mem_limit
        }