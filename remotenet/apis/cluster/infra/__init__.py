from abc import ABC, abstractmethod
from typing import Any, Dict, List

from apis.models import (
    AddContainerModel, AddTunnelModel, AddWorkerModel, 
    ContainerModel, TunnelModel, WorkerModel
)


class Repository(ABC):
    @abstractmethod
    def add_container(self, model: AddContainerModel) -> ContainerModel:
        pass
    
    @abstractmethod
    def remove_container(self, id: int):
        pass

    @abstractmethod
    def get_containers(self) -> List[ContainerModel]:
        pass

    @abstractmethod
    def get_container_by_name(self, name: str) -> 'ContainerModel | None':
        pass
    
    @abstractmethod
    def get_container_by_ip(self, ip: str) -> 'ContainerModel | None':
        pass

    

    @abstractmethod
    def add_tunnel(self, model: AddTunnelModel) -> TunnelModel:
        pass
    
    @abstractmethod
    def remove_tunnel_by_id(self, id: int):
        pass
    
    @abstractmethod
    def remove_tunnels_by_worker_id(self, worker_id: int):
        pass


    
    @abstractmethod
    def add_worker(self, model: AddWorkerModel) -> WorkerModel:
        pass
    
    @abstractmethod
    def remove_worker(self, id: int):
        pass

    @abstractmethod
    def get_worker_by_id(self, id: int) -> 'WorkerModel | None':
        pass
    
    @abstractmethod
    def get_worker_by_name(self, name: str) -> 'WorkerModel | None':
        pass

    @abstractmethod
    def get_worker_by_url(self, url: str) -> 'WorkerModel | None':
        pass

    @abstractmethod
    def get_workers(self) -> List[WorkerModel]:
        pass
    
    @abstractmethod
    def update_worker(self, model: WorkerModel):
        pass
