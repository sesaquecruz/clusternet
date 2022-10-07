from clusternet.apis.cluster.infra import Repository
from clusternet.apis.cluster.services import get_container_by_name
from clusternet.apis.presentation.exceptions import NotFound
from clusternet.apis.presentation.helpers import error, internal_server_error, not_found, success
from clusternet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse


class GetContainerController(Controller):
    def __init__(self, name: str, repository: Repository) -> None:
        self.name       = name
        self.repository = repository
    

    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            container = get_container_by_name(self.name, self.repository)
            return success({'content': container.to_dict()})
        
        except NotFound as ex:
            return not_found(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))