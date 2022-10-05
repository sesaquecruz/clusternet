from clusternet.apis.cluster.infra import Repository
from clusternet.apis.cluster.services import get_worker_by_name
from clusternet.apis.presentation.exceptions import BadRequest, NotFound
from clusternet.apis.presentation.helpers import bad_request, error, internal_server_error, not_found, success
from clusternet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse


class RemoveWorkerController(Controller):
    def __init__(self, name: str, repository: Repository) -> None:
        self.name = name
        self.repository = repository
    
    def remove_worker(self):
        worker = get_worker_by_name(self.name, self.repository)
        
        if(worker.is_running):
            raise Exception(f'Stop the Worker {worker.name} before remove it')
        self.repository.remove_worker(worker.id)
        
    
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            self.remove_worker()
            return success({'content': f'Worker {self.name} removed'})
        
        except BadRequest as ex:
            return bad_request(error(f'{ex}'))
        except NotFound as ex:
            return not_found(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))