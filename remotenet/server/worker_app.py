import os

from flask import Flask, jsonify, request
from flask.wrappers import Request

from remotenet.apis.worker.controllers import (
    AddContainerController, ListContainersController, 
    RunCommandOnHostController, RunPingallController,
    StartWorkerController, StopWorkerController
)
from remotenet.apis.presentation.helpers import parse_request
from remotenet.apis.presentation.protocols import Controller


server = Flask(__name__)


def make_response(controller: Controller, request: Request):
    response = controller.handle(parse_request(request))
    return jsonify(response.body), response.status_code
    
    

@server.route('/containers', methods=['GET'])
def get_containers():
    controller = ListContainersController()
    return make_response(controller, request)


@server.route('/containers', methods=['POST'])
def add_container():
    controller = AddContainerController()
    return make_response(controller, request)


@server.route('/cmd/<string:host>', methods=['POST'])
def run_command(host: str):
    controller = RunCommandOnHostController(hostname=host)
    return make_response(controller, request)


@server.route('/pingall', methods=['GET'])
def run_pingall():
    controller = RunPingallController()
    return make_response(controller, request)


@server.route('/start', methods=['POST'])
def start():
    controller = StartWorkerController()
    return make_response(controller, request)


@server.route('/stop', methods=['GET'])
def stop():
    controller = StopWorkerController()
    return make_response(controller, request)


def main():
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

if(__name__=='__main__'):
    main()
    