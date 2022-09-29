from remotenet.apis.cluster.infra import Repository
from remotenet.apis.cluster.services import get_worker_by_id
from remotenet.apis.presentation.exceptions import NotFound
from remotenet.apis.presentation.helpers import error, internal_server_error, not_found, success
from remotenet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse


class GetWorkerController(Controller):
    def __init__(self, worker_id: int, repository: Repository) -> None:
        self.worker_id  = worker_id
        self.repository = repository
    

    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            worker = get_worker_by_id(self.worker_id, self.repository)
            return success({'content': worker.to_dict()})
        
        except NotFound as ex:
            return not_found(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))