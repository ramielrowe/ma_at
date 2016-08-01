import os

import docker
import docker.errors
from docker import tls

DOCKER_HOST = os.getenv('MA_AT_DOCKER_HOST')


def get_client():
    tls_config = tls.TLSConfig(
        client_cert=('/etc/docker/server-cert.pem',
                     '/etc/docker/server-key.pem'),
        verify='/etc/docker/ca.pem'
    )
    return docker.Client(base_url=DOCKER_HOST, tls=tls_config)


def inspect_by_name(client, name):
    ids = client.containers(filters=dict(name=name), quiet=True, all=True)
    if ids:
        try:
            return client.inspect_container(ids[0])
        except docker.errors.NotFound as nfe:
            pass
