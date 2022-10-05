from clusternet.apis.presentation.exceptions import BadRequest, NotFound
from clusternet.apis.presentation.helpers import bad_request, created, error, internal_server_error, not_found, validate_required_params
from clusternet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse
from clusternet.apis.worker.services import WorkerInstance

class AddContainerController(Controller):
    def __init__(self) -> None:
        self.net = WorkerInstance.instance()
    
    def handle(self, request: HttpRequest) -> HttpResponse:
        required_params = ['name', 'dimage', 'cpu_period', 'cpu_quota', 'mem_limit']

        try:
            if(not self.net.is_running):
                raise Exception('Worker not is running')
            
            validate_required_params(request, required_params)
            
            name = request.body.pop('name')
            if(name in self.net):
                raise Exception(f'Container {name} already exists')
             
            self.net.addDocker(name=name, **request.body)
            self.net.addLink(name, self.net.switches[0])
            self.net.configHosts()
            
            return created({'content': f'Container {name} created'})
        
        except BadRequest as ex:
            return bad_request(error(f'{ex}'))
        except NotFound as ex:
            return not_found(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))
        
        
        