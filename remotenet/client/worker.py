import httpx


class RemoteWorker:
    def __init__(self, cluster: str, name: str, url: str, controller_ip: str, controller_port: int) -> None:
        self.cluster    = cluster
        self.name       = name
        self.url        = url
        self.controller = controller_ip
        self.port       = controller_port
        self.is_running = False
    

    def remove(self):
        response = httpx.delete(url=f'{self.cluster}/workers/{self.name}')
        
        if(response.is_error):
            raise Exception(response.json()['error'])
        print(response.json()['content'])


    def start(self):
        response = httpx.get(url=f'{self.cluster}/workers/{self.name}/start', timeout=None)
        
        if(response.is_error):
            raise Exception(response.json()['error'])

        self.is_running = True
        print(response.json()['content'])


    def stop(self):
        response = httpx.get(url=f'{self.cluster}/workers/{self.name}/stop', timeout=None)
        
        if(response.is_error):
            raise Exception(response.json()['error'])
        
        self.remove()
        self.is_running = False
        print(response.json()['content'])
