import httpx

from clusternet.client.container import RemoteContainer
from clusternet.client.worker import RemoteWorker

class Cluster:
    def __init__(self, cluster_url: str) -> None:
        self.cluster_url = cluster_url
        self.workers: list[RemoteWorker] = []
        self.containers: dict[str, RemoteContainer] = {}
        self.client = httpx.Client()

    def create_worker(self, name: str, ip: str, controller: str, port: int):
        data = {'name': name, 'ip': ip, 'controller_ip': controller, 'controller_port': port}
        response = self.client.post(url=f'{self.cluster_url}/workers', json=data)
        
        if(response.is_error):
            raise Exception(response.json()['error'])
        
        self.workers.append(RemoteWorker(cluster=self.cluster_url, **data))
        print(response.json()['content'])


    def create_container(self, name: str, worker: str, **params):
        data = {'name': name, 'worker_name': worker, **params}
        response = self.client.post(url=f'{self.cluster_url}/containers', json=data)

        if(response.is_error):
            raise Exception(response.json()['error'])
        
        self.containers[name] = RemoteContainer(self.cluster_url, name, worker)
        print(response.json()['content'])


    def create_tunnel(self, worker: str, remote_ip: str):
        data = {'worker_name': worker, 'remote_ip': remote_ip}
        response = self.client.post(url=f'{self.cluster_url}/tunnels', json=data)

        if(response.is_error):
            raise Exception(response.json()['error'])
        print(response.json()['content'])


    def get_container(self, name: str) -> RemoteContainer:
        return self.containers[name]


    def start(self):
        for worker in self.workers:
            worker.start()

    def stop(self):
        for worker in self.workers:
            if(worker.is_running):
                worker.stop()
            worker.remove()
        
        self.client.close()
