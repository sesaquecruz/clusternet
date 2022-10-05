import os
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask.wrappers import Request

from clusternet.apis.cluster.controllers import (
    CreateContainerController, CreateTunnelController, CreateWorkerController, 
    ListContainersController, ListWorkersController,
    RemoveContainerController, RunCommandOnContainerController, RemoveWorkerController, 
    StartWorkerController, StopWorkerController
)

from clusternet.apis.cluster.infra.inmemory import InMemoryRepository
from clusternet.apis.presentation.helpers import parse_request
from clusternet.apis.presentation.protocols import Controller

server     = Flask(__name__)
repository = InMemoryRepository()
cors       = CORS(server)

def make_response(controller: Controller, request: Request):
    response = controller.handle(parse_request(request))
    return jsonify(response.body), response.status_code



@server.route('/', methods=['GET'])
def index():
    return jsonify({'content': 'Cluster'}), 200


@server.route('/containers', methods=['POST'])
def create_container():
    controller = CreateContainerController(repository)
    return make_response(controller, request) 


@server.route('/containers/<string:name>', methods=['DELETE'])
def remove_container(name: str):
    controller = RemoveContainerController(name, repository)
    return make_response(controller, request) 


@server.route('/containers', methods=['GET'])
def get_containers():
    controller = ListContainersController(repository)
    return make_response(controller, request)


@server.route('/containers/<string:name>/cmd', methods=['POST'])
def run_command(name: str):
    controller = RunCommandOnContainerController(name, repository)
    return make_response(controller, request)


@server.route('/workers/<string:name>/tunnel', methods=['POST'])
def create_tunnel(name: str):
    controller = CreateTunnelController(name, repository)
    return make_response(controller, request) 


@server.route('/workers', methods=['POST'])
def create_worker():
    controller = CreateWorkerController(repository)
    return make_response(controller, request) 


'''
@server.route('/workers/<int:id>', methods=['GET'])
def get_worker(id: int):
    controller = GetWorkerController(id, repository)
    return make_response(controller, request)
'''


@server.route('/workers/<string:name>', methods=['DELETE'])
def remove_worker(name: str):
    controller = RemoveWorkerController(name, repository)
    return make_response(controller, request)


@server.route('/workers', methods=['GET'])
def get_workers():
    controller = ListWorkersController(repository)
    return make_response(controller, request)


@server.route('/workers/<string:name>/start', methods=['GET'])
def start_worker(name: str):
    controller = StartWorkerController(name, repository)
    return make_response(controller, request)


@server.route('/workers/<string:name>/stop', methods=['GET'])
def stop_worker(name: str):
    controller = StopWorkerController(name, repository)
    return make_response(controller, request)


def main():
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 6060)))

if(__name__=='__main__'):
    main()    
