from clusternet.apis.cluster.infra import Repository
from clusternet.apis.models.worker import AddWorkerModel
from clusternet.apis.presentation.exceptions import BadRequest, NotFound
from clusternet.apis.presentation.helpers import bad_request, created, internal_server_error, not_found, error, validate_required_params
from clusternet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse


class CreateWorkerController(Controller):
    def __init__(self, repository: Repository) -> None:
        self.repository = repository


    def create_worker(self, model: AddWorkerModel) -> HttpResponse:
        self.repository.add_worker(model)
        return created({'content': f'Worker {model.name} created'})

    
    def verify_if_worker_exists(self, name: str, ip: str):
        worker = self.repository.get_worker_by_name(name)
        if(worker is not None):
            raise Exception(f'Worker {name} already exists')

        worker = self.repository.get_worker_by_ip(ip)
        if(worker is not None):
            raise Exception(f'Worker ip {ip} already exists')


    def handle(self, request: HttpRequest) -> HttpResponse:
        required_params = ['name', 'ip', 'controller_ip', 'controller_port']

        try:
            validate_required_params(request, required_params)
            name, ip = request.body['name'], request.body['ip']
            self.verify_if_worker_exists(name, ip)

            model = AddWorkerModel.from_dict({
                'name': request.get('name'),
                'ip': request.get('ip'),
                'controller_ip': request.get('controller_ip'),
                'controller_port': int(request.body['controller_port']),
            })
            return self.create_worker(model)

        except BadRequest as ex:
            return bad_request(error(f'{ex}'))
        except NotFound as ex:
            return not_found(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))
