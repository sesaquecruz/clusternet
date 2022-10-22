from typing import List
from clusternet.apis.presentation.exceptions import BadRequest, NotFound
from clusternet.apis.presentation.helpers import (
    bad_request, created, error, internal_server_error, not_found, validate_required_params
)
from clusternet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse
from clusternet.apis.worker.services import WorkerInstance, get_hostname

class AddLinkController(Controller):
    def __init__(self) -> None:
        self.net = WorkerInstance.instance()

    def verify_if_node_exist(self, nodes: List[str]):
        for node in nodes:
            if(not node in self.net): 
                raise NotFound(f'[{get_hostname()}]: node {node} not found')

    def handle(self, request: HttpRequest) -> HttpResponse:
        required_params = ['node1', 'node2']
        hostname = get_hostname()

        try:
            validate_required_params(request, required_params)
            node1 = request.body['node1']
            node2 = request.body['node2']

            self.verify_if_node_exist(nodes=[node1, node2])
            
            if(self.net.linksBetween(node1, node2)):
                raise Exception(f'[{hostname}]: already exist a link between {node1} and {node2}')

            self.net.addLink(**request.body)
            
            return created({'content': f'[{hostname}]: link created between {node1} and {node2}'})

        except BadRequest as ex:
            return bad_request(error(f'{ex}'))
        except NotFound as ex:
            return not_found(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))