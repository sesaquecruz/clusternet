from remotenet.apis.presentation.helpers import error, internal_server_error, success
from remotenet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse
from remotenet.apis.worker.services import WorkerInstance

class RunPingallController(Controller):
    def __init__(self) -> None:
        self.net = WorkerInstance.instance()
    
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            if(not self.net.is_running):
                raise Exception('Worker not is running')

            packets = self.net.pingAll()
            
            return success({'content': f'{packets}% dropped', 'dropped': packets})
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))
    