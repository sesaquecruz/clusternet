from typing import Any, Dict


class TunnelModel:
    id: int
    port_name: str
    remote_ip: str
    worker_id: int

    def __init__(self, id: int, worker_id: int, port_name: str, remote_ip: str) -> None:
        self.id        = id
        self.worker_id = worker_id
        self.port_name = port_name
        self.remote_ip = remote_ip
    
    @property
    def interface(self) -> str:
        return f'{self.port_name}-gre{self.id+1}'

    @property
    def command(self) -> str:
        port = self.port_name
        interface = self.interface
        ip = self.remote_ip
        return f'ovs-vsctl add-port {port} {interface} -- set interface {interface} type=gre options:remote_ip={ip}'
    

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return TunnelModel(**data) 

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'worker_id': self.worker_id,
            'port_name': self.port_name,
            'remote_ip': self.remote_ip,

        }


class AddTunnelModel:
    def __init__(self, worker_id: int, port_name: str, remote_ip: str) -> None:
        self.worker_id = worker_id
        self.port_name = port_name
        self.remote_ip = remote_ip
    
    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return AddTunnelModel(**data) 

    def to_dict(self) -> Dict[str, Any]:
        return {
            'worker_id': self.worker_id,
            'port_name': self.port_name,
            'remote_ip': self.remote_ip,
        }