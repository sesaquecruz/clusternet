import os

from flask import Flask, jsonify, request
from flask.wrappers import Request

from clusternet.apis.worker.controllers import (
    AddDockerController, 
    RunCommandOnHostController, RunPingallController,
    StartWorkerController, StopWorkerController
)
from clusternet.apis.presentation.helpers import parse_request
from clusternet.apis.presentation.protocols import Controller


server = Flask(__name__)


def make_response(controller: Controller, request: Request):
    response = controller.handle(parse_request(request))
    return jsonify(response.body), response.status_code


@server.route('/containers', methods=['POST'])
def add_container():
    controller = AddDockerController()
    return make_response(controller, request)


@server.route('/hosts/<string:name>/cmd', methods=['POST'])
def run_command(name: str):
    controller = RunCommandOnHostController(name)
    return make_response(controller, request)


@server.route('/hosts/pingall', methods=['GET'])
def run_pingall():
    controller = RunPingallController()
    return make_response(controller, request)


@server.route('/start', methods=['GET'])
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
    