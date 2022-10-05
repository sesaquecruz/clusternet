import socket
from typing import Any, Dict, List

from mininet.node import RemoteController

from clusternet.apis.models.container import ContainerModel
from clusternet.apis.presentation.exceptions import BadRequest, NotFound
from clusternet.apis.presentation.helpers import bad_request, created, error, internal_server_error, not_found, validate_required_params
from clusternet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse
from clusternet.apis.worker.services import WorkerInstance



class StartWorkerController(Controller):
    def __init__(self) -> None:
        self.net = WorkerInstance.instance()
    

    def validate_containers(self, data: Dict[str, Any]) -> List[ContainerModel]:        
        containers = []
        
        for item in data['containers']:
            containers.append(ContainerModel.from_dict(item))

        if(not containers):
            raise Exception(f'Expecting at least one container')
        return containers
    

    def start_containernet(self, request: HttpRequest, containers: List[ContainerModel]):
        switch_name     = request.get('switch')
        controller_ip   = request.get('controller_ip')
        controller_port = request.get('controller_port')

        self.net.addController(name='c0', controller=RemoteController, ip=controller_ip, port=controller_port)
        self.net.addSwitch(name=switch_name)

        for container in containers:
            if(container.name in self.net): continue

            container_params = container.to_dict()
            container_params.pop('name')
            self.net.addDocker(container.name, **container_params)
            self.net.addLink(container.name, switch_name)
        self.net.start()


    def handle(self, request: HttpRequest) -> HttpResponse:   
        required_params = ['switch', 'controller_ip', 'controller_port', 'containers']
        
        try:
            if(self.net.is_running):
                raise Exception('Worker already is running')
            
            validate_required_params(request, required_params)
            
            containers = self.validate_containers(request.body)
            self.start_containernet(request, containers)

        except BadRequest as ex:
            return bad_request(error(f'{ex}'))
        except NotFound as ex:
            return not_found(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))
        
        return created({'content': f'Worker {socket.gethostname()} started'})
        