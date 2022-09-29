from remotenet.apis.cluster.infra import Repository
from remotenet.apis.models.worker import AddWorkerModel
from remotenet.apis.presentation.exceptions import BadRequest, NotFound
from remotenet.apis.presentation.helpers import bad_request, created, internal_server_error, not_found, error, validate_required_params
from remotenet.apis.presentation.protocols import Controller, HttpRequest, HttpResponse


class CreateWorkerController(Controller):
    def __init__(self, repository: Repository) -> None:
        self.repository = repository


    def create_worker(self, model: AddWorkerModel) -> HttpResponse:
        self.repository.add_worker(model)
        return created({'content': f'Worker {model.name} created'})

    
    def verify_if_worker_exists(self, name: str, url: str):
        worker = self.repository.get_worker_by_name(name)
        if(worker is not None):
            raise Exception(f'Worker {name} already exists')

        worker = self.repository.get_worker_by_url(url)
        if(worker is not None):
            raise Exception('Worker url already exists')


    def handle(self, request: HttpRequest) -> HttpResponse:
        required_params = ['name', 'url', 'controller_ip', 'controller_port']

        try:
            validate_required_params(request, required_params)
            name, url = request.body['name'], request.body['url']
            self.verify_if_worker_exists(name, url)

            model = AddWorkerModel.from_dict({
                'name': request.get('name'),
                'controller_ip': request.get('controller_ip'),
                'controller_port': int(request.body['controller_port']),
                'url': request.get('url')})
            return self.create_worker(model)

        except BadRequest as ex:
            return bad_request(error(f'{ex}'))
        except NotFound as ex:
            return not_found(error(f'{ex}'))
        except Exception as ex:
            return internal_server_error(error(f'{ex}'))
