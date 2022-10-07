from typing import List
import httpx

from clusternet.apis.models.container import ContainerModel
from clusternet.client.container import RemoteContainer
from clusternet.client.worker import RemoteWorker

class Cluster:
    def __init__(self, cluster_url: str) -> None:
        self.cluster_url = cluster_url
        self.workers: List[RemoteWorker] = []
        self.client = httpx.Client()

    def create_worker(self, name: str, ip: str, controller: str, port: int) -> RemoteWorker:
        data = {'name': name, 'ip': ip, 'controller_ip': controller, 'controller_port': port}
        response = self.client.post(url=f'{self.cluster_url}/workers', json=data)
        
        if(response.is_error):
            raise Exception(response.json()['error'])
        
        print(f'** {response.json()["content"]}')
        worker = RemoteWorker(cluster=self.cluster_url, **data)
        self.workers.append(worker)
        return worker


    def create_tunnel(self, worker1: RemoteWorker, worker2: RemoteWorker):
        data = {'remote_worker': worker2.name}
        response = self.client.post(url=f'{self.cluster_url}/workers/{worker1.name}/tunnel', json=data)

        if(response.is_error):
            raise Exception(response.json()['error'])
        print(f'** {response.json()["content"]}')


    def get_container(self, name: str) -> RemoteContainer:
        response = self.client.get(url=f'{self.cluster_url}/containers/{name}')
        if(response.is_error):
            raise Exception(response.json()['error'])

        data = response.json()['content']
        return RemoteContainer(self.cluster_url, ContainerModel.from_dict(data))

    
    def remove(self, worker: RemoteWorker):
        response = self.client.delete(url=f'{self.cluster_url}/workers/{worker.name}')
        
        if(response.is_error):
            raise Exception(response.json()['error'])
        print(f'** {response.json()["content"]}')
    

    def start(self):
        for worker in self.workers:
            worker.start()

    def stop(self):
        for worker in self.workers:
            if(worker.is_running):
                worker.stop()
            self.remove(worker)
        
        self.client.close()
