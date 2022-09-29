from remotenet.apis.cluster.infra import Repository
from remotenet.apis.presentation.helpers import error, internal_server_error, success
from remotenet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse


class ListWorkersController(Controller):
    def __init__(self, repository: Repository) -> None:
        self.repository = repository
    
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            workers = self.repository.get_workers()
            data    = list(map(lambda worker: worker.to_dict(), workers))
            return success({'content': data})
        
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))
        