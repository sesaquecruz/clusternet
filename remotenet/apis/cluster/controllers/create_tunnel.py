from remotenet.apis.cluster.infra import Repository
from remotenet.apis.models import AddTunnelModel, WorkerModel
from remotenet.apis.cluster.services import get_worker_by_name
from remotenet.apis.presentation.exceptions import BadRequest, NotFound
from remotenet.apis.presentation.helpers import bad_request, created, error, internal_server_error, not_found, validate_required_params
from remotenet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse

class CreateTunnelController(Controller):
    def __init__(self, worker_name: str, repository: Repository) -> None:
        self.worker_name = worker_name
        self.repository  = repository

    
    def create_tunnel(self, worker: WorkerModel, model: AddTunnelModel):
        if(worker.ip == model.remote_ip):
            raise Exception('Tunnel loops are not allowed')
        
        if(worker.is_running):
            raise Exception(f'Stop the Worker {worker.name} before add a tunnel')
        
        self.repository.add_tunnel(model)


    def verify_if_tunnel_exist(self, worker: WorkerModel, remote_worker: WorkerModel):
        for tunnel in worker.tunnels:
            if(tunnel.remote_ip == remote_worker.ip):
                raise Exception(f'Already exists a tunnel to worker {remote_worker.name}')


    def handle(self, request: HttpRequest) -> HttpResponse:
        required_params = ['remote_worker']

        try:
            validate_required_params(request, required_params)
            remote_worker_name = request.body['remote_worker']

            worker = get_worker_by_name(self.worker_name, self.repository)
            remote_worker = get_worker_by_name(remote_worker_name, self.repository)
            
            self.verify_if_tunnel_exist(worker, remote_worker)
            self.verify_if_tunnel_exist(remote_worker, worker)

            tunnel1 = AddTunnelModel(worker.id, worker.switch, remote_worker.ip)
            tunnel2 = AddTunnelModel(remote_worker.id, remote_worker.switch, worker.ip)
            self.create_tunnel(worker, tunnel1)
            self.create_tunnel(remote_worker, tunnel2)

            return created({'content': f'Tunnel pair created between {worker.name} and {remote_worker.name}'})

        except BadRequest as ex:
            return bad_request(error(f'{ex}'))
        except NotFound as ex:
            return not_found(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))
        