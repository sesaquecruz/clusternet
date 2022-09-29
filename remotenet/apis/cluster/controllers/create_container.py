from remotenet.apis.cluster.infra import Repository
from remotenet.apis.models import AddContainerModel, WorkerModel
from remotenet.apis.cluster.services import get_worker_by_name
from remotenet.apis.presentation.exceptions import BadRequest, NotFound
from remotenet.apis.presentation.helpers import bad_request, created, error, internal_server_error, not_found, validate_required_params
from remotenet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse


class CreateContainerController(Controller):
    def __init__(self, repository: Repository) -> None:
        self.repository  = repository


    def create_container(self, worker: WorkerModel, model: AddContainerModel) -> HttpResponse:
        if(worker.is_running):
            raise Exception(f'Stop the Worker {worker.name} before add that container')

        container = self.repository.add_container(model)
        return created({'content': f'Container {container.name} created at {worker.url}'})
    

    def verify_if_container_exists(self, name: str, ip: str):
        container = self.repository.get_container_by_name(name)
        if(container is not None):
            raise Exception(f'Container {name} already exists')
        
        container = self.repository.get_container_by_ip(ip)
        if(container is not None):
            raise Exception(f'Container {ip} already exists')

    
    def handle(self, request: HttpRequest) -> HttpResponse:
        required_params = ['worker_name', 'name', 'ip', 'dimage', 'cpu_period', 'cpu_quota', 'mem_limit']

        try:
            validate_required_params(request, required_params)

            container_name = request.body['name']
            worker_name = request.body['worker_name']
            container_ip = request.body['ip']

            self.verify_if_container_exists(name=container_name, ip=container_ip)
            worker = get_worker_by_name(worker_name, self.repository)
            
            container = AddContainerModel.from_dict({
                'worker_id':    worker.id,
                'name':         request.get('name'),
                'ip':           request.get('ip'),
                'dimage':       request.get('dimage'),
                'cpu_period':   request.get('cpu_period'),
                'cpu_quota':    request.get('cpu_quota'),
                'mem_limit':    request.get('mem_limit')
            })
            return self.create_container(worker, container)
            
        except BadRequest as ex:
            return bad_request(error(f'{ex}'))
        except NotFound as ex:
            return not_found(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))