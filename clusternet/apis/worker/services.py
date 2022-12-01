import socket

from clusternet.apis.worker.data import WorkerInstance


def get_hostname() -> str:
    return socket.gethostname()
