from clusternet.apis.cluster.infra import Repository
from clusternet.apis.cluster.services import get_worker_by_name, stop_remote_worker
from clusternet.apis.presentation.exceptions import NotFound
from clusternet.apis.presentation.helpers import error, internal_server_error, not_found
from clusternet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse


class StopWorkerController(Controller):
    def __init__(self, worker_name: str, repository: Repository) -> None:
        self.worker_name = worker_name
        self.repository  = repository
    
    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            worker = get_worker_by_name(self.worker_name, self.repository)

            response = stop_remote_worker(worker)
            if(response.is_ok):
                worker.stop()
                self.repository.remove_tunnels_by_worker_id(worker.id)
                self.repository.update_worker(worker)

            return response

        except NotFound as ex:
            return not_found(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))
        