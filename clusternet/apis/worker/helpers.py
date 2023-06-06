from typing import List
import docker
import socket

from mininet.log import info
from clusternet.apis.worker.data import WorkerInstance


def get_hostname() -> str:
    return socket.gethostname()


def clean_containers_with_prefix(prefix: str) -> List[str]:
    client = docker.from_env()
    removed_containers = []

    for container in client.containers.list(all=True):
        name = str(container.name) # type: ignore
        if(name.startswith(prefix)):
            info(f'*** Cleaning container {name}\n')
            container.remove(force=True) # type: ignore
            removed_containers.append(name)
    
    return removed_containers