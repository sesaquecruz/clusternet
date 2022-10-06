import socket
from typing import Any, Dict, List

from clusternet.apis.models import ContainerModel
from clusternet.apis.presentation.exceptions import BadRequest, NotFound
from clusternet.apis.presentation.helpers import bad_request, created, error, internal_server_error, not_found, validate_required_params
from clusternet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse
from clusternet.apis.worker.services import WorkerInstance



class StartWorkerController(Controller):
    def __init__(self) -> None:
        self.net = WorkerInstance.instance()
    

    def validate_containers(self, data: Dict[str, Any]) -> List[ContainerModel]:        
        containers = [ContainerModel.from_dict(item) for item in data['containers']]

        if(not containers):
            raise Exception(f'Expecting at least one container')
        return containers
    

    def handle(self, request: HttpRequest) -> HttpResponse:   
        required_params = ['switch', 'controller_ip', 'controller_port', 'containers']
        
        try:
            if(self.net.is_running):
                raise Exception('Worker already is running')
            
            validate_required_params(request, required_params)
            
            containers = self.validate_containers(request.body)
            self.net.start(request, containers)

        except BadRequest as ex:
            return bad_request(error(f'{ex}'))
        except NotFound as ex:
            return not_found(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))
        
        return created({'content': f'Worker {socket.gethostname()} started'})
        