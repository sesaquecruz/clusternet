import httpx

from apis.cluster.infra import Repository
from apis.models import WorkerModel
from apis.models.container import ContainerModel
from apis.presentation.exceptions import NotFound
from apis.presentation.protocols import HttpResponse


def get_container_by_name(name: str, repository: Repository) -> ContainerModel:
    container = repository.get_container_by_name(name)
    if(container is None):
        raise NotFound(f'Container {name} not found')
    return container

def get_worker_by_id(worker_id: int, repository: Repository) -> WorkerModel:
    worker = repository.get_worker_by_id(worker_id)
    if(worker is None):
        raise NotFound(f'Worker {worker_id} not found')
    return worker

def get_worker_by_name(name: str, repository: Repository) -> WorkerModel:
    worker = repository.get_worker_by_name(name)
    if(worker is None):
        raise NotFound(f'Worker {name} not found')
    return worker


def create_container_on_remote_worker(worker: WorkerModel, container: ContainerModel) -> HttpResponse:
    raise Exception('To be implemented')


def start_remote_worker(worker: WorkerModel) -> HttpResponse:
    body = worker.to_dict()
    body['switch'] = worker.switch
    body.pop('is_running')
    body.pop('tunnels')
    response   = httpx.post(url=f'{worker.url}/start', json=body, timeout=None)
    
    return HttpResponse(
        status_code=response.status_code,
        body=response.json()
    )
    

def stop_remote_worker(worker: WorkerModel) -> HttpResponse:
    response = httpx.get(url=f'{worker.url}/stop', timeout=None)
    return HttpResponse(
        status_code=response.status_code,
        body=response.json()
    )


def run_command_on_host(worker_url: str, host: str, command: str) -> HttpResponse:
    data = {'command': command}
    response = httpx.post(f'{worker_url}/cmd/{host}', json=data, timeout=None)

    return HttpResponse(
        status_code=response.status_code,
        body=response.json()
    )