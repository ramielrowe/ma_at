import os

import docker.errors

from ma_at import docker_util

GOOGLE_USER = os.getenv('GOOGLE_USER')
GOOGLE_PASSWORD = os.getenv('GOOGLE_PASSWORD')
POKEMAP_DOMAIN = os.getenv('POKEMAP_DOMAIN')


def pokemap(username, location):
    container_name = 'pokemap-{}'.format(username)

    docker_client = docker_util.get_client()

    try:
        existing_container = docker_util.inspect_by_name(docker_client,
                                                         container_name)
    except docker.errors.NotFound as e:
        existing_container = None

    if not location and existing_container:
        port_resp = docker_client.port(existing_container['Id'], 5000)
        port_5000_resp = port_resp[0]
        hostport = port_5000_resp['HostPort']
        return 'http://{}:{}'.format(POKEMAP_DOMAIN, hostport)
    elif not location and not existing_container:
        return ('Error: no existing pokemap, please provide '
                'location to create one.')
    elif location and existing_container:
        docker_client.remove_container(existing_container['Id'],
                                       force=True,
                                       v=True)

    env = {
        'GOOGLE_USER': GOOGLE_USER,
        'GOOGLE_PASSWORD': GOOGLE_PASSWORD,
        'LOCATION': location
    }

    host_config = docker_client.create_host_config(port_bindings={5000: None})

    new_container = docker_client.create_container(name=container_name,
                                                   image='pokemap',
                                                   ports=[5000, ],
                                                   environment=env,
                                                   host_config=host_config)

    docker_client.start(new_container['Id'])
    port = docker_client.port(new_container['Id'], 5000)[0]['HostPort']
    return 'http://{}:{}'.format(POKEMAP_DOMAIN, port)
