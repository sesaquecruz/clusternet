from clusternet.apis.presentation.exceptions import BadRequest, NotFound
from clusternet.apis.presentation.helpers import (
    bad_request, error, internal_server_error, not_found, success, validate_required_params
)
from clusternet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse
from clusternet.apis.worker.services import WorkerInstance, get_hostname


class RunCommandOnHostController(Controller):
    def __init__(self, name: str) -> None:
        self.net = WorkerInstance.instance()
        self.name = name
    
    def handle(self, request: HttpRequest) -> HttpResponse:
        hostname = get_hostname()
        required_params = ['command']

        try:        
            validate_required_params(request, required_params)

            if(not self.name in self.net):
                raise NotFound(f'[{hostname}]: node {self.name} not found')

            command = request.body['command']
            host    = self.net.getHost(self.name)
            output  = host.cmd(command)

            return success({'content': output})
            
        except BadRequest as ex:
            return bad_request(error(f'{ex}'))
        except NotFound as ex:
            return not_found(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))
