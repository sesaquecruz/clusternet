import httpx


class RemoteWorker:
    def __init__(self, cluster: str, name: str, ip: str, controller_ip: str, controller_port: int) -> None:
        self.cluster    = cluster
        self.name       = name
        self.ip         = ip
        self.controller = controller_ip
        self.port       = controller_port
        self.is_running = False


    def start(self):
        response = httpx.get(url=f'{self.cluster}/workers/{self.name}/start', timeout=None)
        
        if(response.is_error):
            raise Exception(response.json()['error'])

        self.is_running = True
        print(f'** {response.json()["content"]}')


    def stop(self):
        response = httpx.get(url=f'{self.cluster}/workers/{self.name}/stop', timeout=None)
        
        if(response.is_error):
            raise Exception(response.json()['error'])
        
        self.is_running = False
        print(f'** {response.json()["content"]}')
