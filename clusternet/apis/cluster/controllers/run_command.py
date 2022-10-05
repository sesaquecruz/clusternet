from clusternet.apis.cluster.infra import Repository
from clusternet.apis.cluster.services import get_container_by_name, get_worker_by_id, run_command_on_host
from clusternet.apis.presentation.exceptions import BadRequest, NotFound
from clusternet.apis.presentation.helpers import bad_request, error, internal_server_error, not_found, validate_required_params
from clusternet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse


class RunCommandOnContainerController(Controller):
    def __init__(self, name: str, repository: Repository) -> None:
        self.name       = name
        self.repository = repository

    def handle(self, request: HttpRequest) -> HttpResponse:
        required_params = ['command']
        try:
            validate_required_params(request, required_params)
            container = get_container_by_name(self.name, self.repository)
            worker = get_worker_by_id(container.worker_id, self.repository)
            return run_command_on_host(worker.url, container.name, command=request.body['command'])
            
        except BadRequest as ex:
            return bad_request(error(f'{ex}'))
        except NotFound as ex:
            return not_found(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))