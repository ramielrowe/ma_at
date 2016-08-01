import os
import time

import docker.errors

from ma_at import docker_util

POKEMAP_AUTH = os.getenv('POKEMAP_AUTH')
POKEMAP_USER = os.getenv('POKEMAP_USER')
POKEMAP_PASSWORD = os.getenv('POKEMAP_PASSWORD')
GOOGLE_MAPS_KEY = os.getenv('GOOGLE_MAPS_KEY')
POKEMAP_DOMAIN = os.getenv('POKEMAP_DOMAIN')


def pokemap(username, location, image='pokemap', steps='8'):
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
        while docker_util.inspect_by_name(docker_client, container_name):
            time.sleep(0.1)

    env = {
        'POKEMAP_AUTH': POKEMAP_AUTH,
        'POKEMAP_USER': POKEMAP_USER,
        'POKEMAP_PASSWORD': POKEMAP_PASSWORD,
        'GOOGLE_MAPS_KEY': GOOGLE_MAPS_KEY,
        'LOCATION': location,
        'STEPS': steps,
    }

    host_config = docker_client.create_host_config(port_bindings={5000: None},
                                                   mem_limit='128M',
                                                   memswap_limit='256M')

    new_container = docker_client.create_container(
        name=container_name, image=image, ports=[5000, ],
        environment=env, host_config=host_config)

    docker_client.start(new_container['Id'])
    port = docker_client.port(new_container['Id'], 5000)[0]['HostPort']
    return 'http://{}:{}'.format(POKEMAP_DOMAIN, port)
