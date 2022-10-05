from clusternet.apis.cluster.infra import Repository
from clusternet.apis.presentation.helpers import error, internal_server_error, success
from clusternet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse


class ListContainersController(Controller):
    def __init__(self, repository: Repository) -> None:
        self.repository = repository
    

    def handle(self, request: HttpRequest) -> HttpResponse:
        try:
            containers = self.repository.get_containers()
            data       = list(map(lambda container: container.to_dict(), containers))
            return success({'content': data})
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))
    