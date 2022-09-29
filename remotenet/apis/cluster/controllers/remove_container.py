from remotenet.apis.cluster.infra import Repository
from remotenet.apis.cluster.services import get_container_by_name, get_worker_by_id
from remotenet.apis.presentation.exceptions import BadRequest, NotFound
from remotenet.apis.presentation.helpers import bad_request, error, internal_server_error, not_found, success
from remotenet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse


class RemoveContainerController(Controller):
    def __init__(self, name: str, repository: Repository) -> None:
        self.name = name
        self.repository = repository
    
    def remove_container(self):
        container = get_container_by_name(self.name, self.repository)
        worker = get_worker_by_id(container.worker_id, self.repository)
        
        if(worker.is_running):
            raise Exception(f'Stop the Worker {worker.name} before remove that container')
        self.repository.remove_container(container.id)
        
    
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            self.remove_container()
            return success({'content': f'Container {self.name} removed'})
        
        except BadRequest as ex:
            return bad_request(error(f'{ex}'))
        except NotFound as ex:
            return not_found(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))