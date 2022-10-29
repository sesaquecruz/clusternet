import httpx


class RemoteContainer:
    def __init__(self, name: str, url: str) -> None:
        self.name = name
        self.url = url

    def cmd(self, command: str) -> str:
        data = {'command': command}
        response = httpx.post(url=f'{self.url}/hosts/{self.name}/cmd', json=data, timeout=None)
        
        if(response.is_error):
            raise Exception(response.json()['error'])
        
        return response.json()['content']