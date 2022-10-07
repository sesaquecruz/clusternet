import httpx

from clusternet.apis.models import ContainerModel

class RemoteContainer:
    def __init__(self, cluster_url: str, model: ContainerModel) -> None:
        self.cluster = cluster_url
        self.model   = model

    @property
    def name(self) -> str:
        return self.model.name
    
    @property
    def ip(self) -> str:
        return self.model.ip

    def cmd(self, command: str) -> str:
        data = {'command': command}
        response = httpx.post(url=f'{self.cluster}/containers/{self.name}/cmd', json=data)
        
        if(response.is_error):
            raise Exception(response.json()['error'])
        
        return response.json()['content']