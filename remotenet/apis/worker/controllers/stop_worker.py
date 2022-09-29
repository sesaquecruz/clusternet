from remotenet.apis.presentation.helpers import error, internal_server_error, success
from remotenet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse
from remotenet.apis.worker.services import WorkerInstance


class StopWorkerController(Controller):
    def __init__(self) -> None:
        self.net = WorkerInstance.instance()
    
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            if(not self.net.is_running):
                raise Exception('Worker already is stopped')

            self.net.stop()
            WorkerInstance.clear_instance()
        except Exception as ex:
            message = f'{ex}'
            return internal_server_error(error(message))
        
        return success({'content': 'Worker stopped'})
            