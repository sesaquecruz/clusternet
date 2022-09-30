from threading import Lock
from typing import Any, Dict, List

from remotenet.apis.cluster.infra import Repository
from remotenet.apis.models import (
    AddContainerModel, AddTunnelModel, AddWorkerModel, 
    ContainerModel, WorkerModel, TunnelModel)


class InMemoryRepository(Repository):
    def __init__(self) -> None:
        self.lock = Lock()
        self.tables: Dict[str, List[Dict[str, Any]]] = {
            'workers': [],
            'containers': [],
            'tunnels': []
        }
    
    # ========================================================================= #
    # ================================ Helpers ================================ #
    def _next_id(self, table: str) -> int:
        data = self.tables[table]
        if(not data):
            return 0
        return data[-1]['id'] + 1

    def _get_container_by(self, **params) -> 'ContainerModel | None':
        key, value = params.popitem()
        with self.lock:
            for item in self.tables['containers']:
                if(item[key] == value):
                    return ContainerModel.from_dict(item)
            return None

    def _get_worker_by(self, **params) -> 'WorkerModel | None':
        key, value = params.popitem()
        with self.lock:
            for item in self.tables['workers']:
                if(item[key] == value):
                    id = item['id']
                    item['containers'] = self._get_containers_by_worker(id)
                    item['tunnels'] = self._get_tunnels_by_worker(id)
                    return WorkerModel.from_dict(item)
            return None

    def _get_containers_by_worker(self, worker_id: int) -> List[ContainerModel]:
        return [
            ContainerModel.from_dict(item)
            for item in self.tables['containers']
            if(item['worker_id'] == worker_id)
        ]

    def _get_tunnels_by_worker(self, worker_id: int) -> List[TunnelModel]:
        return [
            TunnelModel.from_dict(item)
            for item in self.tables['tunnels']
            if(item['worker_id'] == worker_id)
        ]
    
    def _remove_collection_by_worker(self, worker_id: int, collection: str):
        for item in self.tables[collection].copy():
            if(item['worker_id'] == worker_id):
                self.tables[collection].remove(item)

    # ========================================================================= #
    # ================================ Workers ================================ #
    def add_worker(self, model: AddWorkerModel) -> WorkerModel:
        with self.lock:
            id = self._next_id('workers')
            worker = WorkerModel(id, **model.to_dict())
            self.tables['workers'].append(worker.to_dict())
            return worker


    def remove_worker(self, id: int):
        with self.lock:
            for item in self.tables['workers'].copy():
                if(item['id'] == id):
                    self._remove_collection_by_worker(id, 'containers')
                    self._remove_collection_by_worker(id, 'tunnels')
                    self.tables['workers'].remove(item)


    def update_worker(self, model: WorkerModel):
        with self.lock:
            for item in self.tables['workers']:
                if(item['id'] == model.id):
                    item.update(**model.to_dict())


    def get_worker_by_ip(self, ip: str) -> 'WorkerModel | None':
        return self._get_worker_by(ip=ip)
    
    
    def get_worker_by_id(self, id: int) -> 'WorkerModel | None':
        return self._get_worker_by(id=id)


    def get_worker_by_name(self, name: str) -> 'WorkerModel | None':
        return self._get_worker_by(name=name)


    def get_workers(self) -> List[WorkerModel]:
        workers = []
       
        for item in self.tables['workers']:
            worker = self.get_worker_by_id(id=item['id'])
            if(worker is not None):
                workers.append(WorkerModel.from_dict(item))
                
        return workers

    # ========================================================================= #
    # ============================== Containers =============================== #
    def add_container(self, model: AddContainerModel) -> ContainerModel:
        with self.lock:
            id        = self._next_id('containers')
            container = ContainerModel(id, **model.to_dict())
            self.tables['containers'].append(container.to_dict())
            return container


    def remove_container(self, id: int):
        with self.lock:
            for item in self.tables['containers'].copy():
                if(item['id'] == id):
                   self.tables['containers'].remove(item)
    

    def get_container_by_name(self, name: str) -> 'ContainerModel | None':
        return self._get_container_by(name=name)

    def get_container_by_ip(self, ip: str) -> 'ContainerModel | None':
        return self._get_container_by(ip=ip)

    def get_containers(self) -> List[ContainerModel]:
        with self.lock:
            return [
                ContainerModel.from_dict(item)
                for item in self.tables['containers']
            ]
        
    # ========================================================================= # 
    # ================================ Tunnels ================================ #
    def add_tunnel(self, model: AddTunnelModel) -> TunnelModel:
        with self.lock:
            id     = self._next_id('tunnels')
            tunnel = TunnelModel(id, **model.to_dict())
            self.tables['tunnels'].append(tunnel.to_dict())
            return tunnel


    def remove_tunnel_by_id(self, id: int):
        with self.lock:
            for item in self.tables['tunnels'].copy():
                if(item['id'] == id):
                   self.tables['tunnels'].remove(item)
    

    def remove_tunnels_by_worker_id(self, worker_id: int):
        return self._remove_collection_by_worker(worker_id, 'tunnels')