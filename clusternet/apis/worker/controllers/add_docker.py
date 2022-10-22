from clusternet.apis.presentation.exceptions import BadRequest
from clusternet.apis.presentation.helpers import (
    bad_request, created, error, internal_server_error, validate_required_params
)
from clusternet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse
from clusternet.apis.worker.services import WorkerInstance

class AddDockerController(Controller):
    def __init__(self) -> None:
        self.net = WorkerInstance.instance()
    
    def handle(self, request: HttpRequest) -> HttpResponse:
        required_params = ['name']

        try: 
            validate_required_params(request, required_params)
            name = request.body['name']

            if(name in self.net):
                raise Exception(f'Container {name} already exists')
             
            self.net.addDocker(**request.body)
            return created({'content': f'Container {name} created'})
        
        except BadRequest as ex:
            return bad_request(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))
        