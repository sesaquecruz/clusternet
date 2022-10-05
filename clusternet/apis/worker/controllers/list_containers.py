from typing import Any, Dict

from mininet.node import Docker

from clusternet.apis.presentation.helpers import error, internal_server_error, success
from clusternet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse
from clusternet.apis.worker.services import WorkerInstance

def parse_container_params(container: Docker) -> Dict[str, Any]: 
    return {
        'name': container.name, 
        'dimage': container.dimage,
        **container.params}

class ListContainersController(Controller):
    def __init__(self) -> None:
        self.net = WorkerInstance.instance()
    
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            containers = [
                parse_container_params(docker)
                for docker in self.net.hosts
            ]
            return success({'content': containers})
        except Exception as ex:
            message = f'{ex}'
            return internal_server_error(error(message))

        