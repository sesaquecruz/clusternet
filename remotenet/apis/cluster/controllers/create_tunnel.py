from remotenet.apis.cluster.infra import Repository
from remotenet.apis.models import AddTunnelModel, WorkerModel
from remotenet.apis.cluster.services import get_worker_by_name, run_command_on_host
from remotenet.apis.presentation.exceptions import BadRequest, NotFound
from remotenet.apis.presentation.helpers import bad_request, error, internal_server_error, not_found, validate_required_params
from remotenet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse

class CreateTunnelController(Controller):
    def __init__(self, repository: Repository) -> None:
        self.repository  = repository

    def create_tunnel(self, worker: WorkerModel, model: AddTunnelModel) -> HttpResponse:
        tunnel = self.repository.add_tunnel(model)
        response = run_command_on_host(worker.url, worker.switch, tunnel.command)

        if(not response.is_ok):
            self.repository.remove_tunnel_by_id(tunnel.id)
        return response

    def handle(self, request: HttpRequest) -> HttpResponse:
        required_params = ['worker_name', 'remote_ip']

        try:
            validate_required_params(request, required_params)
            worker_name = request.body['worker_name']
            remote_ip   = request.body['remote_ip'] 

            worker = get_worker_by_name(worker_name, self.repository)
            tunnel = AddTunnelModel(worker.id, worker.switch, remote_ip)
            return self.create_tunnel(worker, tunnel)

        except BadRequest as ex:
            return bad_request(error(f'{ex}'))
        except NotFound as ex:
            return not_found(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))
        