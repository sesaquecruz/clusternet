from clusternet.apis.presentation.exceptions import BadRequest, NotFound
from clusternet.apis.presentation.helpers import bad_request, error, internal_server_error, not_found, success, validate_required_params
from clusternet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse
from clusternet.apis.worker.services import WorkerInstance


class RunCommandOnHostController(Controller):
    def __init__(self, hostname: str) -> None:
        self.net = WorkerInstance.instance()
        self.hostname = hostname
    
    def handle(self, request: HttpRequest) -> HttpResponse:
        required_params = ['command']

        try:
            if(not self.net.is_running):
                raise Exception('Worker not is running')
            
            if(not self.hostname in self.net):
                raise NotFound(f'Host {self.hostname} not found')

            validate_required_params(request, required_params)

            command = request.get('command')
            host    = self.net.getHost(self.hostname)
            output  = host.cmd(command)

            return success({'content': output})
            
        except BadRequest as ex:
            return bad_request(error(f'{ex}'))
        except NotFound as ex:
            return not_found(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))
