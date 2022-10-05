import httpx

class RemoteContainer:
    def __init__(self, cluster_url: str, name: str, worker: str) -> None:
        self.cluster = cluster_url
        self.name    = name
        self.worker  = worker

    def cmd(self, command: str) -> str:
        data = {'command': command}
        response = httpx.post(url=f'{self.cluster}/containers/{self.name}/cmd', json=data)
        
        if(response.is_error):
            raise Exception(response.json()['error'])
        
        return response.json()['content']